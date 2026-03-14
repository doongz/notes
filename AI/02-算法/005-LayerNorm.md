# Transformer学习笔记三：为什么Transformer要用LayerNorm/Batch Normalization & Layer Normalization （批量&层标准化)

https://zhuanlan.zhihu.com/p/456863215

这一篇写Transformer里标准化的方法。在Transformer中，数据过Attention层和FFN层后，都会经过一个[Add & Norm](https://zhida.zhihu.com/search?content_id=189656123&content_type=Article&match_order=1&q=Add+%26amp%3B+Norm&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzM2NjY1MTgsInEiOiJBZGQgXHUwMDI2YW1wOyBOb3JtIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6MTg5NjU2MTIzLCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.50pyQc8APi_R6yhX_0iY83ETxdBfIRbYDze3eQBfc50&zhida_source=entity)处理。其中，Add为[residule block](https://zhida.zhihu.com/search?content_id=189656123&content_type=Article&match_order=1&q=residule+block&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzM2NjY1MTgsInEiOiJyZXNpZHVsZSBibG9jayIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjE4OTY1NjEyMywiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.3n_gJjeJJ_1Ic95vitHTkSeuzWCkcwtLBbL3EcHIPcU&zhida_source=entity)（残差模块），数据在这里进行[residule connection](https://zhida.zhihu.com/search?content_id=189656123&content_type=Article&match_order=1&q=residule+connection&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzM2NjY1MTgsInEiOiJyZXNpZHVsZSBjb25uZWN0aW9uIiwiemhpZGFfc291cmNlIjoiZW50aXR5IiwiY29udGVudF9pZCI6MTg5NjU2MTIzLCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.Fpm8_rs-Bxblr6_YEIACTcUbZ3W58d915AF2wPEdWqI&zhida_source=entity)（残差连接）。而Norm即为Normalization（标准化）模块。**Transformer中采用的是Layer Normalization（层标准化）方式**。常用的标准化方法有Batch Normalization，Layer Normalization，Group Normalization，Instance Normalization等，这篇笔记将在论文研究的基础上，着重聚焦于前两者。笔记内容包括：

一、Batch Normalization

- 1.1 提出背景
  - 1.1.1 ICS所带来的问题
  - 1.1.2 解决ICS的常规方法
- 1.2 BN的实践
  - 1.2.1 思路
  - 1.2.1 训练过程中的BN
  - 1.2.2 测试过程中的BN
- 1.3 BN的优势总结
- 1.4 大反转：著名深度学习方法BN成功的秘密竟不在ICS？

二、Layer Normalization

- 2.1 背景 (为何NLP多用LN，图像多用BN)
- 2.2 思路
- 2.3 训练过程和测试过程中的LN

三、Transformer LN改进方法：Pre-LN

- 3.1 思路和实践方法
- 3.2 实验效果

四、参考

##  一、Batch Normalization

本节1.2-1.3的部分，在借鉴[天雨粟：Batch Normalization原理与实战](https://zhuanlan.zhihu.com/p/34879333)解说的基础上，增加了自己对论文和实操的解读，并附上图解。上面这篇文章写得非常清晰，推荐给大家阅读～

###  1.1 提出背景


Batch Normalization（以下简称BN）的方法最早由[Ioffe&Szegedy](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1502.03167.pdf)在2015年提出，主要用于解决在深度学习中产生的ICS（[Internal Covariate Shift](https://zhida.zhihu.com/search?content_id=189656123&content_type=Article&match_order=1&q=Internal+Covariate+Shift&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzM2NjY1MTgsInEiOiJJbnRlcm5hbCBDb3ZhcmlhdGUgU2hpZnQiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjoxODk2NTYxMjMsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.XJL2UltaMn57HQp9b3l588plhmFwwEzrU8_gBlSZgZs&zhida_source=entity)）的问题。若模型输入层数据分布发生变化，则模型在这波变化数据上的表现将有所波动，输入层分布的变化称为Covariate Shift，解决它的办法就是常说的[Domain Adaptation](https://zhida.zhihu.com/search?content_id=189656123&content_type=Article&match_order=1&q=Domain+Adaptation&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3NzM2NjY1MTgsInEiOiJEb21haW4gQWRhcHRhdGlvbiIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjE4OTY1NjEyMywiY29udGVudF90eXBlIjoiQXJ0aWNsZSIsIm1hdGNoX29yZGVyIjoxLCJ6ZF90b2tlbiI6bnVsbH0.PvZPe1SKLp6DD7cOSIjHCxIyJXi2O3JhNd3lcvRaVVs&zhida_source=entity)。同理，在深度学习中，第L+1层的输入，也可能随着第L层参数的变动，而引起分布的变动。这样每一层在训练时，都要去适应这样的分布变化，使得训练变得困难。这种层间输入分布变动的情况，就是Internal Covariate Shift。而BN提出的初衷就是为了解决这一问题。


$\begin{aligned} Z^{[L]} &= W^{[L]} * A^{[L-1]} + b^{[L]} （线性变化层）\\ A^{[L]} &= g^{[L]}(Z^{[L]})（非线性变化/激活函数层） \end{aligned}$

（ICS：随着梯度下降的进行， $W^{[L]}$ 和 $b{[L]}$ 都会被更新，则 $Z^{[L]}$ 的分布改变，进而影响 $A^{[L]}$ 分布，也就是第L+1层的输出）

###  1.1.1 ICS所带来的问题


**（1）在过激活层的时候，容易陷入激活层的梯度饱和区，降低模型收敛速度。**
这一现象发生在我们对模型使用饱和激活函数(saturated activation function)，例如sigmoid，tanh时。如下图：

![img](../imgs/v2-0dcf1fbcd61ae858859cdc0b475ab875_1440w.jpg)

几种常用的激活函数


可以发现当绝对值越大时，数据落入图中两端的梯度饱和区（saturated regime），造成梯度消失，进而降低模型收敛速度。当数据分布变动非常大时，这样的情况是经常发生的。当然，解决这一问题的办法可以采用非饱和的激活函数，例如ReLu。
**（2）需要采用更低的学习速率，这样同样也降低了模型收敛速度。**
如前所说，由于输入变动大，上层网络需要不断调整去适应下层网络，因此这个时候的学习速率不宜设得过大，因为梯度下降的每一步都不是“确信”的。

### 1.1.2 解决ICS的常规方法


综合前面，在BN提出之前，有几种用于解决ICS的常规办法：

- 采用非饱和激活函数
- 更小的学习速率
- 更细致的参数初始化办法
- 数据白化（whitening）

其中，最后一种办法是在模型的每一层输入上，采用一种线性变化方式（例如PCA），以达到如下效果：

- 使得输入的特征具有相同的均值和方差。例如采用PCA，就让所有特征的分布均值为0，方差为1
- 去除特征之间的相关性。

然而在每一层使用白化，给模型增加了运算量。而小心地调整学习速率或其他参数，又陷入到了超参调整策略的复杂中。因此，BN作为一种更优雅的解决办法被提出了。

###  1.2 BN的实践

### 1.2.1 思路

- 对每一个batch进行操作，使得对于这一个batch中所有的输入数据，它们的每一个特征都是均值为0，方差为1的分布
- 单纯把所有的输入限制为(0,1)分布也是不合理的，这样会降低数据的表达能力（第L层辛苦学到的东西，这里都暴力变成（0,1）分布了）。因此需要再加一个线性变换操作，让数据恢复其表达能力。这个线性变化中的两个参数 $\gamma, \beta$ 是需要模型去学习的。

整个BN的过程可以见下图：

![img](../imgs/v2-bd1fa944470997e03e89a64e9ce2b469_1440w.jpg)

Batch Normalization的过程



上图所示的是2D数据下的BN，而在NLP或图像任务中，我们通常遇到3D或4D的数据，例如：

- 图像中的数据维度：（N, C, H, W)。其中N表示数据量（图数），C表示channel数，H表示高度，W表示宽度。
- NLP中的数据为度：（B, S, E）。其中B表示批量大小，S表示序列长度，E表示序列里每个token的embedding向量维度。

如下图，它们在执行BN时，在图中每一个蓝色的平面上求取 $\mu, \sigma$ (也就是一个batch里同一channel上的所有数据)，同时让模型自己学习 $\gamma, \beta$ 。其中"H,W"表示的是"H*W"，即每一个channel里pixel的数量。为了表达统一，这张图用作NLP任务说明时，可将(N, C, H*W)分别理解成(B, E, S)。

![img](../imgs/v2-6c8e8c02faae9531aab64f7c897cefc3_1440w.jpg)

BN的范围：对蓝色部分求均值和方差

###   1.2.1 训练过程中的BN


配合上面的图例，我们来具体写一下训练中BN的计算方式。
假设一个batch中有m个样本，则在神经网络的某一层中，我们记第i个样本在改层第j个神经元中，经过线性变换后的输出为 $Z^i_j$ ，则BN的过程可以写成（图中的每一个红色方框）：


$\begin{aligned} \mu_j &= \frac{1}{m} \sum_{i=1}^{m} Z^i_j \\ \sigma^2_j &= \frac{1}{m} \sum_{i=1}^{m} (Z^i_j - \mu_j)^2 \\ \tilde{Z_j} &= \gamma_{j}\frac{Z_j - \mu_j}{\sqrt{\sigma^2_j + \epsilon}} + \beta_{j} \end{aligned}$

其中 $\epsilon$ 是为了防止方差为0时产生的计算错误，而 $\gamma_j, \beta_j$ 则是模型学习出来的参数，目的是为了尽量还原数据的表达能力。

###  1.2.2 测试过程中的BN


在训练过程里，我们等一个batch的数据都装满之后，再把数据装入模型，做BN。但是在测试过程中，我们却更希望模型能来一条数据就做一次预测，而不是等到装满一个batch再做预测。也就是说，我们希望测试过程共的数据不依赖batch，每一条数据都有一个唯一预测结果。**这就产生了训练和测试中的gap：测试里的** $\mu, \sigma$ **要怎么算呢？**一般来说有两种方法。


**（1）用训练集中的均值和方差做测试集中均值和方差的无偏估计**


保留训练模型中，**每一组**batch的**每一个**特征在**每一层**的 $\mu_{batch}, \sigma^2_{batch}$ ，这样我们就可以得到测试数据均值和方差的无偏估计：


$\begin{aligned} \mu_{test} &= \mathbb{E}(\mu_{batch}) \\ \sigma^2_{test} &= \frac{m}{m-1}\mathbb{E}(\sigma^2_{batch})\\ BN(X_{test}) &= \gamma \frac{X_{test} - \mu_{test}}{\sqrt{\sigma^2_{test} + \epsilon}} + \beta \end{aligned}$
其中m表示的是批量大小。
这种做法有一个明显的缺点：需要消耗较大的存储空间，保存训练过程中所有的均值和方差结果（每一组，每一个，每一层）。

**（2）Momentum：移动平均法(Moving Average)**


稍微改变一下训练过程中计算均值和方差的办法，设 $\mu_{t}$是当前步骤求出的均值， $\bar \mu$ 是之前的训练步骤累积起来求得的均值（也称running mean），则：
$\bar\mu \gets p\bar\mu + (1-p)\mu^{t}$
其中，p是momentum的超参，表示模型在多大程度上依赖于过去的均值和当前的均值。 $\bar\mu$ 则是新一轮的ruuning mean，也就是当前步骤里最终使用的mean。同理，对于方差，我们也有：
$\bar{\sigma^2} \gets p\bar{\sigma^2} + (1-p){\sigma^2}^{t}$

采用这种方法的好处是：

- 节省了存储空间，不需要保存所有的均值和方差结果，只需要保存running mean和running variance即可
- 方便在训练模型的阶段追踪模型的表现。一般来讲，在模型训练的中途，我们会塞入validation dataset，对模型训练的效果进行追踪。采用移动平均法，不需要等模型训练过程结束再去做无偏估计，我们直接用running mean和running variance就可以在validation上评估模型。

###  1.3 BN的优势总结

- 通过解决ICS的问题，使得每一层神经网络的输入分布稳定，在这个基础上可以使用较大的学习率，加速了模型的训练速度
- 起到一定的正则作用，进而减少了dropout的使用。当我们通过BN规整数据的分布以后，就可以尽量避免一些极端值造成的overfitting的问题
- 使得数据不落入饱和性激活函数（如sigmoid，tanh等）饱和区间，避免梯度消失的问题

###  **1.4 大反转：著名深度学习方法BN成功的秘密竟不在ICS？**


以解决ICS为目的而提出的BN，在各个比较实验中都取得了更优的结果。但是来自MIT的[Santurkar et al. 2019](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1805.11604.pdf)却指出：

- 就算发生了ICS问题，模型的表现也没有更差
- BN对解决ICS问题的能力是有限的
- ***BN奏效的根本原因在于它让optimization landscape更平滑\***

而在这之后的很多论文里也都对这一点进行了不同理论和实验的论证。
（每篇论文的Intro部分开头总有一句话类似于：“BN的奏效至今还是个玄学”。。。）

图中是VGG网络在标准，BN，noisy-BN下的实验结果。其中noisy-BN表示对神经网络的每一层输入，都随机添加来自分布(non-zero mean, non-unit variance)的噪音数据，并且在不同的timestep上，这个分布的mean和variance都在改变。noisy-BN保证了在神经网络的每一层下，输入分布都有严重的ICS问题。但是从试验结果来看，noisy-BN的准确率比标准下的准确率还要更高一些，这说明ICS问题并不是模型效果差的一个绝对原因。

![img](../imgs/v2-6a413e04c09beebaa0bf72dd77e8ffa5_1440w.jpg)



而当用VGG网络训练CIFAR-10数据时，也可以发现，在更深层的网络（例如Layer11）中，在采用BN的情况下，数据分布也没有想象中的“规整”：

![img](../imgs/v2-66d16a7da62b23f809e3276f541178c6_1440w.jpg)



最后，在VGG网络上，对于不同的训练step，计算其在不同batch上loss和gradient的方差（a和b中的阴影部分），同时测量 $\beta-smoothness$ （简单理解为l2-norm表示的在一个梯度下降过程中的最大斜率差）。可以发现BN相较于标准情况都来得更加平滑。

![img](../imgs/v2-0986effe9bd0b8211a2867bde46c7582_1440w.jpg)



##  二、Layer Normalization

###  2.1 背景


BN提出后，被广泛作用在CNN任务上来处理图像，并取得了很好的效果。针对文本任务，[Ba et al. 2016](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1607.06450.pdf) 提出在RNN上使用Layer Normalization（以下简称LN）的方法，用于解决BN无法很好地处理文本数据长度不一的问题。例如采用RNN模型+BN，我们需要对不同数据的同一个位置的token向量计算 $\mu, \sigma^2$ ，在句子长短不一的情况下，容易出现：

- 测试集中出现比训练集更长的数据，由于BN在训练中累积 $\mu_{batch}, \sigma^2_{batch}$ ，在测试中使用累计的经验统计量的原因，导致测试集中多出来的数据没有相应的统计量以供使用。 （**在实际应用中，通常会对语言类的数据设置一个max_len，多裁少pad，这时没有上面所说的这个问题。但这里我们讨论的是理论上的情况，即理论上，诸如Transformer这样的模型，是支持任意长度的输入数据的**）
- 长短不一的情况下，文本中的某些位置没有足够的batch_size的数据，使得计算出来的 $\mu, \sigma^2$ 产生偏差。例如[Shen et al. (2020)](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2003.07845.pdf)就指出，在数据集Cifar-10（模型RestNet20)和IWLST14（模型Transformer）的训练过程中，计算当前epoch所有batch的统计量 $\mu_{B}, \sigma^2_{B}$ 和当前累计（running）统计量 $\mu, \sigma^2$ 的平均Euclidean distance，可以发现文本数据较图像数据的分布差异更大：

![img](../imgs/v2-2c3498a034c43ff734e35fb5fe782902_1440w.jpg)

这是一个结合实验的解释，而引起这个现象的原因，**可能不止是“长短不一”这一个，也可能和数据本身在某一维度分布上的差异性有关（想一下，对不同句子之间的第一个词做BN，求出来的mean和variance几乎是没有意义的）**。目前相关知识水平有限，只能理解到这里，未来如果有更确切的想法，会在这里补充。



###  2.2 思路


整体做法类似于BN，不同的是LN不是在特征间进行标准化操作（横向操作），而是在整条数据间进行标准化操作（纵向操作）。

![img](../imgs/v2-839ecea737782bc8a8af321f2d4f8633_1440w.jpg)

Layer Normalization计算过程



**在图像问题中，LN是指对一整张图片进行标准化处理，即在一张图片所有channel的pixel范围内计算均值和方差。而在NLP的问题中，LN是指在一个句子的一个token的范围内进行标准化。**

![img](../imgs/v2-1c772d9cfebc50ea7bc89c188b15994a_1440w.jpg)

图像数据中的LN计算范围：在蓝色范围内计算统计值

![img](../imgs/v2-6aff36a5399e1b50f5f220e8cb762861_1440w.jpg)

NLP任务中的计算范围

###   2.3 训练过程和测试过程中的LN


LN使得各条数据间在进行标准化的时候相互独立，因此LN在训练和测试过程中是一致的。LN不需要保留训练过程中的 $\mu, \sigma^2$ ，每当来一条数据时，对这条数据的指定范围内单独计算所需统计量即可。

##  三、Transformer LN改进方法：Pre-LN


原始transformer中，采用的是Post-LN，即LN在residule block（图中addtion）之后。[Xiong et al. (2020)](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2002.04745.pdf)中提出了一种更优Pre-LN的架构，即LN在residule block之前，它能和Post-LN达到相同甚至更好的训练结果，同时规避了在训练Post-LN中产生的种种问题。两种架构的具体形式可以见下图。

![img](../imgs/v2-b71299f375bd3e5ec3dd86051b3d2cb8_1440w.jpg)


这篇论文通过理论分析和实验的方式，证明了Pre-LN相比的Post-LN的优势，主要表现在：

- 在learning rate schedular上，Pre-LN不需要采用warm-up策略，而Post-LN必须要使用warm-up策略才可以在数据集上取得较好的Loss和BLEU结果。
- 在收敛速度上，由于Pre-LN不采用warm-up，其一开始的learning rate较Post-LN更高，因此它的收敛速度更快。
- 在超参调整上，warm-up策略带来了两个需要调整的参数： $lr_{max}$ （最大学习率）和 $T_{warmup}$ (warmup过程的总步数）。这两个参数的调整将会影响到模型最终的效果。而由于transformer模型的训练代价是昂贵的，因此多引入超参，也给模型训练带来了一定难度。

> **Quick Tips：**warm-up learning rate，即指在训练初期的一定步数内，缓慢将学习率从0升至 $lr_{max}$ ，超过此步数范围则采用decay learning rate的策略。在大batch数据集的训练中，warm-up learning rate具有较好的表现。

![img](../imgs/v2-0dd8a7ba3d9f469113df19480d0bc604_1440w.jpg)



$lr(t) = \frac{t}{T_{warmup}} lr_{max},t\le T_{warmup}$
其中，t表示当前训练步数， $T_{warmup}$ 表示warm-up过程总步数， $lr_{max}$ 表示learning rate最高点。

总结看来，Pre-LN带来的好处，基本都是因为不需要做warm-up引起的。而引起这一差异的根本原因是：

- Post-LN在输出层的gradient norm较大，且越往下层走，gradient norm呈现下降趋势。这种情况下，在训练初期若采用一个较大的学习率，容易引起模型的震荡。
- Pre-LN在输出层的gradient norm较小，且其不随层数递增或递减而变动，保持稳定。
- 无论使用何种Optimzer，不采用warm-up的Post-LN的效果都不如采用warm-up的情况，也不如Pre-LN。

以三点原因在论文中有详细的理论和实验证明，为了节省篇幅，这里仅贴上实验结果。实验场景为机器翻译，分别在IWSLT(German to English)和WMT(English to German)这两个数据集上进行。w/o warm-up表示without warm-up，w/warm-up表示with warm-up， $lr_{max}$ 在Post-LN中表示warm-up步骤的最高learning rate，在Pre-LN中表示初始化的learning rate。评价指标分别为Loss和BLEU。这个实验结果证明了上述所说的Pre-LN的优势。更细节的实验和内容可以参见论文。

![img](../imgs/v2-3f7ad3676b612432157442c3e1d6eebb_1440w.jpg)

## 四、参考

1. [https://arxiv.org/pdf/1805.11604.pdf](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1805.11604.pdf)
2. [https://arxiv.org/pdf/1502.03167.pdf](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1502.03167.pdf)
3. [https://arxiv.org/pdf/1607.06450.pdf](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1607.06450.pdf)
4. [https://arxiv.org/pdf/2002.04745.pdf](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2002.04745.pdf)
5. [https://arxiv.org/pdf/2003.07845.pdf](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/2003.07845.pdf)
6. [天雨粟：Batch Normalization原理与实战](https://zhuanlan.zhihu.com/p/34879333)