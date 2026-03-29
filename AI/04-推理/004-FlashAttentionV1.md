# 图解大模型计算加速系列：FlashAttention V1，从硬件到计算逻辑

https://zhuanlan.zhihu.com/p/669926191

大家好哇，好久没有更新了，今天想来讲讲**Flash Attention（V1）**。

不知道你有没有和我一样的感受，第一次读Flash Attention的论文时，感觉头懵懵的：**它不仅涉及了硬件和cuda的知识，还涉及到很多计算逻辑上的trick。**我的痛点是不能在头脑中具象化整个流程，就更不要提对细节的推导了。

所以这篇文章我读了很久，也写了很久（一个月），最终决定按照如下方式对Flash Attention进行介绍：

- 本文一到三部分，介绍相关硬件知识及Flash Attention诞生背景。
- 本文四到五部分，通过**图解形式**介绍forward/backward中的分块计算过程。**所有的符号、公式都会给出详细的说明和推导过程**。我在阅读中发现论文的一些推导不太符合直觉（or写得可能不太对），所以这里我在遵从论文符号表达的基础上，部分内容按自己的理解重新顺了一遍。
- 本文第六到第八部分，量化介绍Flash attention在性能上的改进，包括计算量、显存和IO复杂度。

**【大模型计算加速系列】**

**[猛猿：图解大模型计算加速系列：FlashAttention V1，从硬件到计算逻辑](https://zhuanlan.zhihu.com/p/669926191)**

**[猛猿：图解大模型计算加速系列：Flash Attention V2，从原理到并行计算](https://zhuanlan.zhihu.com/p/691067658)**

**[猛猿：图解Mixtral 8 \* 7b推理优化原理与源码实现](https://zhuanlan.zhihu.com/p/691066049)**

**[猛猿：从啥也不会到CUDA GEMM优化](https://zhuanlan.zhihu.com/p/703256080)**

**[猛猿：图解大模型计算加速系列之：vLLM核心技术PagedAttention原理](https://zhuanlan.zhihu.com/p/691038809)**

**[猛猿：图解大模型计算加速系列：vLLM源码解析1，整体架构](https://zhuanlan.zhihu.com/p/691045737)**

**[猛猿：图解大模型计算加速系列：vLLM源码解析2，调度器策略(Scheduler)](https://zhuanlan.zhihu.com/p/692540949)**

**[猛猿：图解大模型计算加速系列：vLLM源码解析3，块管理器BlockManager（上篇）](https://zhuanlan.zhihu.com/p/700780161)**

**[猛猿：图解大模型计算加速系列：vLLM源码解析3，Prefix Caching](https://zhuanlan.zhihu.com/p/707228704)（BlockManager下篇）**

**[猛猿：图解大模型计算加速系列：分离式推理架构1，从DistServe谈起](https://zhuanlan.zhihu.com/p/706761664)**

**[猛猿：图解大模型计算加速系列：分离式推理架构2，模糊分离与合并边界的chunked-prefills](https://zhuanlan.zhihu.com/p/710165390)**



**【历史文章汇总】**

**[猛猿：【必看】历史技术文章导航](https://zhuanlan.zhihu.com/p/654910335)**



------

## 一、Flash attention在做一件什么事

我们知道，对于Transformer类的模型，假设其输入序列长度为 $N$ ，那么其计算复杂度和消耗的存储空间都为 $O(N^{2})$ 。也就是说，随着输入序列的变长，将给计算和存储带来极大的压力。

因此，我们迫切需要一种办法，能解决Transformer模型的 $O(N^{2})$ 复杂度问题。如果能降到 $O(N)$ ，那是最好的，即使做不到，逼近 $O(N)$ 那也是可以的。所以，Flash Attention就作为一种行之有效的解决方案出现了。

Flash Attention在做的事情，其实都包含在它的命名中了（**Fast and Memory Efficient Exact Attention with IO-Awareness**），我们逐一来看：



**(1）Fast（with IO-Awareness），计算快**。在Flash Attention之前，也出现过一些加速Transformer计算的方法，这些方法的着眼点是“减少计算量FLOPs”，例如用一个稀疏attention做近似计算。**但是Flash attention就不一样了，它并没有减少总的计算量，因为它发现：计算慢的卡点不在运算能力，而是在读写速度上。**所以它通过降低对显存（[HBM](https://zhida.zhihu.com/search?content_id=237002834&content_type=Article&match_order=1&q=HBM&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzMzMjkzNzIsInEiOiJIQk0iLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyMzcwMDI4MzQsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.vMlz_FPFAQf9y9MwtOBmMp7G6hPhtRM801_6qSPZiy0&zhida_source=entity)）的访问次数来加快整体运算速度，这种方法又被称为**O-Awareness**。在后文中，我们会详细来看Flash Attention是如何通过**分块计算（tiling）**和**核函数融合（kernel fusion）**来降低对显存的访问。



**（2）Memory Efficicent，节省显存**。在标准attention场景中，forward时我们会计算并保存N*N大小的注意力矩阵；在backward时我们又会读取它做梯度计算，这就给硬件造成了 $O(N^{2})$ 的存储压力。在Flash Attention中，则巧妙避开了这点，使得存储压力降至 $O(N)$ 。在后文中我们会详细看这个trick。



**（3）Exact Attention，精准注意力。**在（1）中我们说过，之前的办法会采用类似于“稀疏attention”的方法做近似。这样虽然能减少计算量，但算出来的结果并不完全等同于标准attention下的结果。但是Flash Attention却做到了完全等同于标准attention的实现方式，这也是后文我们讲述的要点。



## 二、计算限制与内存限制

在第一部分中我们提过，**Flash Attention一个很重要的改进点是：**由于它发现Transformer的计算瓶颈不在运算能力，而在读写速度上。因此它着手降低了对显存数据的访问次数，这才把整体计算效率提了上来。所**以现在我们要问了：它是怎么知道卡点在读写速度上的？**

为了解答这个问题，我们先来看几个重要概念：

- $\pi$ ：**硬件算力上限**。指的是一个计算平台倾尽全力每秒钟所能完成的浮点运算数。单位是 FLOPS or FLOP/s。
- $\beta$ ：**硬件带宽上限**。指的是一个计算平台倾尽全力每秒所能完成的内存交换量。单位是Byte/s。
- $\pi_{t}$ ：**某个算法所需的总运算量**，单位是FLOPs。下标 $t$ 表示total。
- $\beta_{t}$ ：**某个算法所需的总数据读取存储量，**单位是Byte。下标 $t$ 表示total。



这里再强调一下对FLOPS和FLOPs的解释：

- FLOPS：等同于FLOP/s，表示Floating Point Operations Per Second，即每秒执行的浮点数操作次数，用于衡量硬件计算性能。
- FLOPs：表示Floating Point Operations，表示某个算法的总计算量（即总浮点运算次数），用于衡量一个算法的复杂度。



**我们知道，在执行运算的过程中，时间不仅花在计算本身上，也花在数据读取存储上**，所以现在我们定义

- $T_{cal}$ ：对某个算法而言，计算所耗费的时间，单位为s，下标cal表示calculate。其满足 $T_{cal} =\frac{\pi_{t}}{\pi}$
- $T_{load}$ ：对某个算法而言，读取存储数据所耗费的时间，单位为s。其满足 $T_{load} = \frac{\beta_{t}}{\beta}$

**我们知道，数据在读取的同时，可以计算；在计算的同时也可以读取**，所以我们有：

- $T$ ：对某个算法而言，完成整个计算所耗费的总时间，单位为s。其满足 $T = max(T_{cal}, T_{load})$

**也就是说，最终一个算法运行的总时间，取决于计算时间和数据读取时间中的最大值。**



### 2.1 计算限制

当 $T_{cal} > T_{load}$ 时，算法运行的瓶颈在计算上，我们称这种情况为**计算限制（math-bound）**。此时我们有： $\frac{\pi_{t}}{\pi} > \frac{\beta_{t}}{\beta}$ ，即 $\frac{\pi_{t}}{\beta_{t}} > \frac{\pi}{\beta}$



### 2.2 内存限制

当 $T_{cal} < T_{load}$ 时，算法运行的瓶颈在数据读取上，我们称这种情况为**内存限制（memory-bound）**。此时我们有 $\frac{\pi_{t}}{\pi} <\frac{\beta_{t}}{\beta}$ ，即 $\frac{\pi_{t}}{\beta_{t}} <\frac{\pi}{\beta}$

我们称 $\frac{\pi_{t}}{\beta_{t}}$ 为算法的**计算强度（Operational Intensity）**



### 2.3 Attention计算中的计算与内存限制

本节内容参考自：[回旋托马斯x：FlashAttention:加速计算,节省显存, IO感知的精确注意力](https://zhuanlan.zhihu.com/p/639228219)

有了2.1和2.2的前置知识，**现在我们可以来分析影响Transformer计算效率的因素到底是什么了。我们把目光聚焦到attention矩阵的计算上，其计算复杂度为** $O(N^{2})$ **，是Transformer计算耗时的大头。**

假设我们现在采用的硬件为A100-40GB SXM，同时采用混合精度训练（可理解为训练过程中的计算和存储都是**fp16**形式的，一个元素占用2byte）

$\frac{\pi}{\beta} = \frac{312 * 10^{12}}{1555 * 10^{9}} = 201 FLOPs/Bytes$



假定我们现在有矩阵 $Q, K \in \mathbb{R}^{N*d}$ ，其中 $N$ 为序列长度， $d$ 为embedding dim。现在我们要计算 $S = QK^{T}$ ，则有（**对FLOPs要怎么算不了解的朋友，可以跳到6.1节进行阅读**）：

$\frac{\pi_{t}}{\beta_{t}} = \frac{2N^{2}d}{2Nd + 2Nd + 2N^{2}} = \frac{N^{2}d}{2Nd + N^{2}}$



不同 $N, d$ 取值下的受限类型如下：

![img](../imgs/v2-91bb7f924f2314d1b03a1fcc854629e8_1440w.jpg)

根据这个表格，我们可以来做下总结：

- **计算限制（math-bound）**：大矩阵乘法（N和d都非常大）、通道数很大的卷积运算。相对而言，**读得快，算得慢**。
- **内存限制（memory-bound）**：逐点运算操作。例如：激活函数、dropout、mask、softmax、BN和LN。相对而言，**算得快，读得慢。**

**所以，我们第一部分中所说，“Transformer计算受限于数据读取”也不是绝对的，要综合硬件本身和模型大小来综合判断**。但从表中的结果我们可知，memory-bound的情况还是普遍存在的，所以Flash attention的改进思想在很多场景下依然适用。

在Flash attention中，**计算注意力矩阵时的softmax计算就受到了内存限制，这也是flash attention的重点优化对象**，我们会在下文来详细看这一点。



### 2.4 roof-line模型

其实到2.3为止，我们对计算限制和内存限制的概念已经知道得很清楚了。在这一节中，我们更系统来做一个总结。

一个算法运行的效率是离不开硬件本身的。**我们往往想知道：对于一个运算量为 $\pi_{t}$ ，数据读取存储量为 $\beta_{t}$ 的算法，它在算力上限为 $\pi$ ，带宽上限为 $\beta$ 的硬件上，能达到的最大性能 $P$ (Attanable Performance)是多少？**

这里最大性能 $P$ 指的是当前算法实际运行在硬件上时，每秒最多能达到的计算次数，单位是`FLOP/s`。

**[Roof-line模型](https://zhida.zhihu.com/search?content_id=237002834&content_type=Article&match_order=1&q=Roof-line模型&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzMzMjkzNzIsInEiOiJSb29mLWxpbmXmqKHlnosiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoyMzcwMDI4MzQsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.PUj5a4xhVaw2P7TXPj9ux4wUkb7HneUfZy3C_zxZDuk&zhida_source=entity)**就是为了解答这一问题而提出的，它能直观帮我们看到算法在硬件上能跑得多快，模型见下图。

![img](../imgs/v2-e180cdf9b632e90cf988d23d7af2b0b7_1440w.jpg)

如图，横坐标 $I$ 表示计算强度，满足 $I = \frac{\pi_{t}}{\beta_{t}}$ ；纵坐标 $P$ 表示算法运行在硬件上的性能。**算法的运行性能不会超过硬件本身的计算上限**，所以 $P$ 的最大值取到 $\pi$ 。根据我们之前的分析，当 $I > \frac{\pi}{\beta}$ 时，存在计算限制；当 $I <\frac{\pi}{\beta}$ 时，存在内存限制。



## 三、GPU上的存储与计算

由于Flash attention的优化核心是减少数据读取的时间，而数据读取这块又离不开数据在硬件上的流转过程，所以这里我们简单介绍一些GPU上的存储与计算内容，作为Flash attention的背景知识。



### 3.1 GPU的存储分类

![img](../imgs/v2-6ab0049f478a2adfe336857cf7b7be88_1440w.jpg)

上图是Flash attention论文所绘制的硬件不同的存储类型、存储大小和带宽。一般来说，GPU上的存储分类，可以按照是否在芯片上分为**片上内存(on chip)**和**片下内存(off chip)**。

- **片上内存**：主要用于缓存（cache）及少量特殊存储单元（例如texture），其特点是**“存储空间小，但带宽大”**。对应到上图中，**[SRAM](https://zhida.zhihu.com/search?content_id=237002834&content_type=Article&match_order=1&q=SRAM&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzMzMjkzNzIsInEiOiJTUkFNIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6MjM3MDAyODM0LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.xlV7LLN16au3tUPwBs4pR2NRDcbC_hFpyqRSpDHgpVE&zhida_source=entity)**就属于片上内存，它的存储空间只有20MB，但是带宽可以达到19TB/s。
- **片下内存**：主要用于全局存储（global memory），即我们常说的**显存**，其特点是**“存储空间大，但带宽小”**，对应到上图中，**HBM就属于片下内存（也就是显存）**，它的存储空间有40GB（A100 40GB），但带宽相比于SRAM就小得多，只有1.5TB/s。

当硬件开始计算时，会先从显存（HBM）中把数据加载到片上（SRAM），在片上进行计算，然后将计算结果再写回显存中。**那么这个“片上”具体长什么样，它又是怎么计算数据的呢？**



### 3.2 GPU是如何做计算的

![img](../imgs/v2-860b5b9a88fde84029b7bc351b7215e4_1440w.jpg)

如图，负责GPU计算的一个核心组件叫**SM（[Streaming Multiprocessors](https://zhida.zhihu.com/search?content_id=237002834&content_type=Article&match_order=1&q=Streaming+Multiprocessors&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzMzMjkzNzIsInEiOiJTdHJlYW1pbmcgTXVsdGlwcm9jZXNzb3JzIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6MjM3MDAyODM0LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.EOA8zwA4EH5vmKbJKGbS_fV1kwKe6EGQmjl2I0lHAQ4&zhida_source=entity)，流式多处理器），可以将其理解成GPU的计算单元，一个SM又可以由若干个SMP（SM Partition）组成**，例如图中就由4个SMP组成。SM就好比CPU中的一个核，但不同的是一个CPU核一般运行一个线程，但是一个SM却可以运行多个轻量级线程（由Warp Scheduler控制，一个Warp Scheduler会抓一束线程（32个）放入cuda core（图中绿色小块）中进行计算）。



现在，我们将GPU的计算核心SM及不同层级GPU存储结构综合起来，绘制一张简化图：

![img](../imgs/v2-7510cf5dc5b00560e0c60d8e2ababa77_1440w.jpg)

ref：https://www.nvidia.com/en-us/on-demand/session/gtcspring21-s33322/

- **HBM2**：即是我们的显存。
- **L1缓存/shared memory**：每个SM都有自己的L1缓存，用于存储SM内的数据，被SM内所有的cuda cores共享。SM间不能互相访问彼此的L1。NV Volta架构后，L1和shared memory合并（Volta架构前只有Kepler做过合并），目的是为了进一步降低延迟。合并过后，用户能写代码直接控制的依然是shared memory，同时可控制从L1中分配多少存储给shared memory。**Flash attention中SRAM指的就是L1 cache/shared memory。**
- **L2缓存**：所有SM共享L2缓存。L2缓存不直接由用户代码控制。L1/L2缓存的带宽都要比显存的带宽要大，也就是读写速度更快，但是它们的存储量更小。

**现在我们再理一遍GPU的计算流程：将数据从显存（HBM）加载至on-chip的SRAM中，然后由SM读取并进行计算。计算结果再通过SRAM返回给显存。**

我们知道显存的带宽相比SRAM要小的多，读一次数据是很费时的，但是SRAM存储又太小，装不下太多数据。所以**我们就以SRAM的存储为上限，尽量保证每次加载数据都把SRAM给打满，节省数据读取时间**。



### 3.3 kernel融合

前面说过，由于从显存读一次数据是耗时的，因此**在SRAM存储容许的情况下，能合并的计算我们尽量合并在一起，避免重复从显存读取数据**。

举例来说，我现在要做计算A和计算B。在老方法里，我做完A后得到一个中间结果，写回显存，然后再从显存中把这个结果加载到SRAM，做计算B。但是现在我发现SRAM完全有能力存下我的中间结果，那我就可以把A和B放在一起做了，这样就能节省很多读取时间，我们管这样的操作叫**kernel融合**。

由于篇幅限制，我们无法详细解释**kernel**这个概念，**在这里大家可以粗犷地理解成是“函数”，它包含对线程结构（grid-block-thread）的定义，以及结构中具体计算逻辑的定义。**理解到这一层已不妨碍我们对flash attention的解读了，想要更近一步了解的朋友，推荐阅读这篇（[小小将：CUDA编程入门极简教程](https://zhuanlan.zhihu.com/p/34587739）文章。)）

**kernel融合和尽可能利用起SRAM，以减少数据读取时间，都是flash attention的重要优化点。**在后文对伪代码的解读中我们会看到，分块之后flash attention将矩阵乘法、mask、softmax、dropout操作合并成一个kernel，做到了只读一次和只写回一次，节省了数据读取时间。



好！目前为止所有的背景知识我们都介绍完了，现在我们直入主题，看看flash attention到底是怎么巧妙解决memory-bound问题。



## 四、Forward运作流程

在后文相关的讲解中，我们遵循以下步骤：

**（1）先看Flash Attention做分块计算的整体流程。**

**（2）再看分块的计算细节。**

**（3）最后看Flash Attention是如何通过分块计算控制I/O，进而解决memory-bound的问题，提升整体运算速度。**



### 4.1 标准attention计算

这个大家应该都很熟悉了，假设一共有 $N$ 个token，每个token向量的维度为 $d$ ，则一个标准的attention计算如下图：

![img](../imgs/v2-11d8782784e90bfc908933038d0a78eb_1440w.jpg)

其中， $S = QK^{T}, {P} = softmax(S)$ 。在GPT类的模型中，还需要对 ${P}$ 做mask处理。**为了表达方便，诸如mask、dropout之类的操作，我们都忽略掉，下文也是同理**。



### 4.2 标准Safe softmax

这里我们需要额外强调 ${P} = softmax(S)$ 这一步。正常来说，假设 $S$ 中某一行向量为 $[x_{1}, x_{2}, ..., x_{d}]$ ，该行向量中的某一个元素为 $x_{i}$ ，则对 $S$ 做softmax后，有：

$softmax(x_{i}) = \frac{e^{x_{i}}}{\sum_{j=1}^{d}e^{x_{j}}}$

**而如果 $x_{i}$ 过大，那么在计算softmax的过程中，就可能出现数据上溢的情况**。为了解决这个问题，我们可以采用**safe softmax**方法：

$m(x) = \mathop{max}\limits_{i}x_{i}$

$softmax(x_{i}) = \frac{e^{x_{i}-m(x)}}{\sum_{j=1}^{d}e^{x_{j}-m(x)}}$

下图展示了safe softmax的过程，**这里 $\widetilde{P}, P$ 分别表示做归一化前和做归一化后的结果。**大家记住图中 $m, l$ 表达的含义，在后面的分块（Tiling）计算中，我们会用到这两个概念：

![img](../imgs/v2-238beb6416cf01dee3eefc95a112710b_1440w.jpg)

### 4.3 分块计算整体流程（Tiling）

我们知道Flash Attention的核心优化技术是采用了分块计算（Tiling），那么它是如何分块的？分块后的计算方式和不分块的计算方式又有哪些不同之处呢？

**我们先来了解分块计算的整体流程（帮助大家理解数据块是怎么流转的），然后我们再针对其中的细节做一一讲解。**

![img](../imgs/v2-0f5b256f2edc2889e7a5116b3e2ee28e_1440w.jpg)

（1）首先，将 $Q$ 矩阵切为 $T_{r}$ 块（block），每块的长度为 $B_{r}$ 。用 $Q_{i}$ 来表示切完后的某块矩阵，则 $Q_{i}$ 的维度为 $(B_{r}, d)$ 。不难理解， $Q_{i}$ 中存储着某 $B_{r}$ 个token的query信息。



（2）然后，将 $K^{T}$ 矩阵切为 $T_{c}$ 块，每块的长度为 $B_{c}$ 。用 $K^{T}_{j}$ 表示切完后的某块矩阵，则 $K^{T}_{j}$ 的维度为 $(d, B_{c})$ 。易知 $K^{T}_{j}$ 中存储着某 $B_{c}$ 个token的key信息。



（3）同样，将 $V$ 矩阵也切为 $T_{c}$ 块，每块长度为 $B_{c}$ 。用 $V_{j}$ 表示切完后的某块矩阵，则 $V_{j}$ 的维度为 $(B_{c}, d)$ 。易知 $V_{j}$ 中存储着某 $B_{c}$ 个token的value信息。



（4）理解了上面的定义后，我们就可以开始做**分块的attention计算**了。以上图为例：

- **计算初始attention分数**： $S_{ij} = Q_{i} * K^{T}_{j} = (B_{r}, d) * (d, B_{c}) = (B_{r}, B_{c})$ ，图中的 $S_{ij}$ 表示前 $B_{r}$ 个token和前 $B_{c}$ 个token间的原始相关性分数。



- **Safe softmax + mask + dropout**：对 $S_{ij}$ 做safe softmax、mask和dropout操作，得到 $\widetilde{P}_{ij}$ 。**你可能会有疑惑：前面不是说， $\widetilde{P}_{ij}$ 是归一化前的结果， $P_{ij}$ 是归一化后的结果吗？那么这里是不是应该用 $P_{ij}$ 呢？**这里确实只用算到 $\widetilde{P}_{ij}$ ，在后文对分块计算细节的讲解中，我们会详细说这点。目前为止，大家不用太纠结符号，只用大体知道 $P$ 代表的含义即可。



- **计算output**： $O_{ij} = \widetilde{P}_{ij} * V_{j} = (B_{r}, B_{c}) * (B_{c}, d) = (B_{r}, d)$ ，即可得到输出结果 $O_{ij}$ 。**细心的你肯定又发现了，这个等式不太对劲，这个 $O_{ij}$ 不太对劲。**想一想，在正常情况下，前 $B_{r}$ 个token过attention后的输出结果，应该是它和所有token都做注意力计算后的输出结果。可是这里， $O_{ij}$ 却只是前 $B_{r}$ 个token和前 $B_{c}$ 个token的结果。虽然 $O_{ij}$ 的shape对了，但其中的内容却不是我们最终想要的。所以，关于 $O$ 的计算，也是我们需要关注的细节，我们同样放在后文详说。



**在计算这些分块时，GPU是可以做并行计算的，这也提升了计算效率。**



好！现在你已经知道了单块的计算方式，现在让我们把整个流程流转起来把。在上图中，我们注明了 $j$ 是外循环， $i$ 是内循环，这个意思就是说，**对于每个 $j$ ，我们都把所有的 $i$ 遍历一遍，得到相关结果。在论文里，又称为K，V是外循环，Q是内循环。**写成代码就是:



```python3
# ---------------------
# Tc: K和V的分块数
# Tr: Q的分块数量
# ---------------------
for 1 <= j <= Tc:
    for 1 <= i <= Tr:
        do....
```



如果你还有疑惑，那么下面两张图可以更直观地解答你的疑惑.

$j = 0$ ，遍历 $i$ :

![img](../imgs/v2-f6f2c08da5b7eacd1b19b8d98e6ffb0f_1440w.jpg)

$j = 1$ ，遍历 $i$ :

![img](../imgs/v2-d37ba1cb5f65d6656a8cc731359bf40b_1440w.jpg)

**【⚠️特别提醒】：正如上文所说，这里的 $O$ 还需要经过一定的处理，才能和不分块场景下的 $O$ 完全等价。这里我们将每一块的 $O$ 单独画出，是为了帮助大家更好理解分块计算的整体流程，不代表它是最终的输出结果。**



好！到这一步为止，我们已经掌握了使用Tiling计算attention的整体框架。但我们依然有很多细节问题没有解决：

- **分块后，要如何正确计算attention score？（即**$S, P$**的计算方法）**
- **分块后，要如何正确计算输出**$O$**？**
- **分块后，是如何实现优化I/O，解决memory-bound的问题的？**



### 4.4 分块计算中的safe softmax

回顾之前绘制的标准safe softmax流程图，我们知道 $m, l$ 都是针对**完整的一行**做rowmax、rowsum后的结果，那么在分块场景下，会变成什么样呢？

![img](../imgs/v2-52966650e1ccd42a2aacdb246e69f537_1440w.jpg)

以上图红圈内的数据为例，在标准场景下，我们是对红圈内的每一行做rowmax、rowsum后得到 $\widetilde{P}$ 的。

现在切换到分块场景，我们分别算出了 $S_{00}$ 和 $S_{01}$ ，然后我们再对它们分别做rowmax、rowsum，是不是也能得到和标准场景下一模一样的结果呢？

答案当然是否定的。举个简单的例子，**标准场景下的 $m(x)$ 是每行的全局最大值，可是分块后如果你也这么算，它就变成了局部最大值了。**很明显，它不等同于标准场景下的结果。



所以，**Flash Attention的作者们，在这里使用了一种巧妙的计算方式。**

（1）我们假设标准场景下， $S$ 矩阵某一行的向量为 $x = [x_{1}, x_{2}, ..., x_{d}]$ ，因为分块的原因，它被我们切成了两部分 $x = [x^{(1)}, x^{(2)}]$ 。



（2）我们定义：

- $m(x)$ ：标准场景下，该行的全局最大值
- $m(x^{(1)})$ ：分块1的全局最大值
- $m(x^{(2)})$ ：分块2的全局最大值

那么易知： $m(x) = m([x^{(1)}, x^{(2)}]) = max(m(x^{(1)}), m(x^{(2)}))$



（3）我们定义：

- $f(x)$ ：标准场景下， $exp(x - m(x))$ 的结果
- $f(x^{(1)})$ ：分块场景下， $exp(x^{(1)} - m(x^{(1)}))$ 的结果
- $f(x^{(2)})$ ：分块场景下， $exp(x^{(2)} - m(x^{(2)}))$ 的结果

那么易知： $f(x) = [e^{(m(x^{(1)}) - m(x))}f(x^{(1)}), e^{(m(x^{(2)}) - m(x))}f(x^{(2)})]$ 。这个很好理解，详细的证明过程就不写了。



（4）我们定义：

- $l(x)$ ：标准场景下， $rowsum[f(x)]$ 的结果
- $l(x^{(1)})$ ：分块场景下， $rowsum[f(x^{(1)})]$ 的结果
- $l(x^{(2)})$ ：分块场景下， $rowsum[f(x^{(2)})]$ 的结果

那么由（3）易知： $l(x) = e^{m(x^{(1)}) - m(x)}l(x^{(1)}) + e^{m(x^{(2)}) - m(x)}l(x^{(2)})$



（5）现在，我们就可以用分块计算的结果，来表示标准场景下safe softmax的结果了：

$softmax(x) = \frac{f(x)}{l(x)} = \frac{[e^{(m(x^{(1)}) - m(x))}f(x^{(1)}), e^{(m(x^{(2)}) - m(x))}f(x^{(2)})]}{e^{m(x^{(1)}) - m(x)}l(x^{(1)}) + e^{m(x^{(2)}) - m(x)}l(x^{(2)})}$

我们配合上面的图例和flash attention论文中的伪代码，再来进一步理解一下分块计算safe softmax的（1）～（5）步骤。

**这里我们需注意：由于safe softmax是针对矩阵整行的计算，即相当于固定内圈 $i$ ，移动外圈 $j$ 的结果，所以在接下来的介绍中，我们都以这样的视角进行介绍。**

![img](../imgs/v2-7d576eafb486e7561058e596bb5b79c5_1440w.jpg)

我们用 $S_{00}$ （图中浅绿色方块）替换掉（1）～（5）步骤中的 $x^{(1)}$ ，用 $S_{01}$ （图中深绿色方块）替换掉 $x^{(2)}$ 。我们关注点在伪代码部分的5-11行。



由于伪代码中的表达符太多，容易阻碍大家的理解，因此我们先明确各个数学符号表达的含义：

- $S_{ij}$ ：对应在我们的例子里，就是 $S_{00}$ 和 $S_{01}$ ，即 $Q_{i}K^{T}_{j}$ 的结果
- $\widetilde{m}_{ij}$ ：对于当前分块 $S_{ij}$ 来说，每行的局部最大值。相当于前面步骤（2）中对 $m(x^{(1)}), m(x^{(2)})$ 的定义。
- $\widetilde{P}_{ij}$ ：分块场景下，各块的P矩阵（归一化前）结果。相当于步骤（3）中对 $f(x^{(1)})，f(x^{(2)})$ 的定义。
- $\widetilde{l_{ij}}$ ：分块场景下，rowsum的结果。相当于步骤（4）中对 $l(x^{(1)})，l(x^{(2)})$ 的定义。
- $m$ ：标准场景下，对 $S$ 矩阵而言，每行的最大值，这是全局最大值（ $m$ 首次定义在伪代码第2行），相当于前面步骤（2）中对 $m(x)$ 的定义
- $l$ ：标准场景下，全局rowsum的结果（$l$首次定义在伪代码第2行），相当于前面步骤（4）中对 $l(x)$ 的定义。
- $m_{i}$ ：表示 $max(\widetilde{m}_{i0}, \widetilde{m}_{i1}, ..., \widetilde{m}_{i(j-1)})$ 。如果当前分块是 $S_{ij}$ ，则 $m_{i}$ 表示固定 $i$ 时，前 $j-1$ 个分块中的局部最大值。容易推知，当固定 $i$ ，遍历完 $j$ 后， $m_{i}$ 的结果就是全局最大值了。例如图例中，我们遍历完 $S_{00}, S_{01}$ 后，就能得到全局最大值 $m_{0}$ 。
- $m^{new}_{i}$ ：表示 $max(\widetilde{m}_{i0}, \widetilde{m}_{i1}, ..., \widetilde{m}_{i(j-1)}, \widetilde{m}_{ij})$ 。如果当前分块是 $S_{ij}$ ，则 $m^{new}_{i}$ 表示固定 $i$ 时，截止到当前分块为止的局部最大值。
- $l^{new}_{i}$ ：和 $m^{new}_{i}$ 对应，相当于步骤（4）中用分块更新 $l(x)$ 的步骤。
- $l_{i}$ ：和 $m_{i}$ 同理，**即当我们将 $j$ 遍历完后，我们就能得到针对 $i$ 的全局rowmax和全局rowsum**。而根据前面的定义， $m^{new}_{i}$ 和 $l^{new}_{i}$ 是遍历完最新的 $S_{ij}$ 后得到的rowmax和rowsum结果，所以每遍历完一块 $S_{ij}$ ，我们就执行伪代码的第13行，做一次更新。



**如果你被论文中这些数学符号乱花了眼，那再告诉大家一个理解它们的trick**：

- **所有以 $ij$ 作为下标的，都表示当前分块的计算结果**
- **所有以 $i$ 作为下标的，都表示截止到前一个分块（包含前一个分块）的计算结果**
- **所有以 $new$ 为上标的，都表示引入当前分块做更新后的结果**
- **所有没有下标的，都表示全局结果**

![img](../imgs/v2-2771ebc07d1312e5c0921d6c16d79314_1440w.jpg)

相信通过上面对数学表发符的介绍，大家已经大致理解了分块计算safe softmax的过程，为了加深理解，现在我们再来读一遍伪代码，把整个流程串起来：

- `伪代码第5～7行`：从HBM（显存）上读取 $K_{j}, V_{j}$ 到on-chip存储SRAM。注意，在代码处理逻辑上，这里是固定外圈 $j$ ，循环内圈 $i$ 。但是由于整个safe softmax逻辑是对“行”而言的，所以在理解时大家需要想像成固定内圈 $i$ ，循环外圈 $j$ ，也就是我们图例中绘制的深浅绿/蓝/黄色块。



- `伪代码第8行`：从HBM（显存）上读取 $Q_{i}, O_{i}, l_{i}, m_{i}$ 。**记住我们之前说的trick，下标带 $i$ 的都表示截止到前一个分块的计算结果。**虽然我们前面没介绍过 $O_{i}$ （在后文会细说），但按这个trick你应该也能猜到， $O_{i}$ 也是随着分块的移动而逐步更新的。等移动到最后一个分块时，我们就能得到和标准场景下一模一样的输出结果 $O_{i}$ 。在之前的图例中，为了方便大家对分块的整体流程有快速理解，我们画了很多个 $O$ 出来，**现在你应该能猜到，对每个 $i$ ，我们只维持并不断更新一个**$O_{i}$**，直至遍历完毕（例如之前的图例中，我们画了6个 $O$ ，但实际我们要维护更新的，只有3个： $O_{0}, O_{1}, O_{2}$ ）**



- `伪代码第9行`：正常计算 $S_{ij} = Q_{i}K^{T}_{j}$



- `伪代码第10行`：基于当前分块 $S_{ij}$ 计算 $\widetilde{m}_{ij}, \widetilde{P}_{ij}, \widetilde{l_{ij}}$ 。



- `伪代码第11行`：引入当前分块，计算截止目前为止的rowmax和rowsum，分别用 $m^{new}_{i}, l^{new}_{i}$ 表示。



- `伪代码第12行`：更新 $O_{i}$ ，后文会详细解析这部分公式



- `伪代码第13行`：用 $m^{new}_{i}, l^{new}_{i}$ 去更新 $m_{i}, l_{i}$



讲完了分块safe softmax的伪代码，这时你可能发现一个问题了：**之前你是否一直以为，在这一顿操作后，分块计算得出的 $S, \widetilde{P}$ 应该要和标准场景下的完全一致（比如应该是我们步骤（1）~（5）介绍的那样）？但是现在看来，每个分块** $S_{ij}, \widetilde{P}_{ij}$ **依然是用自己局部的rowmax和rowsum做计算的，并没有达到我们理想中的效果呀！**



别急，还记得伪代码第12行我们说的更新 $O_{i}$ 的公式么？**分块计算的真正意义不在于得到正确的 $S, \widetilde{P}$ ，而在于得到正确的 $O$ 。**



然后，你再来看伪代码5-13行，你会发现，在整个计算过程中，只有 $m_{i}, l_{i}, O_{i}$ 被从on-chip的SRAM中写回到显存（HBM）中。**把 $i$ 都遍历完后，读写量也不过是 $m, l, O$ 。相比于标准场景下，我们要读写的是 $S, P, O$ ，读写量是不是一下就少很多，这不就能解决memory-bound的问题了吗。**



所以，**分块计算safe softmax的意义，就是抹去对** $S,P$ **的读写。**



### 4.5 分块计算中的输出O

终于到翘首以盼的输出$O$的分析部分了，当你第一次看到伪代码12行更新$O_{i}$的公式，是不是觉得两眼一黑？不要紧，这里我们依然通过图解的方式，帮助大家理解并推导这个公式。

![img](../imgs/v2-494b855fe59891bf264c31ef7dae6100_1440w.jpg)

之前我们说过，**上图中画的6个 $O$ 并不是我们最终想要的结果。**我们期望维护并更新 $O_{i}$ ，当该 $i$ 下的所有 $j$ 遍历完毕后，我们的 $O_{i}$ 就应该和标准场景下的 $O_{i}$ 完全相等。



回到图例中，图中的 $O_{i}$ 就应该等于被红框圈起来的 $S,P$ 部分和 $V$ 部分的乘积。但是别忘记之前说过，**这里各块** $S, P$ **都是局部rowmax，rowsum计算出来的结果。**所以我们必须对各块 $S, P$ 再做一些处理，才能让它们和V相乘，更新 $O_{i}$ 。



那么要处理到什么程度为止呢？**第一想法可能是，只要让每块 $S,P$ 结果和标准场景下的结果完全一致，不就行了吗？但是别忘了，你不计算到最后一块 $S,P$ ，你是拿不到全局的rowmax和rowsum的。**而由于为了解决memory-bound的问题，我们只保留 $m,l,O$ 而不存各块 $S,P$ 。因此等你遍历到最后一块时，虽然有了全局的rowmax和rowsum，但没有 $S, P$ ，你根本算不出最终的 $O_{i}$ 。



所以这里我们**换个思路**： $O_{i}$ 不是每遍历一块就更新一次吗？那有没有一种办法，****不断用当前最新的rowmax和rowsum去更新** $O_{i}$ **，直到遍历完最后一块，这时的 $O_{i}$ 不就和标准场景下的结果完全一致了吗？也就是我们想构造形如下面这样的更新等式：****

$O_{i} = O_{i} + 当前最新结果$



沿着这个思路，我们来看伪代码第12行公式的诞生过程：

$\begin{aligned} O^{(j+1)}_{i}&= P_{i,:j+1}V_{:j+1}\\ &= softmax(S_{i,:j+1})V_{:j+1}\\ &= diag(l^{(j+1)})^{-1}[exp([S_{i,:j}, S_{i(j+1)}]-m^{(j+1)})]\begin{bmatrix} V_{:j}\\V_{j+1} \end{bmatrix}\\ &= diag(l^{(j+1)})^{-1}[exp(S_{i,:j}-m^{(j+1)})V_{:j} + exp(S_{i(j+1)}-m^{(j+1)})V_{j+1})]\\ &= diag(l^{(j+1)})^{-1}[e^{-m^{(j+1)}}exp(S_{i,:j})V_{:j} + e^{-m^{(j+1)}}exp(S_{i(j+1)})V_{j+1})]\\ &= diag(l^{(j+1)})^{-1}[diag(l^{(j)})e^{m^{(j)}-m^{(j+1)}}diag(l^{(j)})^{-1}exp(S_{i,:j}-m^{(j)})V_{:j} + e^{-m^{(j+1)}}exp(S_{i(j+1)})V_{j+1})]\\ &= diag(l^{(j+1)})^{-1}[diag(l^{(j)})e^{m^{(j)}-m^{(j+1)}}{P}_{i,:j}V_{:j} + e^{-m^{(j+1)}}exp(S_{i(j+1)})V_{j+1})]\\ &= diag(l^{(j+1)})^{-1}[diag(l^{(j)})e^{m^{(j)}-m^{(j+1)}}O^{(j)}_{i} + e^{\widetilde{m}-m^{(j+1)}}exp(S_{i(j+1)}-\widetilde{m})V_{j+1}]\\ &= diag(l^{(j+1)})^{-1}[diag(l^{(j)})e^{m^{(j)}-m^{(j+1)}}O^{(j)}_{i} + e^{\widetilde{m}-m^{(j+1)}}\widetilde{P}_{i(j+1)}V_{j+1}] \end{aligned}$

初次看到这个推导过程，你可能有些懵圈，不要紧，我们一行一行来看。在讲解之前，我们先明确以上推导过程中符号**上下标**的含义：

- $i$ ：这个大家应该很熟悉了。例如图例中， $i=0,1,2$ 分别对应着深浅绿、深浅蓝、深浅黄块。
- $i(j+1)$ ：表示**当前分块**的相关结果
- $i,:j+1$ ：表示**截止到当前分块（包含当前分块）**的相关结果。 $i, :j$ 表示**截止到前一分块（包含前一分块）**的相关结果。



（1）第一行：**首先，我们期望的结果是，每遍历一个分块，就更新一次** $O_{i}$ **，遍历完全部的分块后，我们就能得到和标准场景下完全一致的** $O_{i}$ 。基于此我们有 $O^{(j+1)}_{i} = P_{i,:j+1}V_{:j+1}$ 。其中， $P_{i,:j+1}$ 表示从第0个分块到当前分块，我们用**当前最新**的rowmax，rowsum更新一次**所有分块**的 $P$ 结果（因为做过归一化了，所以是不带波浪号的 $P$ ）。 $V_{:j+1}$ 则表示当前分块及之前所有分块所对应着的 $V$ 部分（例如图例中，若当前分块是浅绿色块，则其对应着浅灰色 $V$ ；若当前分块是深绿色块，则其对应着浅灰色+深灰色 $V$ ）。



（2）第二行：将 $P_{i,:j+1}$ 改写成 $softmax(S_{i, :j+1})$ 的形式。**特别注意，这里 $S_{i,:j+1}$ 所代表的各个分块间都是相互独立的**，你可以理解为，只有在做 $softmax$ 这个操作时，才考虑对这些独立的 $S$ 用最新的rowmax，rowsum去更新 $P$ 。



（3）第三行：就是把(2)当中的 $softmax$ 展开写了。即用当前最新的rowmax和rowsum去计算 $P$ 。这里将 $S_{i,:j+1}$ 拆成 $[S_{i,:j}, S_{i(j+1)}]$ 两部分（**[之前所有的分块，当前分块]**）。同理拆 $V$ 。



（4）～（5）第四～五行：做简单的变式，不再赘述。



（6）第六行：我们观察到，中括号式子里的前半部分，和之前所有分块的结果密切相关。**联想到我们最终的目标是不断更新** $O_{i}$ **，也就是在上一个** $O_{i}$ **的基础上，引入当前分块的信息做更新。**因此，能不能把上一个 $O_{i}$ （对应到我们的式子里就是 $O^{(j)}_{i}$ ）表达出来呢？

基于这个思想做递推， $O^{(j)}_{i}$ 当然就是**之前的所有分块**，用**上一分块**的rowmax、rowsum做更新后求得 $P$ ，再乘上对应的 $V$ 得到的结果呀，所以根据此我们攒出了 $diag(l^{(j)})^{-1}exp(S_{i,:j}-m^{(j)})V_{:j}$ 这一项（就是 $O^{(j)}_{i}$ ），然后再用 $diag(l^{(j)})e^{m^{(j)}-m^{(j+1)}}$ 去抵消我们在攒它的过程中引入的项。



(7)~(9)：第七～九行：明确了（6）以后，剩下的部分就很好理解啦。这里额外说下，为什么要把 $\widetilde{m}$ 放进去呢（毕竟有了 $S_{i(j+1)}, m^{(j+1)}$ 都是已知的，已经可以算了）。因为我们在求解rowsum相关的数据时，还是要把数据从 $S$ 转为 $\widetilde{P}$ 才能求，因此避不开算 $\widetilde{P}$ 。另外也是为了让表达起来更统一，因此这里引入 $\widetilde{m}$ ，进而引入 $\widetilde{P}$ 进行计算。



现在再回头看伪代码的第12行，是不是就很清楚了呢？**建议大家可以自行画图，动手推导，加深理解。**



## 五、Backward运作流程



### 5.1 softmax求导

在后文对分块计算backward中，我们会频繁接触到和softmax求导相关的知识，繁杂的数学符号可能会使很多朋友看得蒙圈，所以这里我们做个快速复习。

设

$\left\{\begin{matrix} \begin{aligned} y &= softmax(z)\\ L &= f(y) \end{aligned} \end{matrix}\right.$

其中， $L$ 表示Loss， $f(.)$ 表示Loss函数， $y = \begin{bmatrix} y_{1}&y_{2}&y_{3} \end{bmatrix}$ ， $z = \begin{bmatrix} z_{1}&z_{2}&z_{3} \end{bmatrix}$ ，若现在我们想求 $\frac{\partial L}{\partial z_{j}}$ ，要怎么算呢？

根据链式法则，我们有 $\frac{\partial L}{\partial z_{j}} = \frac{\partial L}{\partial y}\frac{\partial y}{\partial z_{j}}$ ，所以我们分别来看这两项。



（1） $\frac{\partial L}{\partial y}$

我们现在不考虑具体的Loss函数，直接假设这一项的结果为 $\begin{bmatrix} m_{1}&m_{2}&m_{3} \end{bmatrix}$



（2） $\frac{\partial y}{\partial z_{j}}$

我们知道，对于某个 $z_{j}$ 来说，在softmax的操作下，它参与了 $y_{1}, y_{2}, y_{3}$ 三者的计算，因此它的偏导也和这三者密切相关，这里我们分成两种情况：

$\left\{\begin{matrix} \begin{aligned} \frac{\partial y_{i}}{\partial z_{j}} &= y_{i}(1-y_{i})，当i=j\\ \frac{\partial y_{i}}{\partial z_{j}} &= -y_{i}y_{j}，\qquad当i\neq j \end{aligned} \end{matrix}\right.$



这里不再赘述详细的推动过程，有需要的朋友可以参考[这篇文章](https://link.zhihu.com/?target=https%3A//www.cnblogs.com/wuliytTaotao/p/10787510.html)。



有了这个理解，我们再来谈谈基于 $y= softmax(z)$ 的Jacobian矩阵 $diag(y) - y^{T}y$ :



$\begin{aligned} diag(y) - y^{T}y &= \begin{bmatrix} y_{1}&0&0 \\ 0&y_{2}&0 \\ 0&0&y_{3} \end{bmatrix}-\begin{bmatrix} y_{1}\\y_{2}\\y_{3} \end{bmatrix}*\begin{bmatrix} y_{1}&y_{2}&y_{3} \end{bmatrix}\\ &=\begin{bmatrix} y_{1}-y_{1}^{2}&-y_{1}y_{2}&-y_{1}y_{3} \\ -y_{2}y_{1}&y_{2}-y_{2}^{2}&-y_{2}y_{3} \\ -y_{3}y_{1}&-y_{3}y_{2}&y_{3}-y_{3}^{2} \end{bmatrix} \end{aligned} $



很容易发现只要把每行/每列相加，就能得到对应 $z$ 的偏导。别着急求和，我们继续往下看。



（3） $\frac{\partial L}{\partial z_{j}} = \frac{\partial L}{\partial y}\frac{\partial y}{\partial z_{j}}$

有了（1）（2）的结果，现在就可以来推导 $\frac{\partial L}{\partial z_{j}}$ ，我们有：

$\frac{\partial L}{\partial z_{j}} = \frac{\partial L}{\partial y}\frac{\partial y}{\partial z_{j}} =\sum_{i=1}^{l}\frac{\partial L}{\partial y_{i}}\frac{\partial y_{i}}{\partial z_{j}} = y_{j}(\mathrm{d}y_{j}-\sum_{j=1}^{l}y_{j}dy_{j}) $



举个例子，若我们现在想求 $\frac{\partial L}{\partial z_{1}}$ ，我们将 $\frac{\partial L}{\partial y} = \begin{bmatrix} m_{1}&m_{2}&m_{3} \end{bmatrix}$ 代入上面公式，则有：

$\frac{\partial L}{\partial z_{1}} = m_{1}(y_{1}-y_{1}^{2}) - m_{2}y_{1}y_{2} - m_{3}y_{1}y_{3}$



现在，针对所有的 $z$ ，我们将 $\frac{\partial L}{\partial z}$ 写成矩阵表达式有：



$\begin{aligned} \frac{\partial L}{\partial z} &=\frac{\partial L}{\partial y}\frac{\partial y}{\partial z} =\mathrm{d}y(diag(y) - y^{T}y)\\ &=\begin{bmatrix} m_{1}&m_{2}&m_{3} \end{bmatrix}(\begin{bmatrix} y_{1}&0&0 \\ 0&y_{2}&0\\ 0&0&y_{3} \end{bmatrix} - \begin{bmatrix} y_{1}\\y_{2}\\y_{3} \end{bmatrix}\begin{bmatrix} y_{1}&y_{2}&y_{3} \end{bmatrix}))\\ &=\begin{bmatrix} m_{1}&m_{2}&m_{3} \end{bmatrix}\begin{bmatrix} y_{1}-y_{1}^{2}&-y_{1}y_{2}&-y_{1}y_{3} \\ -y_{2}y_{1}&y_{2}-y_{2}^{2}&-y_{2}y_{3} \\ -y_{3}y_{1}&-y_{3}y_{2}&y_{3}-y_{3}^{2} \end{bmatrix} \end{aligned}$



**至此，大家记住这两个重要的结论：**

$\begin{aligned} \frac{\partial L}{\partial z} &=\frac{\partial L}{\partial y}\frac{\partial y}{\partial z} =\mathrm{d}y(diag(y) - y^{T}y)\\ \frac{\partial L}{\partial z_{j}} &= y_{j}(\mathrm{d}y_{j}-\sum_{j=1}^{l}y_{j}dy_{j}) \end{aligned}$



### 5.2 标准backward计算

![img](../imgs/v2-36eadc31074e8040db6e53da6c8eecb4_1440w.jpg)

我们先来总结下forward中做的操作，为了表达简便，这里将mask、dropout等零碎操作省去，同时假设$f(.)$是损失函数：

$\begin{matrix} \begin{aligned} S &= QK^{T}\\ P &= softmax(S)\\ O &= PV \\ L & = f(O) \end{aligned} \end{matrix}$



对于标准backward来说，在计算开始时，显存（HBM）上已经存放有 $Q, K, V, O, S, P$ 这些数据。论文中的伪代码已经介绍得非常清楚，大家可以自行阅读，这里就不赘述了。对伪代码第3行求 $dS_{ij}$ 有困惑的朋友，可见上文“softamx求导”部分。



### 5.3 分块backward计算

在讲解backward计算前，我们先来看看经过分块Forward计算后，显存（HBM）上都存了哪些数据：

- $m$ ：全局rowmax
- $l$ ：全局rowsum
- $Q, K, V$ ：等同于标准attention场景下的结果
- $O$ ：等同于标准attention场景下的输出结果 $O$
- $\mathrm{d}O$ ：有了完整的 $O$ ，我们就可以按正常的backward步骤先求出它的梯度，也存放在显存上。然后我们就能按照链式法则，分块地去求别的矩阵的梯度了。



既然有了全局的 $m,l$ ，那么现在对于任意一块 $S_{ij}$ ，我们就能基于$m,l$算出和标准场景下完全一致的 $P_{ij}$ 了。因此，在backward的过程中，flash attention将采用**重计算**的方式，**重新算出 $S_{ij}, P_{ij}$ ，并将它们运用到backward的计算中去，所以在接下来的讲解中，大家就可以把 $S, P$ 理解成完全等同于标准场景下的结果，而不是像分块计算forward中那样的 $S, P$ 。**



**另外需要注意的是，为了简化表达，在接下来的分析中，关于mask、dropout之类的步骤，我们在表述上都略去。**现在让我们来看分块计算backward的伪代码：

![img](../imgs/v2-a8593fdc6bbadc744d4f0571bc0acddb_1440w.jpg)



**（1）求 $V_{j}$ 梯度**

由Forward过程我们知： $O = PV$ ，因此有了 $dO$ 后，我们就可以先来求 $dP$ 和 $dV$ 了。**观察下方的图，我们会发现此时所有的** $P$ **都是不带波浪号的，再强调一下，这是因为经过了重计算，此处** $S, P$ **的结果都等同于标准场景下的结果，而不是forward中所代表的含义。**

![img](../imgs/v2-baebd05e8ddc5652f0df6cbc1f41096a_1440w.jpg)

假设现在 $j=0$ ，那我们要怎么求 $dV_{0}$ 呢？

**我们先来看** $V_{0}$ **都参与了** $O$ **哪些部分的计算，以及是怎么参与的**：由图可知， $P_{00}$ 和 $V_{00}$ 参与了 $O_{0}$ 的计算， $P_{10}$ 和 $V_{00}$ 参与了 $O_{1}$ 的计算， $P_{20}$ 和 $V_{0}$ 参与了 $O_{2}$ 的计算。所以我们有：

$dV_{0} = (P_{00})^{T}dO_{0} + (P_{10})^{T}dO_{1} + (P_{20})^{T}dO_{2}$



进而推知：

$dV_{j} = \sum_{i}(P_{ij})^{T}dO_{i}$



在伪代码11～15行中，做的都是 $S, P$ **重计算**的过程，伪代码的第16行，就是在按这个方法分块计算并累积 $dV_{j}$ 。



**（2）求 $P_{ij}$ 梯度**

![img](../imgs/v2-f4cebe5b186bdd8d0d6e2a9dd543c39a_1440w.jpg)

观察上图，可以发现 $P_{ij}$ 只与 $V_{j}, O_{i}$ 相关，例如 $P_{10}$ 只与 $V_{0}, O_{1}$ 相关。因此我们有：

$dP_{ij} = dO_{i}V_{j}^{T}$

这就是伪代码第17行做的事情。



**（3）求 $S_{ij}$ 梯度**

这一块是令许多人感到迷惑的，我们先来**回顾下“softmax求导”部分让大家记住的一个重要结论：**

$\frac{\partial L}{\partial z} =\frac{\partial L}{\partial y}\frac{\partial y}{\partial z} =\mathrm{d}y(diag(y) - y^{T}y)$



我们假设 $s_{i}, p_{i}, o_{i}$ 分别为矩阵 $S,P,O$ 的某一行（注意这里 $i$ 不是表示第 $i$ 块的意思，是表示第 $i$ 行，所以我们用小写的 $s, p, o$ 表示），那么根据这个结论，我们有:

$\begin{aligned} ds_{i} &= dp_{i}(diag(p_{i}) - p_{i}^{T}p_{i})\\ &= dp_{i}diag(p_{i})-dp_{i}p_{i}^{T}p_{i}\\ &=dp_{i}diag(p_{i})-do_{i}V^{T}p_{i}^{T}p_{i}\\ &= dp_{i}diag(p_{i}) - do_{i}o_{i}^{T}p_{i}\\ &= p_{i}\circ [dp_{i} - rowsum(do_{i}\circ o_{i})] \end{aligned}$



**你可能对这个推导的最后一步有疑惑：为什么要大费周章，将** $ds_{i}$ **改写成这么复杂的形式呢？因为在最后一步之前，我们都是针对“某一行”来求导，而引入最后一步的目的，是为了延展至对“某一块（多行）”的求导，**也就是说针对某一块 $dS_{i}$ （注意这里是大写的 $S$ ， $i$ 的含义也回归至“第几块”），我们有：

$dS_{i} = P_{i}\circ[dP_{i} - rowsum(dO_{i}\circ O_{i})]$



如果实在难以理解推导过程，建议大家可以带一些具体的值进去，就能理解我们为什么要写成这种形式了。进而，我们可以推知：

$dS_{ij} = P_{ij}\circ[dP_{ij} - rowsum(dO_{i}\circ O_{i})]$



这就是伪代码第19～20行做的事情。



**（4）求 $Q_{i}$ 梯度**

![img](../imgs/v2-0a4fb34b242e3c304df306aced63a0bf_1440w.jpg)

到目前为止，我们已经知道 $dS_{ij}$ ，那么现在就可以根据链式法则继续求 $dQ_{i}$ 了。

对照上图，我们把目光聚焦在 $Q_{0}$ 身上，由forward过程可知：

$\begin{matrix} S_{00}&= Q_{0}K_{0}^{T}\\ S_{01} &= Q_{0}K_{1}^{T} \end{matrix}$



因此，针对 $Q_{0}$ ，我们有： $dQ_{0} = dS_{00}K_{0} + dS_{01}K_{1}$



推广到任意 $Q_{i}$ ，我们有： $dQ_{i} = \sum_{j}dS_{ij}K_{j}$



这就是伪代码第21行做的事情。



**（5）求 $K_{j}$ 梯度**

![img](../imgs/v2-8def82318d4c8e162a62bc9e86647765_1440w.jpg)

这一步就很简单啦，**如果你被复杂的分块推导弄懵了脑袋，那不妨再复习一下我们前面提过的trick**：对照上图，取出某一块 $K_{j}$ 。由于我们是从 $dS_{ij}$ 链式推向 $K_{j}$ ，所以这里只要搞明白这块 $K_{j}$ 和哪些 $Q$ 一起计算出了哪些 $S$ 再把相关结果相加即可。

只要看了流程图，就不难得知：某块 $K_{j}$ 和对应的 $Q_{i}$ 共同计算出了对应的 $S_{ij}$ ，因此有：

$dK_{j} = \sum_{i}dS_{ij}^{T}Q_{i}$

**这就是伪代码第22行做的事情。**

好！现在我们就把分块backward的细节讲完了，**当大家感到迷茫时，一定记得画图**；在碰到需要做累加才能计算出梯度的步骤中，画图也可以帮助我们快速理解是按 $i$ 维度还是按 $j$ 维度进行累加。



## 六、计算量和显存需求



### 6.1 矩阵相乘的计算量

我们先来看一个前置知识：**两个矩阵相乘，要怎么统计它们的计算量？**

我们一般用**FLOPs（floating point operations，浮点运算次数）**来表示运算量的大小。对于“两矩阵相乘”这个操作而言，其**运算量 = 乘法运算的次数 + 加法运算的次数。**

来看一个具体例子：

![img](../imgs/v2-3e8b79111e61b85c39fe5d5fb8367e50_1440w.jpg)

两矩阵相乘，**为了获取图中深橘色部分的元素，我们一共需要进行n次乘法运算和n-1次加法运算**。

那么现在结果矩阵中，一共有m*p个橘色方块，则意味着我们需要进行：`m*p*(n + n - 1)`次浮点计算。

再进一步，假设此时在蓝色和绿色的矩阵外，我们还有一个**bias矩阵**，意味着计算单个橘色方块时我们需要进行n次乘法和n-1+1次加法运算，那么此时总计算量为：`m*p*(n+n) = 2mnp`。当然，即使不加这个bias，我们也可以把-1项给忽略，得到相同的结果。

**所以这里我们总结下，假设有两个矩阵A和B，它们的维度分别为(m, n)和(n, p)，则这两矩阵相乘的运算量为`2mnp`。**

一般在矩阵运算中，**乘法运算的时间要高于加法运算的时间，因此有时在统计运算量时，我们只考虑乘法运算的次数，则此时两矩阵相乘的运算量可近似为mnp**



### 6.2 Flash Attention的计算量

有了前置知识，我们就能分析flash attention的计算量了，我们以forward过程为例（为了大家阅读方便，我们再把forward的伪代码放一遍）：

![img](../imgs/v2-7d576eafb486e7561058e596bb5b79c5_1440w-20260310233707485.jpg)

我们知道矩阵相乘运算占据了运算量的大头，因此我们把分析目光集中到所有的矩阵运算上来。



（1）在代码第9行，我们有 $S_{ij} = Q_{i}K_{j}^{T}$ ，其中 $Q_{i}\in\mathbb{R}^{B_{r}*d}, K_{j}^{T} \in \mathbb{R}^{d*B_{c}}$ 。根据前置知识，求 $S_{ij}$ 的计算量为 $O(B_{r}B_{c}d)$ 。



（2）在代码第12行，我们有 $\widetilde{P}_{ij}V_{j}$ ，其中 $\widetilde{P}_{ij} \in \mathbb{R}^{B_{r}*B_{c}}, V_{j} \in \mathbb{R}^{B_{c}*d}$ 。则这里的计算量同样为 $O(B_{r}B_{c}d)$



（3）接下来我们看一共计算了多少次（1）和（2），也就是执行了多少次内循环： $T_{c}T_{r} = \frac{N}{B_{c}}\frac{N}{B_{r}}$



（4）**综合以上三点，flash attention的forward计算量为：** $O(\frac{N^{2}}{B_{c}B_{r}}B_{r}B_{c}d) = O(N^{2}d)$ ，注意，因为计算量是用大O阶表示的，所以这里我们把常数项都省略了。

同理大家可以自行推一下backward中的计算量，在论文里给出的结论是 $O(N^{2})$ ，d远小于N，因此 $d$ 也可以略去不表达。



### 6.3 Flash Attention的显存需求

和标准attention相比，如果不考虑 $O$ 的话，Flash Attention只需要存储 $m,l$ ，其显存需求为 $O(N)$ 。

而标准attention需要存储 $S,P$ ，其显存需求为 $O(N^{2})$ 。



**可以发现相比于标准attention，flash attention明显降低了对显存的需求。**





## 七、IO复杂度

之前我们强调过，flash attention相比于标准attention的最大优势，就是其减少了对显存（HBM）的访问次数，一定程度上解决了memory bound的问题。所以这一节我们就来具体分析这两者对显存的访问次数（同样都是以forward为例，backward部分论文中也有给出相关推导过程，大家可以类比forward自行阅读）。



### 7.1 标准attention的IO复杂度

![img](../imgs/v2-7f0acab1a283b0b250010b7ebde2d211_1440w.jpg)

（1）从HBM中读取 $Q, K \in \mathbb{R}^{N * d}$ ，计算 $S = QK^{T}, S \in \mathbb{R}^{N*N}$ 并将 $S$ 写回HBM。一读一写的IO复杂度为： $O(Nd + N^{2})$ ，在表示大O阶时我们忽略常数项。

（2）从HBM中读取 $S \in \mathbb{R}^{N*N}$ ，同时计算 $P \in \mathbb{R}^{N*N}$ 并将其写回HBM。一读一写的IO复杂度为： $O(N^{2})$

（3）从HBM中读取 $P \in \mathbb{R}^{N*N}, V \in \mathbb{R}^{N*d}$ ，计算 $O=PV, O \in \mathbb{R}^{N*d}$ 并将 $O$ 写回HBM。一读一写的IO复杂度为： $O(Nd + N^{2})$



所以，**总体来说标准attention的IO复杂度为：** $O(Nd + N^{2})$



### 7.2 Flash attention的IO复杂度

（1）我们来看伪代码的第6行，在每个外循环中，我们都会加载 $K, V$ 的block。所有外循环结束后，相当于我们加载了完整的 $K, V \in \mathbb{R}^{N*d}$ ，因此这里的IO复杂度为： $O(Nd)$



（2）再看伪代码第8行，在每个内循环中，我们都加载了部分 $Q, O, m, l$ block，由于 $m, l$ 本身比较小(IO复杂度是 $O(N)$ )，因此我们暂时忽略它们，只考虑 $Q, O$ （原论文也是这么分析的）。固定某个外循环，所有内循环结束后，我们相当于完整遍历了 $Q, O \in \mathbb{R}^{N*d}$ 。同时我们会经历 $T_{c}$ 次外循环。因此这里最终的IO复杂度为： $O(T_{c}Nd)$ 。



（3）将 $O, m, l$ 写回HBM，这里近似后IO复杂度为： $O(Nd)$ 。不过在原论文的分析中并没有考虑写回的复杂度，不过省略一些常数项不会影响我们最终的分析。



所以，**总体来说flash attention的IO复杂度为：**

$O(T_{c}Nd) = O(\frac{N}{B_{c}}Nd) = O(\frac{4Nd}{M}Nd) = O(\frac{N^{2}d^{2}}{M})$

论文中提过，一般d的取值在64～128，M的取值在100KB左右，因此有 $\frac{d^{2}}{M} << 1$ 。**因此可以看出，Flash attention的IO复杂度是要显著小于标准attention的IO复杂度的。**



## 八、实验效果



![img](../imgs/v2-c0b8916e3c66f6d1bdf6cfb375bfecb9_1440w.jpg)

Flash attention的作者将 $N=1024, d = 64, B = 64$ 的GPT2-medium部署在A100 GPU上，来观测采用flash attention前后的模型的计算性能。



我们先看最左侧图表，标准attention下，计算强度 $I = \frac{66.6}{40.3} = 1.6 < 201$ ，说明GPT2在A100上的训练是受到内存限制的。而在采用flash attention后得到了明显改善，runtime也呈现了显著下降。



我们再来看中间的图表，它表示在使用flash attention的前提下，以forward过程为例，每个数据块的大小对HBM读写次数（绿色）和耗时（蓝色）的影响。可以发现，数据块越大，读写次数越少，而随着读写次数的减少，runtime也整体下降了（复习一下，读写复杂度为 $O(T_{c}Nd)$ ，数据块越大意味着 $T_{c}$ 越小）。**但有意思的是，当数据块大小>256后，runtime的下降不明显了，这是因为随着矩阵的变大，计算耗时也更大了，会抹平读写节省下来的时间。**



## 九、参考

1、[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/2205.14135)

2、[https://leimao.github.io/blog/Math-Bound-VS-Memory-Bound-Operations/](https://link.zhihu.com/?target=https%3A//leimao.github.io/blog/Math-Bound-VS-Memory-Bound-Operations/)

3、[回旋托马斯x：FlashAttention:加速计算,节省显存, IO感知的精确注意力](https://zhuanlan.zhihu.com/p/639228219)

4、[紫气东来：NLP（十七）：从 FlashAttention 到 PagedAttention, 如何进一步优化 Attention 性能](https://zhuanlan.zhihu.com/p/638468472)

5、[暧暧内含光：GPU 内存概念浅析](https://zhuanlan.zhihu.com/p/651179378)

6、[kaiyuan：GPU内存(显存)的理解与基本使用](https://zhuanlan.zhihu.com/p/462191421)

7、[小小将：CUDA编程入门极简教程](https://zhuanlan.zhihu.com/p/34587739)

8、[Michael Yuan：Roofline Model与深度学习模型的性能分析](https://zhuanlan.zhihu.com/p/34204282)