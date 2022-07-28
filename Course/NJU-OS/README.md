# 南京大学 操作系统：设计与实现 (2022 春季学期) 

授课老师：蒋炎岩

课程链接：[http://jyywiki.cn/OS/2022/ ](http://jyywiki.cn/OS/2022/ )

视频课：[https://space.bilibili.com/202224425/video](https://space.bilibili.com/202224425/video)

教科书：[https://pages.cs.wisc.edu/~remzi/OSTEP/](https://pages.cs.wisc.edu/~remzi/OSTEP/)



按照并发 → 虚拟化 → 持久化的顺序上课 (我自己的理解)

## 一、课程概述

### 什么是操作系统？

操作系统是一个典型的 “system”——它完成对计算机硬件系统的抽象，提供应用程序的运行环境：

- 从应用程序的视角看，操作系统定义了一系列的对象 (进程/线程、地址空间、文件、设备……) 和操纵它们的 API (系统调用)。这组强大的 API 把计算机的硬件资源有序地管理起来，它不仅能实现应用程序 (浏览器、游戏……)，还支持着各类神奇的系统程序 (容器、虚拟机、调试器、游戏外挂……)
- 从硬件的视角看，操作系统是一个拥有访问全部硬件功能的程序 (操作系统就是个 C 程序，不用怕)。硬件会帮助操作系统完成最初的初始化和加载，之后，操作系统加载完第一个程序后，从此作为 “中断处理程序” 在后台管理整个计算机系统

### 课程组织

操作系统使用正确的抽象使构造庞大的计算机软件/硬件生态从不可能变为可能。这门课围绕操作系统是如何设计 (应用程序视角)、怎样实现 (硬件视角) 两个角度展开，分为两个主要部分：

- 原理课 (并发/虚拟化/持久化)：以教科书内容为主，介绍操作系统的原理性内容。课程同时注重讲解操作系统相关的代码实现和编程技巧，包括操作系统中常用的命令行/代码工具、教学操作系统 xv6 的代码讲解等
- 理解操作系统最重要的实验部分
    - Mini labs (应用程序视角；设计)：通过实现一系列有趣的 (~~黑科技~~) 代码理解操作系统中对象存在的意义和操作系统 API 的使用方法、设计理念
    - OS labs (计算机硬件视角；实现)：基于一个简化的硬件抽象层实现多处理器操作系统内核，向应用程序提供一些基础操作系统 API

### 前导知识

这是一门强调 “编程” 的硬核课程。不畏惧且能够写出能够正确工作的代码对理解操作系统来说至关重要的：

> *Talk is cheap. Show me the code.*——Linus Torvalds

因此，我们预期这门课的听众已经能够在操作系统上利用 API 编程，并对计算机硬件提供的机制有一定了解。具体来说，我们假设课程的听众：

1. 掌握 C 语言编程的技术和技巧，包括一定规模代码的编写、测试方法和调试工具的使用方法
2. 熟悉至少一个指令集 (包括应用和系统指令)，包括但不限于 x86, MIPS, 或 RISC-V
3. 达到上述两个要求可以通过独立完成《计算机系统基础》课程中附带的 NEMU 模拟器实验实现

如果你觉得自己的编程基础还没能过关 (例如调试中等规模代码时找不到头绪)，请参考我们准备的[生存指南](http://jyywiki.cn/OS/OS_Guide)。

## 二、教科书与参考资料

> 关于读书和入门：如果你有读过觉得非常好，值得进入推荐列表，请告诉 jyy！如果你有不同意见，例如强烈反对推荐，也请联系 jyy！作为一个过来人，jyy 的建议是多读书：
>
> - 计算机系统中的很多知识是关联的，因此你对体系结构、编译器、软件工程等领域的理解都会加深对操作系统的理解；反之也一样。认识通常是 “螺旋式上升” 的；
> - 计算机系统不是纸上谈兵，因此学习很多技术是非常重要的，例如如何使用 Linux 系统调用编程、如何使用正则表达式、如何使用 profiler 等等。技术类书籍是掌握这些实践的很好切入点；
> - 每一本书的作者都有他们独到的视角 (某些为了凑数编教材而编教材的除外)。因此也许某个作者的思维方式就特别适合你，读起来就会很轻松。
>
> 当然我们已经尽量为你选择了一些经过了 (一定) 考验的好书。

### 教科书

- [OSTEP] Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau. *[Operating Systems: Three Easy Pieces](http://pages.cs.wisc.edu/~remzi/OSTEP/)*. Arpaci-Dusseau Books, 2018. 

- [CSAPP] Randal E. Bryant and David R. O'Hallaron. *Computer Systems: A Programmer's Perspective* (3ed). Pearson, 2017. (作为手册和参考书查阅) 

### 参考资料

#### UNIX/Linux

- Jlevy Hollowa. [*The Art of Command Line*](https://github.com/jlevy/the-art-of-command-line).
- Gerard Beekmans. [Linux from Scratch](http://linuxfromscratch.org/).
- Harley Hahn. *[Harley Hahn's Guide to Unix and Linux](http://www.harley.com/books/sg3.html)*. McGraw-Hill Higher Education, 2008.
- Michael Kerrisk. *The Linux Programming Interface: A Linux and UNIX System Programming Handbook*. No Starch Press, 2010.
- W. Richard Stevens and Stephen A. Rago. *[Advanced Programming in the UNIX® Environment](http://www.apuebook.com/apue3e.html)* (3rd Edition). Addison-Wesley, 2013.

#### 编程

- Brian W. Kernighan and Dennis M. Ritchie. *The C programming language* (2nd Edition). Prentice Hall, 1998.
- [The CERT C Coding Standard: Rules for Developing Safe, Reliable, and Secure Systems](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard). Software Engineering Institute of Carnegie Mellon University, 2016.
- Sandeep.S. *[GCC-Inline-Assembly-HOWTO](http://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html)*, 2003.

#### 操作系统设计与实现

- 陈海波、夏虞斌. *[现代操作系统：原理与实现](http://ipads.se.sjtu.edu.cn/mospi/)*. 机械工业出版社, 2020.
- John R. Levine. *[Linkers and Loaders](https://linker.iecc.com/)*. Morgan-Kauffman, 1999.
- Robert Love. *Linux Kernel Development: A Thorough Guide to the Design and Implementation of the Linux Kernel* (3rd Edition). Addison-Wesley, 2010.
- Marshall Kirk McKusick, Keith Bostic, Michael J. Karels, and John S. Quarterman. *[The Design and Implementation of the 4.4BSD Operating System](https://www.freebsd.org/doc/en/books/design-44bsd/book.html)*. Addison-Wesley Longman, 1996.

#### 开源操作系统实现

- [xv6](https://pdos.csail.mit.edu/6.828/2018/xv6.html)，十分精简优美的 UNIX 实现
- [Plan 9](https://9p.io/plan9/)，来自 Bell Labs 的著名原型操作系统
- [seL4](https://sel4.systems/)，在抽象层上构建安全的微内核操作系统内核
- [Fuchsia](https://fuchsia.googlesource.com/)，Google 的微内核操作系统，基于 Zircon 微内核
- [OpenHarmony](https://gitee.com/openharmony)，“鸿蒙” 操作系统
- [Linux Kernel](https://www.kernel.org/)，巨无霸项目 (新手请绕行)
- [Android Open Source Project (AOSP)](https://source.android.com/)，Android 系统栈

#### Finally, The Friendly Manual

- Linux manpages (tldr, man, info, ...): [man7.org](https://www.man7.org/)
- [Bourne-Again Shell (bash)](https://www.gnu.org/software/bash/manual/html_node/index.html)
- [GNU Compiler Collection (GCC)](https://gcc.gnu.org/onlinedocs/)
- [GNU Debugger (gdb)](https://sourceware.org/gdb/documentation/)
- [Binutils (ld, as, objdump, and more)](https://sourceware.org/binutils/docs/)
- [GNU Make](https://www.gnu.org/software/make/manual/html_node/index.html)
- 现在 jyy 真的已经觉得这些文档很 friendly 了 (这可以看作是评价 “system maturity” 的一条标准，类似 “[mathematical maturity](https://blogs.ams.org/matheducation/2019/04/15/precise-definitions-of-mathematical-maturity/)”)
