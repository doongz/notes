# POSIX

来源：[posix是什么都不知道，还好意思说你懂Linux？](https://zhuanlan.zhihu.com/p/392588996)

Linux开发者越来越多，但是仍然有很多人整不明白POSIX是什么。本文就带着大家来了解一下到底什么是POSIX，了解他的历史和重要性。

## 一、什么是posix？

### 1. 概念

POSIX：可移植操作系统接口（Portable Operating System Interface of UNIX，缩写为 POSIX ），

### 2. 发布者-IEEE

发布者为电气与电子工程师协会（Institute of Electrical and Electronics Engineers），简称IEEE。这个协会老牛了【该组织在太空、计算机、电信、生物医学、电力及消费性电子产品等领域中都是主要的权威】！

![img](https://pic3.zhimg.com/80/v2-6f4988ef499204750080210070b785a6_720w.jpg)

POSIX是IEEE为要在各种UNIX操作系统上运行的软件而定义的一系列API标准的总称，其正式称呼为IEEE 1003，而国际标准名称为ISO/IEC 9945。

POSIX.1 已经被国际标准化组织（International Standards Organization，ISO）所接受，被命名为 ISO/IEC 9945-1:1990 标准。

> IEEE，总部位于美国纽约，是一个国际性的电子技术与信息科学工程师的协会，也是目前全球最大的非营利性专业技术学会。IEEE致力于电气、电子、计算机工程和与科学有关的领域的开发和研究，在太空、计算机、电信、生物医学、电力及消费性电子产品等领域已制定了1300多个行业标准，现已发展成为具有较大影响力的国际学术组织

### 3. POSIX标准下载

很多人听说了POSIX标准，但标准具体长什么样，在哪里下载到，则 不清楚。现在我开放出来，供相关人员使用。

Single UNIX Specification V3，IEEE Std 1003.1,2004 Edition

标准线上地址： [http://www.unix.org/version3/online.html](https://link.zhihu.com/?target=http%3A//www.unix.org/version3/online.html) 注册后可以在线阅读或者下载。

IEEE和Open Group 的POSIX认证： [http://www.opengroup.org/certification/idx/posix.html](https://link.zhihu.com/?target=http%3A//www.opengroup.org/certification/idx/posix.html)

相关页面： [http://www.unix.org/version3/ieee_std.html](https://link.zhihu.com/?target=http%3A//www.unix.org/version3/ieee_std.html)

## 二、POSIX历史

### 1. 起源

POSIX是Unix的标准。

1974年，贝尔实验室正式对外发布Unix。因为涉及到反垄断等各种原因，加上早期的Unix不够完善，于是贝尔实验室以慷慨的条件向学校提供源代码，所以Unix在大专院校里获得了很多支持并得以持续发展。

于是出现了好些独立开发的与Unix基本兼容但又不完全兼容的OS，通称Unix-like OS。

包括：

1. 美国加州大学伯克利分校的Unix4.xBSD(Berkeley Software Distribution)。
2. 贝尔实验室发布的自己的版本，称为System V Unix。
3. 其他厂商的版本，比如Sun Microsystems的Solaris系统,则是从这些原始的BSD和System V版本中衍生而来。



![img](https://pic4.zhimg.com/80/v2-1db5303ab0d529f7ff4922af843dd09f_720w.jpg)

20世纪80年代中期，Unix厂商试图通过加入新的、往往不兼容的特性来使它们的程序与众不同。

局面非常混乱，麻烦也就随之而来了。

为了提高兼容性和应用程序的可移植性，阻止这种趋势， IEEE(电气和电子工程师协会)开始努力标准化Unix的开发，后来由 Richard Stallman命名为“Posix”。

**这套标准涵盖了很多方面，比如Unix系统调用的C语言接口、shell程序和工具、线程及网络编程**。

### 2. 谁遵循这个标准呢？

首先就是大名鼎鼎的Unix和Linux了，

![img](https://pic1.zhimg.com/80/v2-d5f7eaef431eb3db068a3129bd71e740_720w.jpg)



除此之外还有苹果的操作系统也是Unix-based的。

![img](https://pic4.zhimg.com/80/v2-195590e42164da5eb6a516d89f1d63eb_720w.jpg)



有了这个规范，你就可以调用通用的API了，Linux提供的POSIX系统调用在Unix上也能执行，因此学习Linux的底层接口最好就是理解POSIX标准。

![img](https://pic2.zhimg.com/80/v2-e4be3158d8123f353cb59902c9e8a0b1_720w.jpg)

Windows从WinNT开始就有兼容POSIX的考虑。这是因为当年在要求严格的领域，Unix地位比Windows高。为了把Unix用户拉到Windows阵营，被迫支持POSIX。

现在Win10对 Linux/POSIX 支持好，则是因为Linux已经统治了廉价服务器市场。为了提高Windows的竞争力搞的。

所以一切都是以市场为主导。

### 3. 支持POSIX-Linux成功的最重要一个因素

Linux之所以能够成功，有很多因素，但是支持POSIX标准无疑是它能够快速发展的最重要的一个因素。

POSIX 标准的制定最后投票敲定阶段大概是 1991~1993 年间，而此时正是Linux 刚刚起步的时候，这个 UNIX 标准为 Linux 提供了极为重要的信息，使得 Linux 能够在标准的指导下进行开发，并能够与绝大多数 UNIX 操作系统兼容。

在最初的 Linux 内核源码（0.01版、0.11版）中就已经为 Linux 系统与 POSIX 标准的兼容做好了准备工作。

在 Linux 0.01 版内核 /include/unistd.h 文件中就已经定义了几个有关 POSIX 标准要求的符号常数，而且 Linus 在注释中已写道：“OK，这也许是个玩笑，但我正在着手研究它呢”。

正是由于Linux支持POSIX标准，无数可以在unix上运行的程序都陆续的移植到Linux上，而此时unix因为版权问题，官司打的不可开交，使得Linux后来者居上。

**时也命也！**

下面是祖师爷Linus当年申请POSIX标准的邮件：

```
来自： torvalds@klaava.Helsinki.Fi（林纳斯·托瓦兹）
讨论组： comp.os.minix
主题： Gcc-1.40和一个有关POSIX的问题
信息名称： 1991 Jul 3, 100050.9886@klaava.Helsinki.Fi
日期： 1991年7月3日， 格林威治时间10： 00： 50
各位网友好！
由于我现在正在MINIX系统下做一个项目， 对POSIX标准很感兴趣。 有谁能向我提供
一个（最好） 是机器可读形式的最新的POSIX规则？ 能有FTP地址就更好了。
```

![img](https://pic2.zhimg.com/80/v2-1a53c0b66adff874b267dc622649ea55_720w.jpg)

而Linus也在《知识为了好玩》中讲述了POSIX的重要性：

```text
POSIX标准是一个可以适用于数以百计的UNIX系统呼叫中的任意一个的一套冗长规则， 计算机要执行任务（从读、 写、 开机和关机开始） 就需要这个标准。 

POSIX则是指一个UNIX的标准体系， 或一个由来自不同公司的代表所组成的一个组织， 希望按照一个共同的标准进行运作。 对于程序员开发的在该操作系统下的新应用软件或开发应用软件的新版本而言， 标准是极其重要的。 从POSIX这样的系统呼叫（system call） ， 尤其是重要的呼叫（call） 中， 我可以获得一个操作系统应该具有哪些功能的一个单子； 然后我就可以通过自己的方式在自己的系统中实现每一个功能。 通过编写出这些标准， 我的系统软件的源代码将可以被别人使用， 以开发新的应用软件。

当时我并不知道我本可以直接从POSIX公司买到这些规则的软盘， 但这无所谓。 哪怕我能买得起， 什么东西运到芬兰， 往往会需要很长的时间。 我不愿等上那么久， 因此我四处搜求一个能从FTP地址上直接下载的版本。

没有人给我提供能找到POSI标准的来源。 于是我开始了计划B。

我从学校找到运行sun器(sun server)的sun微系统版的UNIX手册。 该手册中有一个完全可以凑合使用的系统呼叫的基本版本。 从用户手册中能看出系统呼叫的主要功能， 以及为完成这些功能所需要完成的步骤。 但是， 从中看不出具体的方法， 而只是标明了最终的结果。 于是我便着手从安德鲁·塔南鲍姆的书中和别的材料中收集一些系统呼叫。 

最终有人给我寄来了那几卷厚厚的POSIX标准。
```

## 三、可移植性

聊到POSIX，那我们就不得不说说到底什么是可移植性，在讲可移植性之前，我们先来了解库函数和系统调用的区别。

Linux下对文件操作有两种方式：系统调用（system call）和库函数调用（Library functions）。

### 1. 系统调用

系统调用是通向操作系统本身的接口，是面向底层硬件的。通过系统调用，可以使得用户态运行的进程与硬件设备(如CPU、磁盘、打印机等)进行交互，是操作系统留给应用程序的一个接口。

### 2. 库函数

库函数（Library function）是把函数放到库里，供别人使用的一种方式。

方法是把一些常用到的函数编完放到一个文件里，供不同的人进行调用。一般放在.lib文件中。

库函数调用则是面向应用开发的，库函数可分为两类，

1. 一类是C语言标准规定的库函数，
2. 一类是编译器特定的库函数。

(由于版权原因，库函数的源代码一般是不可见的，但在头文件中你可以看到它对外的接口)。

![img](https://pic1.zhimg.com/80/v2-a7967d7e22e948e07d4e45de7486070c_720w.jpg)

glibc 是 Linux 下使用的开源的标准 C 库，它是 GNU 发布的 libc 库，即运行时库。这些基本函数都是被标准化了的，而且这些函数通常都是用汇编直接实现的。

glibc 为程序员提供丰富的 API（Application Programming Interface），这些API都是遵循POSIX标准的，API的函数名，返回值，参数类型等都必须按照POSIX标准来定义。

**POSIX兼容也就指定这些接口函数兼容，但是并不管API具体如何实现。**

### 3. 库函数API和系统调用的区别

![img](https://pic4.zhimg.com/80/v2-3a61e1a67e92a89bd5a4e5f050ee406f_720w.jpg)

如上图所示：

- (1) 库函数是语言或应用程序的一部分，而系统调用是内核提供给应用程序的接口，属于系统的一部分
- (2) 库函数在用户地址空间执行，系统调用是在内核地址空间执行，库函数运行时间属于用户时间，系统调用属于系统时间，库函数开销较小，系统调用开销较大
- (3) 系统调用依赖于平台，库函数并不依赖

![img](https://pic1.zhimg.com/80/v2-992cba1f5d83d0875e501d78ffdd1608_720w.jpg)

**系统调用是为了方便使用操作系统的接口，而库函数则是为了人们编程的方便。**

**库函数调用与系统无关，不同的系统，调用库函数，库函数会调用不同的底层函数实现，因此可移植性好。**

### 4. 程序的可移植性及其本质

**那么目标代码和启动代码是怎么生成的呢？ 答案是编译器**。

**编程语言编写的程序首先要被编译器编译成目标代码（0、1代码），然后在目标代码的前面插入启动代码，最终生成了一个完整的程序**。

> 要注意的是，程序中为访问特定设备（如显示器）或者操作系统（如windows xp 的API)的特殊功能而专门编写的部分通常是不能移植的。

综上所述，一个编程语言的可移植性取决于

1. 不同平台编译器的数量
2. 对特殊硬件或操作系统的依赖性

移植是基于操作系统的。但是这个时候，我们需要注意一点：**基于各种操作系统平台不同，应用程序在二级制级别是不能直接移植的**。

我们只能在代码层去思考可移植问题，在API层面上由于各个操作系统的命名规范、系统调用等自身原因，在API层面上实现可移植也是不大可能的。

在各个平台下，我们默认C标准库中的函数都是一样的，这样基本可以实现可移植。但是对于C库本身而言，在各种操作系统平台下其内部实现是完全不同的，也就是说C库封装了操作系统API在其内部的实现细节。

因此，**C语言提供了我们在代码级的可移植性，即这种可移植是通过C语言这个中间层来完成的**。

例如在我们的代码中下功夫。以下代码可以帮助我们实现各平台之间的可移植：

```text
#ifdef _WINDOWS_
       CreateThread();      //windows下线程的创建
#else
       Pthread_create();    //Linux下线程的创建
#endif
```

对于头文件，也使用同样的预编译宏来实现。如：

```text
#ifndef _WINDOWS_
       #include <windows.h>
#else
       #include <thread.h>
#endif
```

这样就可以实现代码的可移植了。在编译的时候只要通过#define就可以选择在那个平台下完成程序的编译。

综上所述，我们都是将C，C++等各种语言当作中间层，以实现其一定程度上的可移植。如今，语言的跨平台的程序都是以这样的方式实现的。但是在不同的平台下，仍需要重新编译。

### 5. 系统开销

使用系统调用会影响系统的性能，在执行调用时的从用户态切换到内核态，再返回用户态会有系统开销。

为了减少开销，因此需要**减少系统调用的次数**，并且让**每次系统调用尽可能的完成多的任务**。

硬件也会限制对底层系统调用一次所能写的数据块的大小。

为了给设备和文件提供更高层的接口，Linux系统提供了一系列的标准函数库。

使用标准库函数，可以高效的写任意长度的数据块，库函数在数据满足数据块长度要求时安排执行底层系统调用。

一般地，操作系统为了考虑实现的难度和管理的方便，它只提供一少部分的系统调用，这些系统调用一般都是由C和汇编混合编写实现的，其接口用C来定义，而具体的实现则是**汇编**，这样的**好处就是执行效率高**，而且，极大的方便了上层调用。

随着系统提供的这些库函数把系统调用进行封装或者组合，可以实现更多的功能，这样的库函数能够实现一些对内核来说比较复杂的操作。

比如，read()函数根据参数，直接就能读文件，而背后**隐藏的比如文件在硬盘的哪个磁道，哪个扇区，加载到内存的哪个位置等等这些操作**，程序员是不必关心的，这些操作里面自然也包含了系统调用。

而对于第三方的库，它其实和系统库一样，只是它直接利用系统调用的可能性要小一些，而是利用系统提供的API接口来实现功能(API的接口是开放的)。

## 四、举例：Linux系统调用

如下图是Linux系统调用的大概流程。

当应用程序调用printf()函数时，printf函数会调用C库中的printf，继而调用C库中的write，C库最后调用内核的write()。

而另一些则不会使用系统调用，比如strlen, strcat, memcpy等。

![img](https://pic4.zhimg.com/80/v2-7f5eb3c97342632b5975493cbdd45b9f_720w.jpg)



printf函数执行过程中，程序运行状态切换如下：

```text
用户态–>系统调用–>内核态–>返回用户态
```

printf函数、glibc库和系统调用在系统中关系图如下：

![img](https://pic3.zhimg.com/80/v2-a8315ef7d9a895bb4649fe3cd6f3e96a_720w.jpg)



实例代码如下：

```c
  1 #include <stdio.h>
  2 
  3 
  4 int main(int argc, char **argv)
  5 {
  6     printf(yikoulinux);   
  7     return 0;
  8 }   
```

编译执行

```text
root@ubuntu:/home/peng/test# gcc 123.c -o run
root@ubuntu:/home/peng/test# strace ./run
```



![img](https://pic4.zhimg.com/80/v2-4a6b1b885510374f17e22bea8a725a5b_720w.jpg)

如执行结果可知： 我们的程序虽然只有一个printf函数，但是在执行过程中，我们前后调用了execve、access、open、fstat、mmap、brk、write等系统调用。 其中write系统调用会把字符串：yikoulinux通过设备文件1，发送到驱动，该设备节点对应终端stdout。

![img](https://pic2.zhimg.com/80/v2-3387b06c17199dd7cb4849f4ebde6ebd_720w.jpg)

【注意】运行程序前加上strace，可以追踪到函数库调用过程