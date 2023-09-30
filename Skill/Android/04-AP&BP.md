# AP和BP简介

来源：https://www.cnblogs.com/lixuejian/p/16716154.html

大多数手机都至少存在两个处理器，**一个负责AP侧，一个负责BP侧。**

- 数的手机都含有两个处理器。操作系统、用户界面和应用程序都在Application Processor(即AP)（应用处理器）上执行，AP一般采用ARM芯片的CPU。运行在Application Processor(AP)的软件包称为AP包,包括操作系统、用户界面和应用程序等;
- 手机射频通讯控制软件，则运行在另一个分开的CPU上，这个CPU称为Baseband Processor(即BP)（基带处理器）。与Baseband Processor(BP)相关的软件包称为BP包, 包括baseband modem的通信控制软件等.

射频功能放在bp上主要原因：

- 射频控制函数（信号调制、编码、射频为一等）都是与时间高度相关的。最好的办法把这些函数放在一个cpu上执行，并且cpu运行的实时操作os。
- 外一个好处是，bp侧设计认证好了之后，ap侧软件怎么变化，都不影响bp功能。比如通信功能，不会被影响。另外ap侧os和driver相关bug也不会影响bp侧网络。

对于手机开发商，会开发AP和BP两个部分，在刷机时，需要将AP和BP的文件按照开发人员、厂商提供的方式，进行刷机。而非手机业务、通信soc，不会存在BP侧，比如rk、nxp一些音视频、车载、工控的soc。

## AP和BP通信方式

通过查看BP侧代码，会发现文件夹的名字xxxx_proc,可见：二者是通过共享内存来通讯。

BP侧三大基础功能：语音通话、短信等数据通信、以及sim卡管理。AP侧调用BP侧标准的接口TAPI（TELEPHONY API）,实现上述功能。就是我们手机的短信、电话拨号、sim卡管理app等。