# 电子设计自动化

**电子设计自动化**（英语：**Electronic design automation**，[缩写](https://baike.baidu.com/item/缩写)：**EDA**）是指利用[计算机辅助设计](https://baike.baidu.com/item/计算机辅助设计)（CAD）软件，来完成[超大规模集成电路](https://baike.baidu.com/item/超大规模集成电路)（VLSI）芯片的[功能设计](https://baike.baidu.com/item/功能设计)、[综合](https://baike.baidu.com/item/综合)、[验证](https://baike.baidu.com/item/验证)、[物理设计](https://baike.baidu.com/item/物理设计/12728832)（包括[布局](https://baike.baidu.com/item/布局)、[布线](https://baike.baidu.com/item/布线)、[版图](https://baike.baidu.com/item/版图/791489)、[设计规则检查](https://baike.baidu.com/item/设计规则检查)等）等流程的设计方式。

## 历史与发展

在电子设计自动化出现之前，设计人员必须手工完成集成电路的设计、布线等工作，这是因为当时所谓集成电路的复杂程度远不及现在。工业界开始使用几何学方法来制造用于电路光绘（photoplotter）的胶带。到了1970年代中期，开发人应尝试将整个设计过程自动化，而不仅仅满足于自动完成掩膜草图。第一个电路[布局](https://baike.baidu.com/item/布局)、[布线](https://baike.baidu.com/item/布线)工具研发成功。设计自动化研讨会（Design Automation Conference）在这一时期被创立，旨在促进电子设计自动化的发展。 [1] 

电子设计自动化发展的下一个重要阶段以卡弗尔·米德（Carver Mead）和[琳·康维](https://baike.baidu.com/item/琳·康维)于1980年发表的论文《[超大规模集成电路系统导论](https://baike.baidu.com/item/超大规模集成电路系统导论/51096927)》（*Introduction to VLSI Systems*）为标志。这一篇具有重大意义的论文提出了通过[编程语言](https://baike.baidu.com/item/编程语言)来进行芯片设计的新思想。如果这一想法得到实现，芯片设计的复杂程度可以得到显著提升。这主要得益于用来进行集成电路[逻辑仿真](https://baike.baidu.com/item/逻辑仿真)、[功能验证](https://baike.baidu.com/item/功能验证)的工具的性能得到相当的改善。随着计算机仿真技术的发展，设计项目可以在构建实际硬件电路之前进行[仿真](https://baike.baidu.com/item/仿真)，芯片[布局](https://baike.baidu.com/item/布局)、[布线](https://baike.baidu.com/item/布线/1516927)对人工设计的要求降低，而且软件错误率不断降低。直至今日，尽管所用的语言和工具仍然不断在发展，但是通过编程语言来设计、验证电路预期行为，利用工具软件综合得到低抽象级（或称“后端”）[物理设计](https://baike.baidu.com/item/物理设计/12728832)的这种途径，仍然是数字集成电路设计的基础。

从1981年开始，电子设计自动化逐渐开始商业化。1984年的设计自动化会议（Design Automation Conference）上还举办了第一个以电子设计自动化为主题的销售展览。Gateway设计自动化在1986年推出了一种[硬件描述语言](https://baike.baidu.com/item/硬件描述语言)[Verilog](https://baike.baidu.com/item/Verilog)，这种语言在现在是最流行的高级抽象设计语言。1987年，在[美国国防部](https://baike.baidu.com/item/美国国防部)的资助下，另一种硬件描述语言VHDL被创造出来。现代的电子设计自动化设计工具可以识别、读取不同类型的硬件描述。根据这些语言规范产生的各种仿真系统迅速被推出，使得设计人员可对设计的芯片进行直接仿真。后来，技术的发展更侧重于[逻辑综合](https://baike.baidu.com/item/逻辑综合)。

[数字集成电路](https://baike.baidu.com/item/数字集成电路/6931724)的设计都比较模块化（参见[集成电路设计](https://baike.baidu.com/item/集成电路设计)、[设计收敛](https://baike.baidu.com/item/设计收敛)（Design closure）和设计流（Design flow (EDA)））。半导体器件制造工艺需要标准化的设计描述，高抽象级的描述将被编译为信息单元（cell）的形式。设计人员在进行逻辑设计时尚无需考虑信息单元的具体硬件工艺。利用特定的集成电路制造工艺来实现硬件电路，信息单元就会实施预定义的逻辑或其他电子功能。半导体硬件厂商大多会为它们制造的元件提供“元件库”，并提供相应的标准化仿真模型。相比数字的电子设计自动化工具，[模拟系统](https://baike.baidu.com/item/模拟系统)的电子设计自动化工具大多并非模块化的，这是因为模拟电路的功能更加复杂，而且不同部分的相互影响较强，而且作用规律复杂，电子元件大多没有那么理想。Verilog AMS就是一种用于模拟电子设计的硬件描述语言。此文，设计人员可以使用[硬件验证语言](https://baike.baidu.com/item/硬件验证语言)来完成项目的验证工作最新的发展趋势是将集描述语言、验证语言集成为一体，典型的例子有[SystemVerilog](https://baike.baidu.com/item/SystemVerilog)。

随着集成电路规模的扩大、半导体技术的发展，电子设计自动化的重要性急剧增加。这些工具的使用者包括半导体器件制造中心的硬件技术人员，他们的工作是操作半导体器件制造设备并管理整个工作车间。一些以设计为主要业务的公司，也会使用电子设计自动化软件来评估制造部门是否能够适应新的设计任务。电子设计自动化工具还被用来将设计的功能导入到类似[现场可编程逻辑门阵列](https://baike.baidu.com/item/现场可编程逻辑门阵列)的半定制[可编程逻辑器件](https://baike.baidu.com/item/可编程逻辑器件)，或者生产[全定制](https://baike.baidu.com/item/全定制)的[专用集成电路](https://baike.baidu.com/item/专用集成电路)。

## 现况

现今数字电路非常模组化（参见[集成电路设计](https://baike.baidu.com/item/集成电路设计/2090026)、[设计收敛](https://baike.baidu.com/item/设计收敛)、设计流程 (EDA)），产线最前端将设计流程标准化，把设计流程区分为许多“细胞”（cells），而暂不考虑技术，接着细胞则以特定的集成电路技术实现逻辑或其他电子功能。制造商通常会提供组件库（libraries of components），以及符合标准模拟工具的模拟模型给生产流程。模拟 EDA 工具较不模组化，因为它需要更多的功能，零件间需要更多的互动，而零件一般说较不理想。

在电子产业中，由于半导体产业的规模日益扩大，EDA 扮演越来越重要的角色。使用这项技术的厂商多是从事半导体器件制造的[代工](https://baike.baidu.com/item/代工)制造商，以及使用 EDA 模拟软件以评估生产情况的设计服务公司。EDA 工具也应用在[现场可编程逻辑门阵列](https://baike.baidu.com/item/现场可编程逻辑门阵列)的程序设计上。

2019年，我国EDA市场规模约为5.8亿美元，仅占全球市场的5.6%。中国EDA厂商总营收不到4.2亿元，只占全球市场份额的0.6%。 [3] 

## 社会意义

EDA被誉为“芯片之母”，是电子设计的基石产业。拥有百亿美金的EDA市场构筑了整个电子产业的根基，可以说“谁掌握了EDA，谁就有了芯片领域的主导权。

”近年来，我国在多个领域面临关键核心技术“卡脖子”的危机，其中对芯片技术领域的制约尤为严重，尽快打破垄断、让芯片关键技术不再受制于人可谓刻不容缓。

对于我国来说，EDA芯片设计软件的国产化对于芯片领域的突破意义与光刻机制造同等重要。因此，中国团队拿下EDA全球冠军可以说为我国前沿科技领域研究注入了强心剂，极大程度上提振了我国突破技术封锁、实现高端芯片制造独立自主的信心。 [2] 