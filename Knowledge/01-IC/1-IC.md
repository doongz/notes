# IC

来源：https://en.wiki.hancel.org/wiki/Integrated_circuit

- 工艺
- 设计
- 制造
- 器件
- 封装
- 类型：数字IC、模拟IC、混合IC

## 概述

**集成电路**或**单片集成电路**（也称为**IC**、**芯片**或**微芯片**）是在一个小平板（或“芯片”）[半导体](https://en.wikipedia.ahmu.cf/wiki/Semiconductor)材料（通常是[硅](https://en.wikipedia.ahmu.cf/wiki/Silicon)）上的一组[电子电路](https://en.wikipedia.ahmu.cf/wiki/Electronic_circuit)。[大量](https://en.wikipedia.ahmu.cf/wiki/Transistor_count)微型[MOSFET](https://en.wikipedia.ahmu.cf/wiki/MOSFET)（金属氧化物半导体[场效应晶体管](https://en.wikipedia.ahmu.cf/wiki/Field-effect_transistors)）集成到一个小芯片中。

这导致电路比由分立[电子元件](https://en.wikipedia.ahmu.cf/wiki/Electronic_component)构成的电路小几个数量级、速度更快且成本更低。

[金属氧化物硅](https://en.wikipedia.ahmu.cf/wiki/Metal–oxide–silicon)(MOS)[半导体器件制造](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication)技术的进步使[超大规模集成](https://en.wikipedia.ahmu.cf/wiki/Very-large-scale_integration)变得实用。

[与分立电路](https://en.wikipedia.ahmu.cf/wiki/Discrete_circuit)相比，IC 有两个主要优势：成本和性能。成本很低，因为这些芯片及其所有组件都是通过[光刻](https://en.wikipedia.ahmu.cf/wiki/Photolithography)作为一个单元印刷的，而不是一次构建一个晶体管。此外，封装 IC 使用的材料比分立电路少得多。性能之所以高是因为 IC 的组件切换速度很快，并且由于尺寸小且接近，因此消耗的功率相对较少。IC 的主要缺点是设计它们和制造所需[光掩模](https://en.wikipedia.ahmu.cf/wiki/Photomask)的成本很高。如此高的初始成本意味着 IC 仅在预计 [大批量生产](https://en.wikipedia.ahmu.cf/wiki/Economies_of_scale)时才具有商业可行性。

## 设计

来源：https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit_design

**集成电路设计**或**IC 设计是**[电子工程](https://en.wikipedia.ahmu.cf/wiki/Electronics_engineering)的一个子领域，包括设计[集成电路](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuits)或 IC所需的特定[逻辑](https://en.wikipedia.ahmu.cf/wiki/Boolean_logic)和[电路设计技术。](https://en.wikipedia.ahmu.cf/wiki/Circuit_design)IC 由通过[光刻技术](https://en.wikipedia.ahmu.cf/wiki/Photolithography)在单片[半导体](https://en.wikipedia.ahmu.cf/wiki/Semiconductor)衬底上构建到[电气网络中的小型化](https://en.wikipedia.ahmu.cf/wiki/Electrical_network)[电子元件组成](https://en.wikipedia.ahmu.cf/wiki/Electronic_component)。

IC设计可分为[数字](https://en.wikipedia.ahmu.cf/wiki/Digital_data)IC设计和[模拟](https://en.wikipedia.ahmu.cf/wiki/Analog_electronics)IC设计两大类。

- 数字 IC 设计是生产[微处理器](https://en.wikipedia.ahmu.cf/wiki/Microprocessors)、[FPGA](https://en.wikipedia.ahmu.cf/wiki/FPGA)、存储器（[RAM](https://en.wikipedia.ahmu.cf/wiki/Random-access_memory)、[ROM](https://en.wikipedia.ahmu.cf/wiki/Read-only_memory)和[闪存](https://en.wikipedia.ahmu.cf/wiki/Flash_memory)）和数字[ASIC](https://en.wikipedia.ahmu.cf/wiki/Application-specific_integrated_circuit)等组件。数字设计侧重于逻辑正确性、最大化电路密度和放置电路，以便有效地路由时钟和时序信号。
- 模拟IC设计还专攻功率IC设计和[RF](https://en.wikipedia.ahmu.cf/wiki/Radio_frequency) IC设计。模拟IC设计用于[运算放大器](https://en.wikipedia.ahmu.cf/wiki/Op-amp)、[线性稳压器](https://en.wikipedia.ahmu.cf/wiki/Linear_regulator)、[锁相环](https://en.wikipedia.ahmu.cf/wiki/Phase_locked_loop)的设计，[振荡器](https://en.wikipedia.ahmu.cf/wiki/Oscillator)和[有源滤波器](https://en.wikipedia.ahmu.cf/wiki/Active_filter)。模拟设计更关注半导体器件的物理特性，例如增益、匹配、功耗和电阻。

现代 IC 设计的复杂性，以及快速生产设计的市场压力，导致在 IC 设计过程中广泛使用[自动化设计工具。](https://en.wikipedia.ahmu.cf/wiki/Electronic_design_automation)简而言之，使用[EDA 软件](https://en.wikipedia.ahmu.cf/wiki/Electronic_design_automation)设计 IC 就是对 IC 要执行的指令进行设计、测试和验证。

集成电路设计涉及电子元件的创建，例如[晶体管](https://en.wikipedia.ahmu.cf/wiki/Transistors)、[电阻器](https://en.wikipedia.ahmu.cf/wiki/Resistors)、[电容器](https://en.wikipedia.ahmu.cf/wiki/Capacitors)以及将这些元件[互连](https://en.wikipedia.ahmu.cf/wiki/Interconnects_(integrated_circuits))到一块半导体（通常是[硅](https://en.wikipedia.ahmu.cf/wiki/Silicon)）上。由于衬底硅是导电的并且经常形成单个组件的有源区，因此需要一种隔离形成在[衬底中的各个组件的方法。](https://en.wikipedia.ahmu.cf/wiki/Wafer_(electronics))

两种常用方法是[pn 结隔离](https://en.wikipedia.ahmu.cf/wiki/P-n_junction_isolation)和[电介质隔离](https://en.wikipedia.ahmu.cf/w/index.php?title=Dielectric_isolation&action=edit&redlink=1)。必须注意晶体管的功耗和互连电阻以及互连、[接触和通孔的电流密度](https://en.wikipedia.ahmu.cf/wiki/Via_(electronics))因为与分立元件相比，IC 包含非常小的器件，因此此类问题不是问题。金属互连中的[电迁移和对微小组件的](https://en.wikipedia.ahmu.cf/wiki/Electromigration)[ESD](https://en.wikipedia.ahmu.cf/wiki/Electrostatic_discharge)损坏也值得关注。最后，某些电路子块的物理布局通常很关键，以实现所需的操作速度，将 IC 的噪声部分与安静部分隔离，平衡 IC 上产生的热量影响，或便于[放置](https://en.wikipedia.ahmu.cf/wiki/Placement_(EDA))与 IC 外部电路的连接。

### 设计流程

一个典型的 IC 设计周期包括几个步骤：

1. 系统规格

   1. 可行性研究和模具尺寸估算
   2. 功能分析

2. 架构或系统级设计

3. 逻辑设计

   1. 模拟设计、仿真和布局
   2. 数字设计与仿真
   3. 系统仿真与验证

4. 电路设计

   1. 数字设计合成
   2. [测试设计](https://en.wikipedia.ahmu.cf/wiki/Design_For_Test)和[自动测试模式生成](https://en.wikipedia.ahmu.cf/wiki/Automatic_test_pattern_generation)
   3. [可制造性设计 (IC)](https://en.wikipedia.ahmu.cf/wiki/Design_for_manufacturability_(IC))

5. 物理设计

   1. 平面图
   2. 地点和路线
   3. 寄生提取

6. 物理验证和

   签核

   1. 静态时序
   2. 协同仿真和时序

7. 掩膜数据准备

   （布局后处理）

   1. [用Tape out](https://en.wikipedia.ahmu.cf/wiki/Tape_out)完成芯片加工
   2. 标线布局
   3. Layout-to-mask准备

8. [晶圆制造](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_fabrication)

9. [打包](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit_packaging)

10. 模具测试

    1. [后硅验证](https://en.wikipedia.ahmu.cf/wiki/Post_silicon_validation)和集成
    2. 器件表征
    3. 调整（如有必要）

11. 芯片部署

    1. 数据表生成（通常是[可移植文档格式](https://en.wikipedia.ahmu.cf/wiki/Portable_Document_Format)(PDF) 文件）
    2. 斜坡上升
    3. 生产
    4. 良率分析/保修分析[可靠性（半导体）](https://en.wikipedia.ahmu.cf/wiki/Reliability_(semiconductor))
    5. 任何退货的[失败分析](https://en.wikipedia.ahmu.cf/wiki/Failure_analysis)
    6. 尽可能利用生产信息规划下一代芯片

## 类型

集成电路可大致分为[模拟](https://en.wikipedia.ahmu.cf/wiki/Analog_circuit)、[[59\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit#cite_note-59) [数字](https://en.wikipedia.ahmu.cf/wiki/Digital_circuit)[[60\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit#cite_note-60)和[混合信号](https://en.wikipedia.ahmu.cf/wiki/Mixed-signal_integrated_circuit)[[61\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit#cite_note-61)，由同一 IC 上的模拟和数字信号组成。

数字集成电路可以在几平方毫米内包含数十亿[[39\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit#cite_note-Pascal-39)[逻辑门](https://en.wikipedia.ahmu.cf/wiki/Logic_gate)、[触发器](https://en.wikipedia.ahmu.cf/wiki/Flip-flop_(electronics))、[多路复用器和其他电路。](https://en.wikipedia.ahmu.cf/wiki/Multiplexer)与板级集成相比，这些电路的小尺寸允许高速、低功耗和降低[制造成本。](https://en.wikipedia.ahmu.cf/wiki/Manufacturing_cost)这些数字 IC（通常是[微处理器](https://en.wikipedia.ahmu.cf/wiki/Microprocessor)、[DSP](https://en.wikipedia.ahmu.cf/wiki/Digital_signal_processor)和[微控制器](https://en.wikipedia.ahmu.cf/wiki/Microcontroller)）使用[布尔代数](https://en.wikipedia.ahmu.cf/wiki/Boolean_algebra)来处理[“一”和“零”信号](https://en.wikipedia.ahmu.cf/wiki/Binary_number)。

其中最先进的集成电路是[微处理器](https://en.wikipedia.ahmu.cf/wiki/Microprocessor)或“**[核心](https://en.wikipedia.ahmu.cf/wiki/Processor_core)**”，用于个人电脑、手机、[微波炉](https://en.wikipedia.ahmu.cf/wiki/Microwave_oven)等。多个核心可以集成在单个 IC 或芯片中。数字[存储芯片](https://en.wikipedia.ahmu.cf/wiki/Computer_memory)和[专用集成电路](https://en.wikipedia.ahmu.cf/wiki/Application-specific_integrated_circuit)(ASIC) 是其他集成电路系列的示例。

1980 年代，开发了[可编程逻辑器件](https://en.wikipedia.ahmu.cf/wiki/Programmable_logic_device)。这些设备包含的电路的逻辑功能和连接性可以由用户编程，而不是由集成电路制造商固定。这允许对芯片进行编程以执行各种 LSI 类型的功能，例如[逻辑门](https://en.wikipedia.ahmu.cf/wiki/Logic_gate)、[加法器](https://en.wikipedia.ahmu.cf/wiki/Adder_(electronics))和[寄存器](https://en.wikipedia.ahmu.cf/wiki/Processor_register)。可编程性有多种形式——只能[编程一次](https://en.wikipedia.ahmu.cf/wiki/Programmable_read-only_memory)的器件、可以擦除然后[使用紫外线](https://en.wikipedia.ahmu.cf/wiki/EPROM)重新编程的器件、可以使用[闪存](https://en.wikipedia.ahmu.cf/wiki/Flash_memory)（重新）编程的器件以及[现场可编程门阵列](https://en.wikipedia.ahmu.cf/wiki/Field-programmable_gate_array)（FPGA）可以在任何时间进行编程，包括在操作期间。当前的 FPGA（截至 2016 年）可以实现相当于数百万个门，并在高达 1 [GHz的](https://en.wikipedia.ahmu.cf/wiki/Hertz)[频率](https://en.wikipedia.ahmu.cf/wiki/Clock_rate)下运行。

[传感器](https://en.wikipedia.ahmu.cf/wiki/Sensor)、[电源管理电路](https://en.wikipedia.ahmu.cf/wiki/Power_network_design_(IC))和[运算放大器](https://en.wikipedia.ahmu.cf/wiki/Operational_amplifier)(op-amps)等模拟 IC处理[连续信号](https://en.wikipedia.ahmu.cf/wiki/Continuous_signal)，并执行[放大](https://en.wikipedia.ahmu.cf/wiki/Amplifier)、[有源滤波](https://en.wikipedia.ahmu.cf/wiki/Active_filter)、[解调](https://en.wikipedia.ahmu.cf/wiki/Demodulation)和[混频](https://en.wikipedia.ahmu.cf/wiki/Frequency_mixer)等模拟功能。

IC 可以将模拟和数字电路组合在一个芯片上，以创建模数转换器和[数模转换器](https://en.wikipedia.ahmu.cf/wiki/Analog-to-digital_converter)等[功能](https://en.wikipedia.ahmu.cf/wiki/Digital-to-analog_converter)。这种混合信号电路尺寸更小，成本更低，但必须考虑信号干扰。在 1990 年代后期之前，[无线电](https://en.wikipedia.ahmu.cf/wiki/Radios)无法采用与微处理器相同的低成本[CMOS工艺制造。](https://en.wikipedia.ahmu.cf/wiki/CMOS)但自 1998 年以来，无线电芯片已使用[RF CMOS](https://en.wikipedia.ahmu.cf/wiki/RF_CMOS)工艺开发。示例包括英特尔的[DECT](https://en.wikipedia.ahmu.cf/wiki/Digital_Enhanced_Cordless_Telecommunications)无绳电话，或由[Atheros](https://en.wikipedia.ahmu.cf/wiki/Atheros)和其他公司开发的[802.11](https://en.wikipedia.ahmu.cf/wiki/802.11) ( [Wi-Fi ) 芯片。](https://en.wikipedia.ahmu.cf/wiki/Wi-Fi)[[63\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit#cite_note-IEEE-CMOS-dualband-n-63)

现代[电子元器件分销商](https://en.wikipedia.ahmu.cf/wiki/Category:Electronic_component_distributors)通常将集成电路进一步细分：

- [数字IC](https://en.wikipedia.ahmu.cf/wiki/Digital_integrated_circuit)分为逻辑IC（如[微处理器](https://en.wikipedia.ahmu.cf/wiki/Microprocessors)和[微控制器](https://en.wikipedia.ahmu.cf/wiki/Microcontrollers)）、[存储芯片](https://en.wikipedia.ahmu.cf/wiki/Memory_chip)（如[MOS存储器](https://en.wikipedia.ahmu.cf/wiki/MOS_memory)和[浮栅](https://en.wikipedia.ahmu.cf/wiki/Floating-gate)存储器）、接口IC（[电平转换器](https://en.wikipedia.ahmu.cf/wiki/Logic_level)、[串行器/解串器](https://en.wikipedia.ahmu.cf/wiki/Serializer/deserializer)等）、[电源管理IC](https://en.wikipedia.ahmu.cf/wiki/Power_management_IC)和[可编程器件](https://en.wikipedia.ahmu.cf/wiki/Programmable_logic_device).
- [模拟集成电路](https://en.wikipedia.ahmu.cf/wiki/Analog_integrated_circuit)分为[线性集成电路](https://en.wikipedia.ahmu.cf/wiki/Linear_integrated_circuit)和[射频电路](https://en.wikipedia.ahmu.cf/wiki/RF_circuit)（[射频](https://en.wikipedia.ahmu.cf/wiki/Radio_frequency)电路）。
- [混合信号集成电路](https://en.wikipedia.ahmu.cf/wiki/Mixed-signal_integrated_circuit)分为[数据采集](https://en.wikipedia.ahmu.cf/wiki/Data_acquisition)IC（包括[A/D转换器](https://en.wikipedia.ahmu.cf/wiki/A/D_converter)、[D/A转换器](https://en.wikipedia.ahmu.cf/wiki/D/A_converter)、[数字电位器](https://en.wikipedia.ahmu.cf/wiki/Digital_potentiometer)）、[时钟/定时IC](https://en.wikipedia.ahmu.cf/wiki/Clock_generator)、[开关电容](https://en.wikipedia.ahmu.cf/wiki/Switched_capacitor)（SC）电路和[RF CMOS](https://en.wikipedia.ahmu.cf/wiki/RF_CMOS)电路。
- [三维集成电路](https://en.wikipedia.ahmu.cf/wiki/Three-dimensional_integrated_circuit)(3D IC) 分为[硅通孔](https://en.wikipedia.ahmu.cf/wiki/Through-silicon_via)(TSV) IC 和 Cu-Cu 连接 IC。

## 制造

来源：https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication

**半导体器件制造**是用于制造[半导体器件](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_devices)的过程，通常是用于[集成电路](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit)(IC) 芯片（例如现代计算机处理器、微控制器和存储芯片（例如[NAND 闪存](https://en.wikipedia.ahmu.cf/wiki/NAND_flash)和[DRAM](https://en.wikipedia.ahmu.cf/wiki/DRAM) ）中的[金属氧化物半导体](https://en.wikipedia.ahmu.cf/wiki/Metal–oxide–semiconductor)(MOS) 器件）存在于日常[电气](https://en.wikipedia.ahmu.cf/wiki/Electrical)和[电子](https://en.wikipedia.ahmu.cf/wiki/Electronics)设备中。它是[光刻](https://en.wikipedia.ahmu.cf/wiki/Photolithography)和化学处理步骤的多步骤序列（例如[表面钝化](https://en.wikipedia.ahmu.cf/wiki/Surface_passivation)、[热氧化](https://en.wikipedia.ahmu.cf/wiki/Thermal_oxidation)、[平面扩散](https://en.wikipedia.ahmu.cf/wiki/Planar_process)和[结隔离](https://en.wikipedia.ahmu.cf/wiki/P–n_junction_isolation)) 在此期间，[电子电路](https://en.wikipedia.ahmu.cf/wiki/Electronic_circuits)逐渐在由纯[半导体](https://en.wikipedia.ahmu.cf/wiki/Semiconducting)材料制成的[晶片上创建。](https://en.wikipedia.ahmu.cf/wiki/Wafer_(electronics))几乎总是使用[硅，但各种](https://en.wikipedia.ahmu.cf/wiki/Silicon)[化合物半导体](https://en.wikipedia.ahmu.cf/wiki/Compound_semiconductor)用于特殊应用。

整个制造过程需要时间，从开始到封装芯片准备好发货，至少需要 6 到 8 周（仅流片，不包括电路设计），并且在高度专业化的[半导体制造工厂](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_fabrication_plant)（也称为代工厂或晶圆厂）中进行。[[1\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-berlin-regression-methods-1)所有制造都在无尘室内进行，这是工厂的中心部分。在更先进的半导体器件中，例如现代[14](https://en.wikipedia.ahmu.cf/wiki/14_nanometer) / [10](https://en.wikipedia.ahmu.cf/wiki/10_nanometer) / [7 nm](https://en.wikipedia.ahmu.cf/wiki/7_nanometer)节点，制造可能需要长达 15 周的时间，行业平均时间为 11-13 周。[[2\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-2)先进制造设施的生产是完全自动化的，并在密封的氮气环境中进行，以提高产量（晶圆中正常工作的微芯片的百分比），自动化材料处理系统负责晶圆在机器之间的运输。晶圆在[FOUP](https://en.wikipedia.ahmu.cf/wiki/FOUP)内运输，特殊的密封塑料盒。所有机器和 FOUP 都包含内部氮气氛。机器和 FOUP 内的空气通常比洁净室中的周围空气更清洁。这种内部气氛被称为迷你环境。[[3\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-3)制造工厂需要大量的液氮来维持生产机械和 FOUP 内的气氛，而生产机械和 FOUP 会不断地用氮气吹扫。

### 尺寸 / 工艺

特定的**半导体工艺**对芯片每层特征的最小尺寸和间距有特定的规则。[[5\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-shirriff_die_shrink-5) 较新的半导体工艺通常具有更小的最小尺寸和更紧密的间距，这允许简单的[芯片缩小](https://en.wikipedia.ahmu.cf/wiki/Die_shrink)以降低成本并提高性能。[[5\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-shirriff_die_shrink-5)部分是由于晶体管密度的增加（每平方毫米的晶体管数量）。早期的半导体工艺有任意的名称，例如[HMOS](https://en.wikipedia.ahmu.cf/wiki/HMOS) III、[CHMOS](https://en.wikipedia.ahmu.cf/wiki/CHMOS) V；后面的都是按尺寸指的，比如[90nm工艺](https://en.wikipedia.ahmu.cf/wiki/90_nm_process)。

按照行业标准，每一代半导体制造工艺，也称为**技术节点**[[6\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-6)或**工艺节点**[ [7\] ](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-7)[[8\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-8)，由工艺的**最小特征尺寸**指定。技术节点，也称为“工艺技术”或简称为“节点”，通常由工艺[晶体管栅极](https://en.wikipedia.ahmu.cf/wiki/Gate_(transistor))长度的[纳米](https://en.wikipedia.ahmu.cf/wiki/Nanometers)（或历史上的[微米）大小表示。](https://en.wikipedia.ahmu.cf/wiki/Micrometre)然而，自 1994 年以来情况并非如此。最初晶体管栅极长度小于工艺节点名称（例如 350 nm 节点）所建议的长度。然而，这种趋势在 2009 年发生了逆转。[[9\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-9)用于命名工艺节点的纳米已成为一种营销术语，与实际特征尺寸和晶体管密度（每平方毫米的晶体管数量）无关。例如，英特尔之前的 10 纳米工艺实际上有 7 纳米宽度的特征（[FinFET](https://en.wikipedia.ahmu.cf/wiki/FinFET)鳍的尖端），英特尔之前的 10 纳米工艺在晶体管密度上与台积电的 7 纳米工艺相似，而格罗方德的 12 和 14 纳米工艺有相似的特征尺寸。

IC 可以由[集成设备制造商](https://en.wikipedia.ahmu.cf/wiki/Integrated_device_manufacturer)(IDM) 在内部制造，也可以使用[代工模式](https://en.wikipedia.ahmu.cf/wiki/Foundry_model)制造。IDM 是垂直整合的公司（如[英特尔](https://en.wikipedia.ahmu.cf/wiki/Intel)和[三星](https://en.wikipedia.ahmu.cf/wiki/Samsung)），他们设计、制造和销售自己的 IC，并可能向其他公司（后者通常向[无晶圆厂公司](https://en.wikipedia.ahmu.cf/w/index.php?title=Fabless_company&action=edit&redlink=1)）提供设计和/或制造（代工）服务。在代工厂模式中，无晶圆厂公司（如英[伟达](https://en.wikipedia.ahmu.cf/wiki/Nvidia)）只设计和销售 IC，并将所有制造外包给[台积电](https://en.wikipedia.ahmu.cf/wiki/TSMC)等[纯代工厂](https://en.wikipedia.ahmu.cf/wiki/Pure_play#pure_play_foundries)。这些代工厂可能会提供 IC 设计服务。

### 步骤

[半导体](https://en.wikipedia.ahmu.cf/wiki/Semiconductor)IC 采用[平面工艺](https://en.wikipedia.ahmu.cf/wiki/Planar_process)制造，包括三个关键工艺步骤—— [光刻](https://en.wikipedia.ahmu.cf/wiki/Photolithography)、沉积（如[化学气相沉积](https://en.wikipedia.ahmu.cf/wiki/Chemical_vapor_deposition)）和[蚀刻](https://en.wikipedia.ahmu.cf/wiki/Etching_(microfabrication))。主要工艺步骤辅以掺杂和清洗。从 22 nm 节点（英特尔）或 16/14 nm 节点开始，更新的或高性能 IC 可能会使用[多栅极](https://en.wikipedia.ahmu.cf/wiki/Multigate_device) [FinFET](https://en.wikipedia.ahmu.cf/wiki/FinFET)或[GAAFET晶体管而不是平面晶体管。](https://en.wikipedia.ahmu.cf/wiki/GAAFET)

[大多数应用都使用单晶硅](https://en.wikipedia.ahmu.cf/wiki/Monocrystalline_silicon) [晶片](https://en.wikipedia.ahmu.cf/wiki/Wafer_(electronics))（或者对于特殊应用，使用其他半导体，例如[砷化镓](https://en.wikipedia.ahmu.cf/wiki/Gallium_arsenide)）。晶片不必完全是硅。[光刻](https://en.wikipedia.ahmu.cf/wiki/Photolithography)用于标记要[掺杂](https://en.wikipedia.ahmu.cf/wiki/Doping_(semiconductor))的衬底的不同区域或在其上沉积多晶硅、绝缘体或金属（通常是铝或铜）轨道。[掺杂剂](https://en.wikipedia.ahmu.cf/wiki/Dopant)是有意引入半导体以调节其电子特性的杂质。掺杂是将掺杂剂添加到半导体材料中的过程。

在晶圆上制造芯片需要经过上百个工序，**主要的工艺步骤包括光刻、刻蚀、掺杂、薄膜沉积等**。

**光刻**

光刻的目的是把设计好的图形转印到晶圆上。首先我们在晶圆上层光刻胶，光刻胶(正胶)的特性是经过特定频率光线的照射后，可以溶解在显影液里。然后将设计好图形的掩膜版罩在晶圆之上，用光刻机进行曝光，有些光线透过掩膜版照射到光刻胶上，有些光线被掩膜版上的图形阻挡。曝光之后，将晶圆放在显影液里浸泡，被光线照射过的光刻胶溶解，**晶圆表面就留下了和掩膜版一样的光刻胶图形**。

光刻是晶圆加工制造中最核心的工艺，晶圆加工的工艺水平主要取决于光刻的精度。通常我们说的28纳米或14纳米工艺，指的就是光刻机能够分辨的最小图形尺寸。晶圆上能够加工的图形尺寸越小，那么同样复杂度的芯片电路所占的面积就越小，一片晶圆上能够切割出来的芯片数量也就越多。由于芯片的加工步骤都是以晶圆为单位进行的，平均下来单个芯片的成本也就很低。当然，最小线宽的缩小不仅能带来芯片成本的下降，还有很多其他好处，比如功耗的降低、集成度的提高以及良品率的提升等。

得到光刻图形后，就可以进行下一步的加工，比如刻蚀、掺杂或薄膜沉积等。

**刻蚀**

刻蚀可以**将没有被光刻胶保护的部分侵蚀掉**，一般用来在晶圆上挖槽，通常分为干法刻蚀和湿法刻蚀，前者主要采用等离子体轰击,后者一般采用溶剂浸泡溶解。刻蚀完成后，清除残余光刻胶，就得到了想要的凹槽图案。

**掺杂**

**为了改变半导体的电学性质**，在晶圆上形成四PN结、电阻、欧姆接触等结构，我们还需要将特定的杂质(一般是Ⅲ、Ⅳ族元素，比如磷、砷、硼等)掺入特定的区域中。小尺寸工艺条件下最主要的掺杂方法是离子注入，它直接将具有很高能量的杂质离子注入半导体衬底中，可以精确控制掺杂的深度和浓度。

**退火**

离子注入完成后，通常需要进行退火。退火是指将晶圆放在氮气等不活泼气体氛围中进行热处理，使不在晶格位置上的离子运动到晶格位置上，一方面可以**激活杂质，使其具有电活性**，另一方面也可以**消除离子注入带来的晶格损伤**。

**沉积**

薄膜沉积也是片生产过程中重要的工艺步骤,通常分为化学气相淀积( Chemical Vapor Deposition，CVD)和物理气相淀积( Physical Vapor Deposition，PVD)。CVD是指通过气态物质的化学反应，在衬底上淀积一层薄膜材料的过程。它几乎可以淀积集成电路工艺中所需要的各种薄膜，例如二氧化硅、多晶硅、非晶硅、氮化硅、金属(钨、钼)等，适用范围广、台阶覆盖性好。PVD主要包括蒸发和溅射,通常用于**淀积芯片中的电极和金属互联层**。

**将前述工艺重复若干次**，就可以在晶圆上加工出设计好的芯片。通常**在进行每一道主要工艺步骤之前都需要重新进行一次光刻**，因此，也常用掩膜版的数量来衡量工艺的复杂度，现在加工出一颗CPU芯片，往往需要上百套掩膜版，数千个加工步骤。

**光刻-对光刻胶处理**

**刻蚀-对硅片处理**

- 晶圆加工

  - 湿洗
    - [用丙酮](https://en.wikipedia.ahmu.cf/wiki/Acetone)、[三氯乙烯](https://en.wikipedia.ahmu.cf/wiki/Trichloroethylene)和[超纯水](https://en.wikipedia.ahmu.cf/wiki/Ultrapure_water)等溶剂清洗
    - [食人鱼解决方案](https://en.wikipedia.ahmu.cf/wiki/Piranha_solution)
    - [RCA 清洁](https://en.wikipedia.ahmu.cf/wiki/RCA_clean)
  - [表面钝化](https://en.wikipedia.ahmu.cf/wiki/Surface_passivation)
  - [光刻](https://en.wikipedia.ahmu.cf/wiki/Photolithography)
  - [离子注入](https://en.wikipedia.ahmu.cf/wiki/Ion_implantation)（其中[掺杂剂](https://en.wikipedia.ahmu.cf/wiki/Dopant)嵌入晶圆中，产生导电率增加或减少的区域）
  - 蚀刻（微细加工）
    - 干法蚀刻（等离子蚀刻）
      - 反应离子蚀刻(RIE)
        - [深反应离子蚀刻](https://en.wikipedia.ahmu.cf/wiki/Deep_reactive-ion_etching)
        - [原子层蚀刻](https://en.wikipedia.ahmu.cf/wiki/Atomic_layer_etching)(ALE)
    - 湿法蚀刻
      - [缓冲氧化物蚀刻](https://en.wikipedia.ahmu.cf/wiki/Buffered_oxide_etch)
  - [等离子灰化](https://en.wikipedia.ahmu.cf/wiki/Plasma_ashing)
  - 热处理
    - [快速热退火](https://en.wikipedia.ahmu.cf/wiki/Rapid_thermal_anneal)
    - [炉退火](https://en.wikipedia.ahmu.cf/wiki/Furnace_anneal)
    - [热氧化](https://en.wikipedia.ahmu.cf/wiki/Thermal_oxidation)
  - [化学气相沉积](https://en.wikipedia.ahmu.cf/wiki/Chemical_vapor_deposition)(CVD)
  - [原子层沉积](https://en.wikipedia.ahmu.cf/wiki/Atomic_layer_deposition)(ALD)
  - [物理气相沉积](https://en.wikipedia.ahmu.cf/wiki/Physical_vapor_deposition)(PVD)
  - [分子束外延](https://en.wikipedia.ahmu.cf/wiki/Molecular_beam_epitaxy)(MBE)
  - 激光剥离（用于[LED](https://en.wikipedia.ahmu.cf/wiki/LED)生产[[32\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-32)）
  - 电化学沉积（ECD）。见[电镀](https://en.wikipedia.ahmu.cf/wiki/Electroplating)
  - [化学机械抛光](https://en.wikipedia.ahmu.cf/wiki/Chemical-mechanical_polishing)(CMP)
  - [晶圆测试](https://en.wikipedia.ahmu.cf/wiki/Wafer_testing)（使用[自动测试设备](https://en.wikipedia.ahmu.cf/wiki/Automatic_Test_Equipment)验证电气性能，也可以在此步骤进行分档和/或[激光微调）](https://en.wikipedia.ahmu.cf/wiki/Laser_trimming)

- 模具准备

  - [硅通孔](https://en.wikipedia.ahmu.cf/wiki/Through-silicon_via)制造（用于[三维集成电路](https://en.wikipedia.ahmu.cf/wiki/Three-dimensional_integrated_circuit)）
  - [晶圆安装（使用切割胶带](https://en.wikipedia.ahmu.cf/wiki/Dicing_tape)将晶圆安装到金属框架上）
  - [晶圆背磨](https://en.wikipedia.ahmu.cf/wiki/Wafer_backgrinding)和抛光[[33\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-33)[ （减少智能卡](https://en.wikipedia.ahmu.cf/wiki/Smartcard)或[PCMCIA 卡](https://en.wikipedia.ahmu.cf/wiki/PCMCIA_card)或晶圆键合和堆叠等薄设备的晶圆厚度，这也可能发生在晶圆切割过程中，称为 Dice Before Grind 或 DBG [[34\] ](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-34)[[35\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-35) )
  - [晶圆键合](https://en.wikipedia.ahmu.cf/wiki/Wafer_bonding)和堆叠（用于[三维集成电路](https://en.wikipedia.ahmu.cf/wiki/Three-dimensional_integrated_circuit)和[微机电系统](https://en.wikipedia.ahmu.cf/wiki/MEMS)）
  - [再分配层](https://en.wikipedia.ahmu.cf/wiki/Redistribution_layer)制造（用于[WLCSP](https://en.wikipedia.ahmu.cf/wiki/Wafer-level_packaging)封装）
  - Wafer Bumping（用于[倒装芯片](https://en.wikipedia.ahmu.cf/wiki/Flip_chip)BGA（[球栅阵列](https://en.wikipedia.ahmu.cf/wiki/Ball_grid_array)）和 WLCSP 封装）
  - 模切或[晶圆切割](https://en.wikipedia.ahmu.cf/wiki/Wafer_dicing)

- 集成电路封装

  - [芯片贴附](https://en.wikipedia.ahmu.cf/wiki/Die_attachment)（使用导电膏或芯片贴膜[[36\] ](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-36)[[37\]](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_device_fabrication#cite_note-37)将芯片贴附在引线框架上）

  - IC 键合：[引线键合](https://en.wikipedia.ahmu.cf/wiki/Wire_bonding)、[热超声键合](https://en.wikipedia.ahmu.cf/wiki/Thermosonic_bonding)、[倒装芯片](https://en.wikipedia.ahmu.cf/wiki/Flip_chip)或[磁带自动键合](https://en.wikipedia.ahmu.cf/wiki/Tape-automated_bonding)(TAB)

  - IC 封装

    或集成散热器 (IHS) 安装

    - 成型（使用可能含有玻璃粉作为填料的特殊成型化合物）
    - 烘烤
    - [电镀](https://en.wikipedia.ahmu.cf/wiki/Electroplating)（在[引线框架的](https://en.wikipedia.ahmu.cf/wiki/Lead_frame)[铜](https://en.wikipedia.ahmu.cf/wiki/Copper)引线上镀锡[，](https://en.wikipedia.ahmu.cf/wiki/Tin)使[焊接](https://en.wikipedia.ahmu.cf/wiki/Soldering)更容易）
    - 激光打标或丝网印刷
    - 修剪和成型（将引线框架彼此分开，并弯曲引线框架的引脚，以便它们可以安装在[印刷电路板上](https://en.wikipedia.ahmu.cf/wiki/Printed_circuit_board)）

- [集成电路测试](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_fabrication#Device_test)

## 封装

在电子制造中，**集成电路封装**是[半导体器件制造](https://en.wikipedia.ahmu.cf/wiki/Fabrication_(semiconductor))的最后阶段，其中[半导体材料块](https://en.wikipedia.ahmu.cf/wiki/Die_(integrated_circuit))被封装在一个支撑外壳中，以防止物理损坏和腐蚀。该外壳称为“[封装](https://en.wikipedia.ahmu.cf/wiki/Semiconductor_package)”，支持将设备连接到电路板的电触点。

### 设计考虑

**电气**

与片上信号相比，从芯片流出、通过封装并进入[印刷电路板(PCB) 的载流迹线具有非常不同的电气特性。](https://en.wikipedia.ahmu.cf/wiki/Printed_circuit_board)它们需要特殊的设计技术，并且比仅限于芯片本身的信号需要更多的电力。因此，用作电触点的材料必须具有低电阻、低电容和低电感等特性。[[1\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit_packaging#cite_note-:02-1)结构和材料都必须优先考虑信号传输特性，同时尽量减少可能对信号产生负面影响的 任何[寄生元素。](https://en.wikipedia.ahmu.cf/wiki/Parasitic_element_(electrical_networks))

随着其他技术开始加速，控制这些特性变得越来越重要。封装延迟有可能占到高性能计算机延迟的近一半，而且这种速度瓶颈预计会增加。

**机械和热**

[集成电路](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit)封装必须能够抵抗物理损坏、防潮，并且还必须提供有效的芯片散热。此外，对于[射频](https://en.wikipedia.ahmu.cf/wiki/RF)应用，封装通常需要屏蔽[电磁干扰](https://en.wikipedia.ahmu.cf/wiki/Electromagnetic_interference)，这可能会降低电路性能或对相邻电路产生不利影响。最后，封装必须允许芯片与[PCB](https://en.wikipedia.ahmu.cf/wiki/Printed_circuit_board)互连。[[1\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit_packaging#cite_note-:02-1)封装材料可以是塑料（[热固性](https://en.wikipedia.ahmu.cf/wiki/Thermosetting_polymer)或[热塑性塑料](https://en.wikipedia.ahmu.cf/wiki/Thermoplastic)）、金属（通常为[Kovar](https://en.wikipedia.ahmu.cf/wiki/Kovar)）或陶瓷。一种常用的[塑料](https://en.wikipedia.ahmu.cf/wiki/Plastic)是[环氧树脂](https://en.wikipedia.ahmu.cf/wiki/Epoxy)-[甲酚](https://en.wikipedia.ahmu.cf/wiki/Cresol)-[酚醛清漆](https://en.wikipedia.ahmu.cf/wiki/Novolak)(ECN)。[[2\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit_packaging#cite_note-2)所有三种材料类型均具有可用的机械强度、耐湿性和耐热性。然而，对于更高端的设备，金属和陶瓷封装通常是首选，因为它们具有更高的强度（也支持更高的引脚数设计）、散热、[密封性能](https://en.wikipedia.ahmu.cf/wiki/Hermetic_seal)或其他原因。一般来说，陶瓷封装比类似的塑料封装要贵。[[3\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit_packaging#cite_note-:1-3)

一些封装具有[金属翅片](https://en.wikipedia.ahmu.cf/wiki/Fin_(extended_surface))以增强热传递，但这些会占用空间。更大的封装还允许更多的互连引脚。

**经济**

成本是选择集成电路封装的一个因素。

### 操作

*芯片连接*是将芯片安装并固定到[封装](https://en.wikipedia.ahmu.cf/wiki/Chip_carrier)或支撑结构（接头）的步骤。[[10\]](https://en.wikipedia.ahmu.cf/wiki/Integrated_circuit_packaging#cite_note-Turner762-10)对于高功率应用，通常使用金锡或金硅[焊料](https://en.wikipedia.ahmu.cf/wiki/Solder)（以实现良好的[热传导）将芯片](https://en.wikipedia.ahmu.cf/wiki/Heat_conduction)[共晶](https://en.wikipedia.ahmu.cf/wiki/Eutectic)键合到封装上。对于低成本、低功耗的应用，通常使用[环氧树脂](https://en.wikipedia.ahmu.cf/wiki/Epoxy)[粘合剂将芯片直接粘合到基板（例如](https://en.wikipedia.ahmu.cf/wiki/Adhesive)[印刷线路板](https://en.wikipedia.ahmu.cf/wiki/Printed_wiring_board)）上。

以下操作在封装阶段执行，分为键合、封装和晶圆键合步骤。请注意，此列表并非包罗万象，并且并非对每个包都执行所有这些操作

- IC键合
  - [引线键合](https://en.wikipedia.ahmu.cf/wiki/Wire_bonding)
  - [热超声键合](https://en.wikipedia.ahmu.cf/wiki/Thermosonic_Bonding)
  - [向下粘合](https://en.wikipedia.ahmu.cf/w/index.php?title=Down_bonding&action=edit&redlink=1)
  - [胶带自动粘合](https://en.wikipedia.ahmu.cf/wiki/Tape_automated_bonding)
  - [倒装芯片](https://en.wikipedia.ahmu.cf/wiki/Flip_chip)
  - [被子包装](https://en.wikipedia.ahmu.cf/wiki/Quilt_packaging)
  - [贴膜](https://en.wikipedia.ahmu.cf/w/index.php?title=Film_attaching&action=edit&redlink=1)
  - [垫片连接](https://en.wikipedia.ahmu.cf/w/index.php?title=Spacer_attaching&action=edit&redlink=1)
- IC封装
  - [烘烤](https://en.wikipedia.ahmu.cf/wiki/Curing_(chemistry))
  - [电镀](https://en.wikipedia.ahmu.cf/wiki/Plating)
  - [激光打标](https://en.wikipedia.ahmu.cf/wiki/Lasermarking)
  - [修剪和成型](https://en.wikipedia.ahmu.cf/w/index.php?title=Trim_and_form&action=edit&redlink=1)
- [晶圆键合](https://en.wikipedia.ahmu.cf/wiki/Wafer_bonding)
