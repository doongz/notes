# Android 构架

# Android 架构

来源：[https://source.android.com/devices/architecture](https://source.android.com/devices/architecture)

## 一、Android 系统架构

Android 系统架构包含以下组件：

![IMG_7653](./doc/IMG_7653.PNG)

**图 1.** Android 系统架构

- **应用框架**。应用框架最常被应用开发者使用。作为硬件开发者，您应该非常了解开发者 API，因为很多此类 API 都可以直接映射到底层 HAL 接口，并可提供与实现驱动程序相关的实用信息。
- **Binder IPC**。Binder 进程间通信 (IPC) 机制允许应用框架跨越进程边界并调用 Android 系统服务代码，这使得高级框架 API 能与 Android 系统服务进行交互。在应用框架级别，开发者无法看到此类通信的过程，但一切似乎都在“按部就班地运行”。
- **系统服务**。系统服务是专注于特定功能的模块化组件，例如窗口管理器、搜索服务或通知管理器。应用框架 API 所提供的功能可与系统服务通信，以访问底层硬件。Android 包含两组服务：“系统”（诸如窗口管理器和通知管理器之类的服务）和“媒体”（涉及播放和录制媒体的服务）。
- **硬件抽象层 (HAL)**。HAL 可定义一个标准接口以供硬件供应商实现，这可让 Android 忽略较低级别的驱动程序实现。借助 HAL，您可以顺利实现相关功能，而不会影响或更改更高级别的系统。HAL 实现会被封装成模块，并会由 Android 系统适时地加载。如需了解详情，请参阅[硬件抽象层 (HAL)](https://source.android.com/devices/architecture/hal)。
- **Linux 内核**。开发设备驱动程序与开发典型的 Linux 设备驱动程序类似。Android 使用的 Linux 内核版本包含一些特殊的补充功能，例如低内存终止守护进程（一个内存管理系统，可更主动地保留内存）、唤醒锁定（一种 [`PowerManager`](https://developer.android.com/reference/android/os/PowerManager.html) 系统服务）、Binder IPC 驱动程序，以及对移动嵌入式平台来说非常重要的其他功能。这些补充功能主要用于增强系统功能，不会影响驱动程序开发。您可以使用任意版本的内核，只要它支持所需功能（如 Binder 驱动程序）即可。不过，我们建议您使用 Android 内核的最新版本。如需了解详情，请参阅[构建内核](https://source.android.com/setup/building-kernels)一文。

## 二、HAL 接口定义语言（AIDL/HIDL）

Android 8.0 重新设计了 Android 操作系统框架（在一个名为“Treble”的项目中），以便让制造商能够以更低的成本更轻松、更快速地将设备更新到新版 Android 系统。在这种新架构中，HAL 接口定义语言（HIDL，发音为“hide-l”）指定了 HAL 和其用户之间的接口，让用户无需重新构建 HAL，就能替换 Android 框架。在 Android 10 中，HIDL 功能已整合到 AIDL 中。此后，HIDL 就被废弃了，并且仅供尚未转换为 AIDL 的子系统使用。

**注意**：如需详细了解 Treble 计划，请参阅开发者博文 [Treble 现已推出：Android 的模块化基础](https://android-developers.googleblog.com/2017/05/here-comes-treble-modular-base-for.html)和[借助 Treble 项目更快速地采用新系统](https://android-developers.googleblog.com/2018/05/faster-adoption-with-project-treble.html)。

利用新的供应商接口，Treble 将供应商实现（由芯片制造商编写的设备专属底层软件）与 Android 操作系统框架分离开来。供应商或 SOC 制造商构建一次 HAL，并将其放置在设备的 `/vendor` 分区中；框架可以在自己的分区中通过[无线下载 (OTA) 更新](https://source.android.com/devices/tech/ota)进行替换，而无需重新编译 HAL。

旧版 Android 架构与当前基于 HIDL 的架构之间的区别在于对供应商接口的使用：

- Android 7.x 及更低版本中没有正式的供应商接口，因此设备制造商必须更新大量 Android 代码才能将设备更新到新版 Android 系统：

![IMG_7655](./doc/IMG_7655.PNG)

- Android 8.0 及更高版本提供了一个稳定的新供应商接口，因此设备制造商可以访问 Android 代码中特定于硬件的部分，这样一来，设备制造商只需更新 Android 操作系统框架，即可跳过芯片制造商直接提供新的 Android 版本：

![IMG_7656](./doc/IMG_7656.PNG)



所有搭载 Android 8.0 及更高版本的新设备都可以利用这种新架构。为了确保供应商实现的向前兼容性，供应商接口会由[供应商测试套 (VTS)](https://source.android.com/devices/tech/vts) 进行验证，该套件类似于[兼容性测试套件 (CTS)](https://source.android.com/compatibility/cts)。您可以使用 VTS 在旧版 Android 架构和当前 Android 架构中自动执行 HAL 和操作系统内核测试。

## 三、架构资源

要详细了解 Android 架构，请参阅以下部分：

- [HAL 类型](https://source.android.com/devices/architecture/hal-types)：介绍了绑定式 HAL、直通式 HAL、Same-Process (SP) HAL 和旧版 HAL。
- [AIDL](https://source.android.com/devices/architecture/aidl/overview)：有关 AIDL 的文档（不论是广泛使用还是用作 HAL 接口）。
- [HIDL（一般信息）](https://source.android.com/devices/architecture/hidl)：包含与 HAL 和其用户之间的接口有关的一般信息。
- [HIDL (C++)](https://source.android.com/devices/architecture/hidl-cpp)：包含关于为 HIDL 接口创建 C++ 实现的详情。
- [HIDL (Java)](https://source.android.com/devices/architecture/hidl-java)：包含关于 HIDL 接口的 Java 前端的详情。
- [ConfigStore HAL](https://source.android.com/devices/architecture/configstore)：介绍了可供访问 Android 框架只读配置项的 API。
- [设备树叠加层](https://source.android.com/devices/architecture/dto)： 详细说明了如何在 Android 中使用设备树叠加层 (DTO)。
- [供应商原生开发套件 (VNDK)](https://source.android.com/devices/architecture/vndk)：介绍了一组可供实现供应商 HAL 的供应商专用库。
- [供应商接口对象 (VINTF)](https://source.android.com/devices/architecture/vintf)：介绍了可收集设备的相关信息并通过可查询 API 提供这些信息的对象。
- [SELinux for Android 8.0](https://source.android.com/static/security/selinux/images/SELinux_Treble.pdf)：详细介绍了 SELinux 变更和自定义。

除了本网站上的资源之外，Treble 团队成员还发表了 [Treble：通过在全球分布的利益相关方的活跃软件生态系统中建立平衡来实现快速的软件更新](https://dl.acm.org/doi/10.1145/3358237)。ACM 会员可以免费阅读这篇论文，而非会员可以购买或阅读摘要。









## 一些其他的概述

参考：http://c.biancheng.net/view/2891.html

Android系统构架是安卓系统的体系结构，android的系统架构和其操作系统一样，采用了分层的架构，共分为四层，从高到低分别是:

- Android应用层
- Android应用框架层
- Android系统运行库层
- Linux内核层

Android系统构架主要应用于ARM平台，但不仅限于ARM，通过编译控制，在X86、MAC等体系结构的机器上同样可以运行。

![](../doc/a-1.png)

### 1、应用程序层

Android 装配了一个核心应用程序集合，包括 E-mail 客户端、SMS 短消息程序、日历、地图、浏览器、联系人管理程序和其他程序，所有应用程序都是用 Java 编程语言编写的。

用户开发的 Android 应用程序和 Android 的核心应用程序是同一层次的，它们都是基于 Android 的系统 API 构建的。

### 二、应用程序框架层

应用程序的体系结构旨在简化组件的重用，任何应用程序都能发布它的功能且任何其他应用程序都可以使用这些功能（需要服从框架执行的安全限制），这一机制允许用户替换组件。

开发者完全可以访问核心应用程序所使用的 API 框架。通过提供开放的开发平台，Android 使开发者能够编制极其丰富和新颖的应用程序。开发者可以自由地利用设备硬件优势访问位置信息、运行后台服务、设置闹钟、向状态栏添加通知等。

所有的应用程序都是由一系列的服务和系统组成的，主要包括以下几种：

- 视图（View）
  - 这里的视图指的是丰富的、可扩展的视图集合，可用于构建一个应用程序，包括列表 (Lists)、网格 (Grids)、文本框 (TextBoxes)、按钮 (Buttons)，甚至是内嵌的 Web 浏览器。
- 内容管理器（Content Provider）
  - 内容管理器使得应用程序可以访问另一个应用程序的数据（如联系人数据库）或者共享自己的数据。
- 资源管理器（Resource Manager）
  - 资源管理器提供访问非代码资源，如本地字符串、图形和分层文件 (layout files)。
- 通知管理器（Notification Manager）
  - 通知管理器使得所有的应用程序都能够在状态栏显示通知信息。
- 活动管理器（Activity Manager）
  - 在大多数情况下，每个 Android 应用程序都运行在自己的 Linux 进程中。当应用程序的某些代码需要运行时，这个进程就被创建并一直运行下去，直到系统认为该进程不再有用为止，然后系统将回收该进程占用的内存以便分配给其他的应用程序。活动管理器管理应用程序生命周期，并且提供通用的导航回退功能。

### 3、系统库

Android 本地框架是由 C/C++ 实现的，包含 C/C++ 库，以供 Android 系统的各个组件使用。这些功能通过 Android 的应用程序框架为开发者提供服务。

这里只介绍 C/C++ 库中的一些核心库

| 名称        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| 系统C语言库 | 标准C语言系统库 (libc) 的 BSD 衍生，调整为基于嵌入式 Linux 设备。 |
| 媒体库      | 基于 PacketVideo 的 OpenCORE，这些库支持播放和录制许多流行的音频和视频格式，以及静态图像文件，包括 MPEG4、H.264、MP3、AAC、AMR、JPG、PNG。 |
| 界面管理    | 管理访问显示子系统，并且为多个应用程序提供 2D 和 3D 图层的无缝融合。 |
| LibWebCore  | 新式的 Web 浏览器引擎，支持 Android 浏览器和内嵌的 Web 视图。 |
| SGL         | 一个内置的 2D 图形引擎。                                     |
| 3D 库       | 基于 OpenGL ES 1.0 APIs 实现，该库可以使用硬件 3D 加速或包含高度优化的 3D 软件光栅。 |
| FreeType    | 位图和矢量字体显示渲染。                                     |
| SQLite      | SQLite 是一个所有应用程序都可以使用的强大且轻量级的关系数据库引擎。 |

#### Android 运行环境

Android 包含一个核心库的集合，该核心库提供了 Java 编程语言核心库的大多数功能。几乎每一个 Android 应用程序都在自己的进程中运行，都拥有一个独立的 Dalvik 虚拟机实例。

Dalvik 是 Google 公司自己设计的用于 Android 平台的 Java 虚拟机。Dalvik 虚拟机是 Google 等厂商合作开发的 Android 移动设备平台的核心组成部分之一，它可以支持已转换为 .dex (Dalvik Executable) 格式的 Java 应用程序的运行。

.dex 格式是专为 Dalvik 设计的一种压缩格式，适合内存和处理器速度有限的系统。

Dalvik 经过优化，允许在有限的内存中同时运行多个虚拟机的实例，并且每一个 Dalvik 应用作为一个独立的 Linux 进程执行。Dalvik 虚拟机依赖 Linux 内核提供基本功能，如线程和底层内存管理。

### 4、Linux内核

Android 基于 Linux 提供核心系统服务，例如安全、内存管理、进程管理、网络堆栈、驱动模型。除了标准的 Linux 内核外，Android 还增加了内核的驱动程序，如Binder (IPC) 驱动、显示驱动、输入设备驱动、音频系统驱动、摄像头驱动、WiFi驱动、蓝牙驱动、电源管理。

Linux 内核也作为硬件和软件之间的抽象层，它隐藏具体硬件细节而为上层提供统一的服务。

分层的好处就是使用下层提供的服务为上层提供统一的服务，屏蔽本层及以下层的差异，当本层及以下层发生了变化时，不会影响到上层，可以说是高内聚、低耦合。

