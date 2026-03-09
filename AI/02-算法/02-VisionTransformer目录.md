# Vision Transformer 原理分析+代码解读 (目录)

来源：https://zhuanlan.zhihu.com/p/348593638

## 1 Vision Transformer优秀论文及对应代码介绍

### Section 1：视觉 Transformer 基础

> **1 一切从 Self-attention 开始**
> 1.1 处理 Sequence 数据的模型
> 1.2 Self-attention
> 1.3 Multi-head Self-attention
> 1.4 Positional Encoding
>
> **2 Transformer 的实现和代码解读 (NIPS2017)**
> (来自Google Research, Brain Team)
> 2.1 Transformer 原理分析
> 2.2 Transformer 代码解读
>
> **3 Transformer+Detection：引入视觉领域的首创DETR (ECCV2020)**
> (来自 Facebook AI)
> 3.1 DETR 原理分析
> 3.2 DETR 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (一)3079 赞同 · 168 评论文章](https://zhuanlan.zhihu.com/p/340149804)





### Section 2：视觉 Transformer 进阶

> **4 Transformer+Detection：Deformable DETR：可变形的 Transformer (ICLR2021)**
> (来自商汤代季峰老师组)
> 4.1 Deformable Convolution 原理分析
> 4.2 Deformable Convolution 代码解读
> 4.3 Deformable DETR 原理分析
> 4.4 Deformable DETR 代码解读
>
> **5 Transformer+Classification：用于分类任务的 Transformer** **(ICLR2021)**
> (来自 Google Research, Brain Team)
> 5.1 ViT 原理分析
> 5.2 ViT 代码解读
>
> **6 Transformer+Image Processing：IPT：用于底层视觉任务的 Transformer**
> (来自北京华为诺亚方舟实验室)
> 6.1 IPT 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二)594 赞同 · 57 评论文章](https://zhuanlan.zhihu.com/p/342261872)





### Section 3：Transformer在识别任务的演进 (避免使用巨大的非公开数据集，只使用 ImageNet 训练Transformer)

> **7 Transformer+Distillation：DeiT：高效图像 Transformer**
> (来自 Facebook AI)
> 7.1 DeiT 原理分析
> 7.2 DeiT 代码解读
>
> **8 Transformer Visual Recognition：Visual Transformers：基于 Token 的图像表示和处理**
> (来自 UC Berkeley)
> 8.1 Visual Transformers 原理分析
> 8.2 Visual Transformers 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (三)215 赞同 · 27 评论文章](https://zhuanlan.zhihu.com/p/349315675)





### Section 4：Transformer内部机制的探究

> **9 充分挖掘 patch 内部信息：Transformer in Transformer：TNT**
> (来自北京华为诺亚方舟实验室)
> 9.1 TNT 原理分析
>
> **10 探究位置编码的必要性：Do We Really Need Explicit Position Encodings for Vision Transformers?**
> (来自美团)
> 10.1 CPVT 原理分析
> 10.2 CPVT 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (四)120 赞同 · 9 评论文章](https://zhuanlan.zhihu.com/p/354913120)





### Section 5：轻量化Transformer (1)

> **11 Efficient Transformer：HAT：高效的硬件感知 Transformer**
> (来自 MIT 韩松团队)
> 11.1 HAT 原理分析
>
> **12 Efficient Transformer：Lite-Transformer 远近注意力机制的轻量化 Transformer**
> (来自 MIT 韩松团队)
> 12.1 Lite-Transformer 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (五)58 赞同 · 4 评论文章](https://zhuanlan.zhihu.com/p/348427133)





### Section 6：将卷积融入视觉 Transformer (1)

> **13 CvT: Introducing Convolutions to Vision Transformers**
> (来自麦吉尔大学, 微软云+AI)
> 13.1 CvT 原理分析
>
> **14 CeiT：将卷积设计整合到视觉 Transformers中**
> (来自商汤)
> 14.1 CeiT 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (六)107 赞同 · 13 评论文章](https://zhuanlan.zhihu.com/p/361112935)





### Section 7：轻量化Transformer (2)

> **15 DeFINE：深度矩阵分解给词向量矩阵瘦身 (ICLR 2020)**
> (来自华盛顿大学)
> 15.1 DeFINE 原理分析
>
> **16 DeLighT: Deep and Light-Weight Transformer (ICLR 2021)**
> (来自 Facebook AI)
> 16.1 DELIGHT 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (七)33 赞同 · 1 评论文章](https://zhuanlan.zhihu.com/p/358102861)





### Section 8：更深的视觉 Transformer

> **17 DeepViT: 解决注意力坍塌以构建深层ViT**
> (来自 新加坡国立大学, 字节跳动 AI Lab(美国))
> 17.1 DeepViT 原理分析
>
> **18 CaiT：Going deeper with Image Transformers**
> (来自 Facebook)
> 18.1 CaiT 原理分析
> 18.2 CaiT 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (八)68 赞同 · 4 评论文章](https://zhuanlan.zhihu.com/p/363370678)





### Section 9：更快更小的 Transformer

> **19 LeViT: 用于快速推理的视觉 Transformer**
> (来自 Facebook，DeiT 一作 Hugo Touvron 挂名)
> 19.1 LeViT 原理分析
>
> **20 ViT-Lite: 紧凑型视觉 Transformer，更小更简单**
> (来自俄勒冈大学，UIUC，PAIR)
> 20.1 ViT-Lite 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (九)95 赞同 · 7 评论文章](https://zhuanlan.zhihu.com/p/364710161)





### Section 10：视觉 Transformer 训练方式的演进

> **21 LV-ViT: 56M 参数训练视觉 Transformer**
> (来自新加坡国立大学，字节跳动)
> 21.1 LV-ViT 原理分析
>
> **22 通过抑制过度平滑来改进视觉 Transformer 训练**
> (来自 Facebook)
> 22.1 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十)48 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/367733889)





### **Section 11：轻量化 Transformer (3)**

> **23 Reformer：高效处理长序列的 Transformer (ICLR 2020)**
> (来自 UC Berkeley, Google Research)
> 23.1 Reformer 原理分析
>
> **24 Linformer: 低秩矩阵逼近实现新的 Self-Attention**
> (来自 Facebook AI)
> 24.1 Linformer 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十一)24 赞同 · 3 评论文章](https://zhuanlan.zhihu.com/p/358658459)





### **Section 12：Transformer+图像质量评价**

> **25 IQT：基于 Transformer 的感知图像质量评价**
> (来自LG，NTIRE 2021冠军方案)
> 25.1 IQT 原理分析
> 25.2 IQT 代码解读
>
> **26 Transformer+图像质量评价：TRIP**
> (来自 NORCE Norwegian Research Centre，深圳大学)
> 26.1 TRIP 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十二)37 赞同 · 3 评论文章](https://zhuanlan.zhihu.com/p/369710857)





### **Section 13：Transformer 的精炼和底层视觉任务新探索**

> **27 low-level 多个任务榜首被占领，中科大等联合提出：Uformer**
> (来自中科院，中科大，刘健庄老师团队)
> 27.1 Uformer 原理分析
>
> **28 Refiner：改进视觉Transformer的自注意力**
> (来自新加坡国立大学)
> 28.1 Refiner 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十三)45 赞同 · 5 评论文章](https://zhuanlan.zhihu.com/p/380391088)





### **Section 14：将卷积融入视觉 Transformer (2)**

> **29 FAIR提出：Convolutional stem is all you need! 探究 ViT 优化不稳定的本质原因**
> (来自 FAIR，RossGirshick等巨佬 )
> 29.1 原理分析
>
> **30 谷歌提出 CoAtNet：结合卷积和注意力 89.77% Accuracy！**
> (来自谷歌大脑，Quoc V. Le团队)
> 30.1 CoAtNet 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十四)52 赞同 · 9 评论文章](https://zhuanlan.zhihu.com/p/385106095)





### **Section 15：Transformer 在识别任务的改进**

> **31 T2T-ViT：在 ImageNet 上从头训练视觉 Transformer**
> (来自新加坡国立大学冯佳时团队，依图科技颜水成团队)
> 31.1 T2T-ViT 原理分析
> 31.2 T2T-ViT 代码解读
>
> **32 VOLO 刷新 CV 多项记录，无需额外训练数据，首次在 ImageNet 上达到87.1%**
> (来自新加坡国立大学冯佳时团队，依图科技颜水成团队)
> 32.1 VOLO 原理分析
> 32.2 VOLO 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十五)47 赞同 · 2 评论文章](https://zhuanlan.zhihu.com/p/386955720)







### **Section 16：Vision Transformer + NAS**

> **33 HR-NAS：使用轻量级 Transformer 的高效搜索高分辨率神经架构**
> (来自香港大学、字节跳动和中国人民大学)
> 33.1 HR-NAS 原理分析
>
> **34 AutoFormer：搜索用于视觉识别的 Transformer**
> (来自 微软)
> 34.1 AutoFormer 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十六)19 赞同 · 1 评论文章](https://zhuanlan.zhihu.com/p/393015148)





### **Section 17：Swin Transformer：各项任务SOTA模型 (1)**

> **35 Swin Transformer: 屠榜各大 CV 任务的视觉 Transformer模型**
> (来自 微软亚研院，中科大)
> 35.1 Swin Transformer 原理分析
> 35.2 Swin Transformer 代码解读
>
> **36 SwinIR: 用于图像复原的 Swin Transformer**
> (来自 ETH Zurich)
> 36.1 SwinIR 原理分析
> 36.2 SwinIR 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十七)138 赞同 · 17 评论文章](https://zhuanlan.zhihu.com/p/404001918)





### **Section 18：Attention is not all you need**

> **37 只使用纯粹的注意力机制就够了吗**
> (来自谷歌，EPFL)
> 37.1 Attention is not all you need 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十八)24 赞同 · 2 评论文章](https://zhuanlan.zhihu.com/p/413331094)





### **Section 19：MetaTransformer：简单到尴尬的视觉模型**

> **38 MetaTransformer：简单到尴尬的视觉模型**
> (来自 Sea AI Lab，新加坡国立大学)
> 38.1 MetaTransformer 原理分析
> 38.2 MetaTransformer 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (十八)32 赞同 · 7 评论文章](https://zhuanlan.zhihu.com/p/438755025)





### **Section 20：Swin Transformer：各项任务SOTA模型 (2)**

> **39 Swin Transformer v2: 扩展容量和分辨率**
> (来自 微软亚研院，中科大)
> 39.1 Swin Transformer v2 原理分析
> 39.2 Swin MLP 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十)28 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/436381997)





### **Section 21：Transformer 用于底层视觉任务的探索**

> **40 EDT：用于底层视觉的高效图像处理 Transformer**
> (来自 港中文，思谋科技)
> 40.1 EDT 原理分析
> 40.2 EDT 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十一)20 赞同 · 1 评论文章](https://zhuanlan.zhihu.com/p/448223763)





### **Section 22：Transformer内部机制的探究**

> **41 Pyramid TNT：使用金字塔结构改进的 TNT Baseline**
> (来自北京华为诺亚方舟实验室)
> 40.1 TNT 回顾
> 41.2 Pyramid TNT 原理分析
> 41.3 Pyramid TNT 代码解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十二)13 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/454761367)





### **Section 23：小数据集训练视觉 Transformer 模型**

> **42 仅用2040张图片训练出的视觉 Transformer 模型**
> (来自南京大学)
> 42.1 IDMM 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十三)22 赞同 · 2 评论文章](https://zhuanlan.zhihu.com/p/463566190)





### **Section 24：极深的 Transformer 模型**

> **43 解决 Transformer 训练难题，1000层 Transformer 也能稳定训练**
> (来自微软亚洲研究院)
> 43.1 DeepNet 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十四)22 赞同 · 5 评论文章](https://zhuanlan.zhihu.com/p/474883699)





### **Section 25：面向 TensorRT 的视觉 Transformer**

> **44 面向 TensorRT 的视觉 Transformer**
> (来自字节跳动)
> 44.1 TRT-ViT 原理分析

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十五)24 赞同 · 1 评论文章](https://zhuanlan.zhihu.com/p/512714683)





### **Section 26：关于视觉 Transformer 你应该知道的3件事**

> **45 关于视觉 Transformer 你应该知道的3件事**
> (来自 Meta AI，DeiT 一作团队)
> 45.1 论文解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十六)15 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/525659537)





### **Section 27：视觉 Transformer 的复仇：DeiT III**

> **46 视觉 Transformer 的复仇：DeiT III**
> (来自 Meta AI，DeiT 一作团队)
> 46.1 论文解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十七)11 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/542208714)





### **Section 28：TinyViT：小型 ViT 的快速预训练蒸馏**

> **47 TinyViT：小型 ViT 的快速预训练蒸馏**
> (来自微软)
> 47.1 TinyViT 论文解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十八)14 赞同 · 2 评论文章](https://zhuanlan.zhihu.com/p/543743516)





### **Section 29：MiniViT：通过权重复用压缩视觉 Transformer 模型**

> **48 MiniViT：通过权重复用压缩视觉 Transformer 模型**
> (来自微软)
> 48.1 MiniViT 论文解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (二十九)14 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/548187887)





### **Section 30：无需微调加速大规模视觉 Transformer 密集预测任务的方法**

> **49 无需微调加速大规模视觉 Transformer 密集预测任务的方法**
> (来自微软亚洲研究院)
> 49.1 论文解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (三十)11 赞同 · 1 评论文章](https://zhuanlan.zhihu.com/p/570552091)





### **Section 31：动态 Token 稀疏化实现高效的视觉 Transformer**

> **50 DynamicViT：动态 Token 稀疏化实现高效的视觉 Transformer**
> (来自清华大学，周杰，鲁继文团队，UCLA)
> 50.1 DynamicViT 论文解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (三十一)15 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/567991402)





### **Section 32：动态 Token 稀疏化实现高效的视觉 Transformer**

> **51 无需训练，Token 合并打造更快的 ViT 架构**
> (来自佐治亚理工学院，Meta AI)
> 51.1 ToMe 论文解读

**link：**

[科技猛兽：Vision Transformer 超详细解读 (原理分析+代码解读) (三十二)19 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/571109108)





### **Section 33：基础 Transformer**

> **52 MAGNETO：基础 Transformer**
> (来自微软)
> 52.1 MAGNETO 论文解读

**link：**

To be continued.

## 2 Vision Transformer优秀开源工作介绍

> **1 用 Pytorch 轻松实现28个 vision Transformer，开源库 timm 了解一下**
> (来自 Ross Wightman)

**link：**

[科技猛兽：视觉Transformer优秀开源工作：timm库vision transformer代码解读382 赞同 · 17 评论文章](https://zhuanlan.zhihu.com/p/350837279)





> **2 视觉神经网络模型优秀开源工作：timm 库使用方法和代码解读**
> (来自 Ross Wightman)

**link：**

[科技猛兽：视觉神经网络模型优秀开源工作：timm库使用方法和代码解读252 赞同 · 19 评论文章](https://zhuanlan.zhihu.com/p/404107277)





## 3 通用 Vision Backbone 优秀论文及对应代码介绍

> (每篇文章对应一个 Section，目录持续更新。)

### **Section 1：视觉 MLP 首创：MLP-Mixer**

> **1 MLP-Mixer: An all-MLP Architecture for Vision**
> (来自 Google Research, Brain Team，ViT 作者团队)
> 1.1 MLP-Mixer 原理分析
> 1.1.1 仅仅靠着 MLP 就真的无法解决复杂数据集的分类任务吗？
> 1.1.2 MLP-Mixer 是如何处理输入图片的？
> 1.1.3 MLP-Mixer 与之前 Conv1×1 的不同之处在哪里？
> 1.1.4 MLP-Mixer 架构
> 1.1.5 MLP-Mixer 实验
> 1.2 MLP-Mixer 代码解读
>
> **2 RepMLP：卷积重参数化为全连接层进行图像识别**
> (来自清华大学，旷视，RepVGG 作者团队)
> 2.1 RepMLP 原理分析
> 2.1.1 深度学习模型的几个性质
> 2.1.2 RepMLP 模块
> 2.1.3 如何将卷积等效成 FC 层？
>
> **3 ResMLP：ImageNet 数据集训练残差 MLP 网络**
> (来自 Facebook AI，索邦大学)
> 3.1 ResMLP 原理分析
> 3.2 ResMLP 代码解读

**link：**

[科技猛兽：Vision MLP超详细解读 (原理分析+代码解读) (一)101 赞同 · 20 评论文章](https://zhuanlan.zhihu.com/p/369970953)





### **Section 2：视觉 MLP 进阶方法**

> **4 谷歌大脑提出 gMLP：请多多关注 MLP**
> (来自谷歌大脑，Quoc V .Le 团队)
> 4.1 gMLP 原理分析
>
> **5 港大提出 CycleMLP：用于密集预测的类似 MLP 的架构**
> (来自港大，罗平教授团队)
> 5.1 CycleMLP 原理分析
> 5.2 CycleMLP 代码解读

**link：**

[科技猛兽：Vision MLP超详细解读 (原理分析+代码解读) (二)19 赞同 · 15 评论文章](https://zhuanlan.zhihu.com/p/406297302)





### **Section 3：傅里叶变换的类 MLP 架构 (1)**

> **6 GFNet：将 FFT 思想用于空间信息交互**
> (来自清华大学)
> 6.1 GFNet 原理分析
> 6.2 GFNet 代码解读

**link：**

[科技猛兽：Vision MLP超详细解读 (原理分析+代码解读) (三)34 赞同 · 7 评论文章](https://zhuanlan.zhihu.com/p/418500459)





### **Section 4：匹敌 Transformer 的2020年代的卷积网络**

> **7 匹敌 Transformer 的2020年代的卷积网络**
> (来自 FAIR，UCB)
> 7.1 ConvNeXt 原理分析
> 7.2 ConvNeXt 代码解读

**link：**

[科技猛兽：Vision MLP 超详细解读 (原理分析+代码解读) (四)22 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/459088028)





### **Section 5：傅里叶变换的类 MLP 架构 (2)**

> **8 AFNO：自适应傅里叶神经算子**
> (来自 NVIDIA，加州理工，斯坦福大学)
> 8.1 AFNO 原理分析

**link：**

[科技猛兽：Vision MLP超详细解读 (原理分析+代码解读) (五)14 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/478358878)





### **Section 6：图神经网络打造的通用视觉架构**

> **9 Vision GNN：把一张图片建模为一个图**
> (来自中国科学院大学，华为诺亚方舟实验室，北大)
> 9.1 Vision GNN 原理分析
> 9.2 Vision GNN PyTorch 伪代码

**link：**

[科技猛兽：Vision GNN 超详细解读 (一)：打造 GNN 通用视觉模型72 赞同 · 13 评论文章](https://zhuanlan.zhihu.com/p/525684088)





### **Section 7：优化器的重参数化技术**

> **10 RepOptimizer：重参数化你的优化器：VGG 型架构 + 特定的优化器 = 快速模型训练 + 强悍性能**
> (来自清华大学，旷视科技，RepVGG 作者工作)
> 10.1 RepOptimizer 原理分析
> 10.1.1 你有多久没换过优化器了？
> 10.1.2 设计动机和背景
> 10.1.3 本文对业界优化器的知识和理解有何贡献？
> 10.1.4 本文做了哪些具体的工作？
> 10.1.5 RepOpt 的第一步：将架构的先验知识转移到你的优化器中
> 10.1.6 RepOpt 的第二步：通过超搜索获得超参数
> 10.1.7 RepOpt 的第三步：使用 RepOpt 进行训练
> 10.1.8 RepOpt 实验设置
> 10.1.9 RepOpt 实验结果

**link：**

[科技猛兽：重参数化你的优化器：VGG 型架构 + 特定的优化器 = 快速模型训练 + 强悍性能52 赞同 · 6 评论文章](https://zhuanlan.zhihu.com/p/561097597)





### **Section 8：递归门控卷积打造的通用视觉架构**

> **11 HorNet：通过递归门控卷积实现高效高阶的空间信息交互**
> (来自清华大学，周杰，鲁继文团队，Meta AI)
> 11.1 HorNet 原理分析
> 11.1.1 背景和动机
> 11.1.2 HorNet 简介
> 11.1.3gConv：门控卷积实现一阶的空间交互
> 11.1.4gnConv：高阶的门控卷积实现高阶的空间交互
> 11.1.5gnConv 的计算复杂度
> 11.1.6 通过大卷积核进行长距离的交互
> 11.1.7 与 Self-attention 之间的联系
> 11.1.8 HorNet 模型架构
> 11.1.9 实验结果

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (八)：递归门控卷积打造的通用视觉架构19 赞同 · 6 评论文章](https://zhuanlan.zhihu.com/p/571027879)





### **Section 9：用于通用视觉架构的 MetaFormer 基线**

> **12 MetaFormer：令牌混合器类型不重要，宏观架构才是通用视觉模型真正需要的**
> (来自 Sea AI Lab，新加坡国立大学)
> 12.1 MetaFormer 论文解读
> 12.1.1 背景和动机
> 12.1.2 什么是 MetaFormer？
> 12.1.3 PoolFormer 架构
> 12.1.4 PoolFormer 通用视觉任务的实验结果
> 12.1.5 MetaFormer 通用视觉任务的实验结果
> 12.1.6 MetaFormer 的性能还可以再提升吗？
> 12.1.7 新的激活函数 StarReLU
> 12.1.8 缩放分支输出和不使用偏置
> 12.1.9 IdentityFormer 和 RandFormer 架构
> 12.1.10 ConvFormer 和 CAFormer 架构
> 12.1.11 新 MetaFormer 通用视觉任务的实验结果

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (九)：用于通用视觉架构的 MetaFormer 基线20 赞同 · 2 评论文章](https://zhuanlan.zhihu.com/p/575910820)





### **Section 10：将卷积核扩展到 51×51**

> **13 SLaK：从稀疏性的角度将卷积核扩展到 51×51**
> (来自埃因霍温理工大学，德州农工)
> 13.1 SLaK 原理分析
> 13.1.1 背景和动机
> 13.1.2 动态稀疏化技术
> 13.1.3 缩放卷积核的大小使之超过 31×31 的三个观察
> 13.1.4 稀疏大 Kernel 网络：SLaK
> 13.1.5 SLaK 实验结果
> 13.1.6 SLaK 的其他讨论

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (十)：从稀疏性的角度将卷积核扩展到 51×5115 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/553774675)





### **Section 11：Transformer 风格的卷积网络视觉基线模型**

> **14 Conv2Former：Transformer 风格的卷积网络视觉基线模型**
> (来自南开大学，字节跳动)
> 14.1 Conv2Former 论文解读
> 14.1.1 背景和动机
> 14.1.2 卷积调制模块
> 14.1.3 Conv2Former 整体架构
> 14.1.4 实验结果

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (十一)：Conv2Former: Transformer 风格的卷积网络视觉基线模型12 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/589738842)





### **Section 12：无注意力机制视觉 Transformer 的自适应权重混合**

> **15 AMixer：无注意力机制视觉 Transformer 的自适应权重混合**
> (来自清华大学)
> 15.1 AMixer 论文解读
> 15.1.1 背景和动机
> 15.1.2 用统一的视角看待视觉 Transformer 和 MLP 模型
> 15.1.3 重新思考注意力机制
> 15.1.4 自适应权重混合
> 15.1.5 相对注意力权重
> 15.1.6 基于自适应权重混合构造的视觉主干模型 AMixer
> 15.1.7 实验结果

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (十二)：无注意力自适应权重混合视觉模型19 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/591020373)





### **Section 13：简单聚类算法实现强悍视觉架构**

> **16 把图片视为点集，简单聚类算法实现强悍视觉架构 (ICLR 2023 超高分论文)**
> (目前匿名，待更新)
> 1.1 CoCs 论文解读
> 1.1.1 背景和动机
> 1.1.2 把图像视为一组点集
> 1.1.3 CoCs 模型的总体架构和图片的预处理环节
> 1.1.4 上下文聚类块原理
> 1.1.5 实验结果

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (十三)：把图片视为点集，简单聚类算法实现强悍视觉架构30 赞同 · 3 评论文章](https://zhuanlan.zhihu.com/p/592982331)



### **Section 14：2020年代的卷积网络适配自监督学习**

> **17 ConvNeXt V2：使用 MAE 协同设计和扩展 ConvNets**
> (来自 KAIST，Meta AI，FAIR，纽约大学 [ConvNeXt 原作者刘壮，谢赛宁团队])
> 1 ConvNeXt V2 论文解读
> 1.1 背景和动机
> 1.2 自监督学习方法 FCMAE 的初步设计
> 1.3 自监督学习方法 FCMAE 的进一步优化
> 1.3.1 Feature collapse 现象
> 1.3.2 特征余弦距离分析
> 1.3.3 全局响应归一化
> 1.3.4 ConvNeXt V2
> 1.4 实验结果

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (十四)：ConvNeXt V2：使用 MAE 协同设计和扩展 ConvNets25 赞同 · 0 评论文章](https://zhuanlan.zhihu.com/p/592261623)





### **Section 15：一个适应所有 Patch 大小的 ViT 模型**

> **18 FlexiViT：一个适应所有 Patch 大小的 ViT 模型**
> (来自谷歌，ViT，MLP-Mixer 作者团队)
> 18 FlexiViT 论文解读
> 18.1 背景和动机
> 18.2 标准 ViT 对于 Patch Size 灵活吗？
> 18.3 对于 Patch Size 更灵活的 FlexiViT 模型
> 18.4 如何改变 Patch Embedding 的尺寸？
> 18.5 与知识蒸馏的关系
> 18.6 FlexiViT 的内部表征
> 18.7 实验：使用预训练的 FlexiViT 模型

**link：**

[科技猛兽：通用 Vision Backbone 超详细解读 (十五)：FlexiViT：一个适应所有 Patch 大小的 ViT 模型20 赞同 · 2 评论文章](https://zhuanlan.zhihu.com/p/590994472)



------

另外，我的其他博客：

**模型压缩系列工作解读**

[科技猛兽：解读模型压缩系列 (目录)139 赞同 · 17 评论文章](https://zhuanlan.zhihu.com/p/370540483)



**自监督学习系列工作解读**

[科技猛兽：Self-Supervised Learning超详细解读 (目录)408 赞同 · 26 评论文章](https://zhuanlan.zhihu.com/p/381354026)





**@科技猛兽 原创**

**学术合作 or 沟通交流欢迎私信联系~**