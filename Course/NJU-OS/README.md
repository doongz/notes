# 南京大学 操作系统：设计与实现 (2022 春季学期) 

授课老师：蒋炎岩

课程链接：[http://jyywiki.cn/OS/2022/ ](http://jyywiki.cn/OS/2022/ )

视频课：[https://space.bilibili.com/202224425/video](https://space.bilibili.com/202224425/video)

教科书：[https://pages.cs.wisc.edu/~remzi/OSTEP/](https://pages.cs.wisc.edu/~remzi/OSTEP/)

## 课程讲义

按照并发 → 虚拟化 → 持久化的顺序上课

1. [操作系统概述](http://jyywiki.cn/OS/2022/slides/1.slides) | [操作系统上的程序](http://jyywiki.cn/OS/2022/slides/2.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/1) | [[M1\] pstree](http://jyywiki.cn/OS/2022/labs/M1) | [[L0\] amgame](http://jyywiki.cn/OS/2022/labs/L0)
2. 并发 [多处理器编程](http://jyywiki.cn/OS/2022/slides/3.slides) | [理解并发程序执行](http://jyywiki.cn/OS/2022/slides/4.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/2) | [[M2\] libco](http://jyywiki.cn/OS/2022/labs/M2)
3. 并发 [并发控制：互斥](http://jyywiki.cn/OS/2022/slides/5.slides) | [并发控制：同步](http://jyywiki.cn/OS/2022/slides/6.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/3) | [[L1\] pmm](http://jyywiki.cn/OS/2022/labs/L1)
4. 并发 [真实世界的并发编程](http://jyywiki.cn/OS/2022/slides/7.slides) | [并发 Bug 和应对](http://jyywiki.cn/OS/2022/slides/8.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/4)
5. [操作系统的状态机模型](http://jyywiki.cn/OS/2022/slides/9.slides) | [状态机模型的应用](http://jyywiki.cn/OS/2022/slides/10.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/5)
6. 虚拟化 [操作系统上的进程](http://jyywiki.cn/OS/2022/slides/11.slides) | [进程的地址空间](http://jyywiki.cn/OS/2022/slides/12.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/6) | [[M3\] sperf](http://jyywiki.cn/OS/2022/labs/M3) | [[L2\] kmt](http://jyywiki.cn/OS/2022/labs/L2)
7. 虚拟化 [系统调用和 UNIX Shell](http://jyywiki.cn/OS/2022/slides/13.slides) | [C 标准库的实现](http://jyywiki.cn/OS/2022/slides/14.slides) | [随堂测验](http://jyywiki.cn/OS/2022/Midterm) | [阅读材料](http://jyywiki.cn/OS/2022/notes/7)
8. 虚拟化 [A `fork()` in the road](http://jyywiki.cn/OS/2022/slides/15.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/8)
9. 虚拟化 [可执行文件](http://jyywiki.cn/OS/2022/slides/16.slides) | [可执行文件的加载](http://jyywiki.cn/OS/2022/slides/17.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/9) | [[M4\] crepl](http://jyywiki.cn/OS/2022/labs/M4)
10. 虚拟化 [xv6 代码导读](http://jyywiki.cn/OS/2022/slides/18.slides) | [实现上下文切换](http://jyywiki.cn/OS/2022/slides/19.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/10) | [[L3\] uproc](http://jyywiki.cn/OS/2022/labs/L3)
11. 虚拟化 [处理器调度](http://jyywiki.cn/OS/2022/slides/20.slides) | [操作系统设计](http://jyywiki.cn/OS/2022/slides/21.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/11)
12. [极限速通操作系统实验](http://jyywiki.cn/OS/2022/slides/22.slides)
13. 持久化 [存储设备原理](http://jyywiki.cn/OS/2022/slides/23.slides) | [输入输出设备](http://jyywiki.cn/OS/2022/slides/24.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/12)
14. 持久化 [设备驱动程序](http://jyywiki.cn/OS/2022/slides/25.slides) | [文件系统 API](http://jyywiki.cn/OS/2022/slides/26.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/13)
15. 持久化 [FAT 和 UNIX 文件系统](http://jyywiki.cn/OS/2022/slides/27.slides) | [持久数据的可靠性](http://jyywiki.cn/OS/2022/slides/28.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/14) | [[M5\] frecov](http://jyywiki.cn/OS/2022/labs/M5) | [[L4\] vfs](http://jyywiki.cn/OS/2022/labs/L4)
16. 持久化 [xv6 文件系统实现](http://jyywiki.cn/OS/2022/slides/29.slides) | [现代存储系统](http://jyywiki.cn/OS/2022/slides/30.slides) | [阅读材料](http://jyywiki.cn/OS/2022/notes/15)
17. [Android 系统](http://jyywiki.cn/OS/2022/slides/31.slides) | [课程总结](http://jyywiki.cn/OS/2022/slides/32.slides)

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

## 三、生存指南

> 核心指导原则 **Don't Panic. (不要慌)**
>
> 曾经 OSLabs 是一个可怕的传说；但随着 jyy 周目的增加，感觉越来越能在 “挑战性” 与 “趣味性” 之间找到一个让大家活下去的平衡：
>
> - 最优秀的同学也应该感到挑战。在 jyy 读书的时代，“期末翻一遍书就有 95 分” 的课程似乎不能承担大家作为一名 “名校毕业生” 肩负的重任
> - 掉在队伍之后的同学，即便是仅有一定的编程基础，努力过的同学也一定能通过 (Yes!)

但无论如何，还是要花点时间说一下怎么在这门课生存下来，因为**说到底操作系统还是一门十分硬核的编程课**。

### 1. 操作系统为什么难学？

操作系统难学的最主要原因是操作系统里的主题很多，有些主题对大家来说并不太熟悉。例如，同学们到目前为止编写的大部分代码都是串行的，打个比方，就是写一个程序模仿 “一个人”，一次执行一步动作。但操作系统引入了并发编程，也就是你需要协同多个共享内存的 “多个人” 时，会遇到很多你也许意料之外的问题。

在操作系统中，哪怕我们完全不管如何实现 “低延迟、高吞吐的牛逼现代操作系统”，即便是实现一个最小的能工作的操作系统内核，你依然会遇到众多非常具有挑战性的问题：

- 操作系统应该为应用程序提供怎样的 API？
- 如何用硬件实现多个进程的并发/并行？
- 如何编写能够工作的并发程序，它不会在压力负载下随时随地崩溃？
- 如何维持多个隔离的执行流？
- 如何在磁盘上实现持久的数据结构？
- ……

在解决这些问题上作出突出贡献的人已经得过 n 个图灵奖了——每一个问题都不是吃素的。要把这些问题的来龙去脉、解决方法、代码实现都掌握好，的确是相当有挑战性的。

### 2. 操作系统该怎么学？

幸运的是，我们在多年的经验里找到了理解操作系统的两把 “钥匙”，它们分别打开了操作系统的两个侧面。

> 🔑 **“程序眼中的操作系统”：对象 + API**
>
> 操作系统为应用程序提供了执行的基础环境、一系列操作系统对象和操作它们的 API——至少对于今天的操作系统来说，这些东西都是精确定义、触手可及的。我们可以在课堂上通过代码片段、调试工具、日志、trace 等等实在地触摸到操作系统为应用程序提供的一切。
>
> 这就帮助我们理解现代操作系统**设计**背后的思路。

我们会学习真实操作系统中的程序是什么，以及如何借助操作系统提供的 API 为操作系统编程。具体来说，我们的选择是 Linux (准确来说是 POSIX) 作为课程教学的平台，因为它既免费也自由 (能知道它内部的实现)，而且互联网上有丰富的 (英文) 文档。它的设计继承自 “Keep it simple, stupid” 的 UNIX，这个经典的设计背后的动机反而更容易为第一次接触操作系统的初学者所理解。让我们看看它的威力：

- 首先，操作系统里的一切对象都用文件表示 (Everything is a file)。进程、设备……都可以在任何编程语言里用文件 API 访问。
- Linux 的命令行 Shell 是一门编程语言——没错，你每天都在 “编程”！更准确地说，Shell 的功能就是把你想要做的事情 (类似自然语言描述的代码) 翻译成操作系统能看懂的文件/进程管理 API 调用。

这使得我们能用前所未有简便的方式玩转操作系统里的几乎任何东西。你想看看你磁盘的主引导扇区究竟是什么代码？好办，一条命令就行了：

```
cat /dev/sda | head -c 512 | ndisasm -b 16 -
```

你不用阅读太多的手册也能自如地作为一个 “Power User” 使用它。课程中不断会给大家一些有趣的小惊喜，例如为大家展示许多身边工具的代码——它们通常有简易版、读得懂的实现。比如来自早期版本 busybox 的 [vi 实现](https://git.busybox.net/busybox/tree/editors/vi.c?h=1_00_stable) 只有一个文件。虽然这个文件有 3993 行，但你如果使用正确的工具把函数代码折叠起来，你会发现这简单，你也写得出。

包括为了帮助大家更好地理解 UNIX/Linux 操作系统的设计 (即操作系统到底为应用程序提供了什么对象以及操作这些对象的 API)，我们设置了若干 Linux 系统上的 Mini Programming Labs，每个 200 行左右的代码，实际调用 Linux 操作系统 API 完成一些仅使用 C 标准库难以办到的任务。

> 🔑**“硬件眼中的操作系统”：程序 (状态机)**
>
> 如果你完全理解了操作系统中有什么对象、如何操纵它们，就只剩一个问题：你能用计算机硬件提供的机制把这些对象和 API 实现出来吗？实际上，运算和访存指令、I/O、中断/异常和虚存就是我们实现操作系统所需的全部。
>
> 通过阅读代码和调试一个真正的操作系统内核**实现**，我们最终理解操作系统的全部。

UNIX 自诞生以来，就不断有人在模仿——一个成功的例子就是 Linux，在它之上还有或许更为成功的 Android。当然，UNIX 还有更多 “迷你版” 的替代实现，能容易地帮助大家理解代码背后的原理。我们在课堂上选用 [xv6-riscv](http://pdos.csail.mit.edu/6.S081/xv6) 作为讲解操作系统的例子。同时，大家也需要在 Operating System Labs 中，从 “裸机” (bare-metal) 编程开始，自底向上实现一个支持多处理器、文件系统、虚拟存储的迷你操作系统内核。

### 3. 操作系统课中的代码

#### 3.1 迈出第一步

如果你还没有入门，仍然感到恐惧，请记住：坚持住，进入未知领域，**从简单的、能理解的东西试起，投入时间，就有收获**。[参考资料](http://jyywiki.cn/OS/OS_References)中有一些非常棒的入门材料，例如 “Harley Hahn's Guide to Unix and Linux”，引人入胜 (这本书不是写给计算机专业人士的，所以它异常好读且有中文版)。从这里开始，你就能慢慢克服恐惧了。

同样，你可能会对一小段程序 (例如课堂上的示例代码) 感到难以理解。程序难读是很正常的——但程序的运行时状态是好理解的。无非就是数字和指针嘛。请你勇敢地打开你的调试器，设置一个断点，单步执行你的程序。不知道怎么调试？调试的时候没有代码？你需要万能的互联网。

我们为大家准备了一些阅读材料。如果你能在互联网手册得辅助下理解下面的 “自测” 内容，《操作系统》对你来说就是相当合适的！

#### 3.2 自测：C 语言编程

直到今天这门课依然使用 C 语言。在阐述操作系统原理方面，它更简单、包袱更少，也没有很庞大的工具链。虽然说这相当于 “把你的手脚捆起来编程”，但我们通常不需要很复杂的数据结构和代码逻辑，因此现代语言特性的好处在大部分时候并不显著。而且用 C 语言还有一些额外的好处：

- 和其他编程语言相比，C 语言特性更容易真正掌握和深入理解。如果你没有学好，用几周的时间补上应该也没问题
- C 是一种 “高级的汇编语言”，你不难在大脑里把 C 出代码翻译成指令序列；但对于现代语言来说，这要困难得多
- 透过对 C 语言的深入理解，可以更好地理解现代编程语言的设计动机和实现方法

一个例子是 “面向对象”，我们在 C 里也可以实现

```c
struct foo {
  int (*bar)(struct foo *this, int a, int b); // 函数指针
};

void baz() {
  struct foo *ptr = get_object();
  ptr->bar(ptr, 3, 4);
  // 等效于C++: ptr->bar(3, 4)
}
```

而 C++ 里的对象，的确也是这样 (类似) 实现的。如果要实现动态绑定 (用父类的指针调用子类的方法)，我们只需把虚函数的入口放到一张表中，通过查表得到函数实际的入口地址：

```c
struct object_header {
  void **vptr;
};

struct foo {
  struct object_header header;
  ...
};

void baz {
  struct foo *ptr = get_object();
  // ptr->bar(3, 4), dynamic binding
  // INDEX_OF_BAR在编译时由编译器确定
  (int (*)(void *, int, int)) (ptr->header.vptr[INDEX_OF_BAR]) (ptr, 3, 4);
}
```

能理解上述的例子，说明你已经有相当扎实的 C 语言基础了。如果不能，建议大家阅读参考书中推荐的 “The C programming language”。

> #### 思考题：多重继承
>
> C++ 支持多重继承，即一个类可以拥有两个父类。你想到多重继承的实现方法了吗？多重继承的实现是把多个父类同时嵌入进来 (会拥有两个 `header`)。编译器会处理好调用、动态绑定等问题。
>
> 从写 C 程序的角度 (操作系统也就是个运行在计算机硬件上的 C 程序)，所谓 “编程” 不过是用那些编程语言提供的机制，把内存里的数据取出来，算一算，再放回去。There is *no* magic in computer systems.

只有在泥潭里摸爬滚打很多年，死了一次又一次，才能体会 C++11/14/17/20+, Rust, Go 等现代程序设计语言的良苦用心。

#### 3.3 自测：编程技巧

选修过《计算机系统基础》的同学一定已经经历过调试 bug 的噩梦。无数次你打算放弃 (或者实际放弃)，或选择不要某个 labs/PA 的成绩，或选择抱大腿同学的实现……你们做出的妥协都可以理解，但在这个过程中忽略的调试经验，只会让你们在调试越来越大系统的时候越来越吃力。

我们的自测问题是：如果你一个很大的项目发现了 bug (假设你可以稳定地重现它)，你应该如何找到出问题的地方所在？

- `printf` 是个很不错的方法；但你遇到过花费很长时间也没有找到 bug 的情况么？
- 如果 `printf` 帮助你找到了一些线索，如何进一步快速确定问题的 root cause？
- 如果项目很大，使用调试器单步就有些太繁琐了。你有什么技巧？(例如 watch point)

如果你对这些问题心里都有一些答案，那祝贺你！如果你一直在使用 “蛮力” 调试，的确有可能过去的代码你还能处理，但对于规模不断增长的代码，这就有些行不通了。

> #### 思考题：怎样尽可能编出**正确**的代码？
>
> 在 “面向 OJ 编程” 成为习惯以后，编程不过 “是测试 →不通过 → 修改” 的循环。但如果你希望**说服别人你的代码真的是对的**，你有什么办法吗？
>
> 试着提前想一想这个问题。这个学期里，大家会面对多线程并发的编程，这时候程序的正确性就尤为重要，只靠 “盲试” 就有些不够了。

### 4. 其他常见问题

- Q: **说好的操作系统呢？为什么没有图形界面？？？我是不是学了假的操作系统？？？？**

- A: 你如果把终端的每一个字符看成是像素点，那终端也勉强算是个 “图形” 界面了。

    实际上，操作系统也是这么管理图形界面的——由一个程序 (可能运行在 GPU 上) 算出每个像素点该显示什么颜色，就像 vi 在终端上显示字符、导航栏一样。当像素点足够小的时候，你就有图形的感觉了：

    ![img](http://jyywiki.cn/pages/OS/img/ascii-patrol.gif)

    ([ASCII Patrol](http://ascii-patrol.com/)：上面的 “图形” 真的都是 ASCII 字符组成的！)

    当然，图形绘制涉及到的知识太多，课程上就不多啰嗦了，假装能完成这个类比，无法假装的同学可以选修著名的 [Games 101](https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html)。

---

- Q: **为什么不是C++/Go/Rust/...?**

- A: **我们并不需要 “更高级” 的语言，依然可以编写优雅、深刻的代码，这对初学者来说尤为重要，不会 “顾此失彼”**。

    好的语言特性使程序变得优雅——但对于初学者，这些特性背后的东西 (例如 C++ RTTI) 可能给你带来未知的麻烦。而在这门课上，退一步并没有什么损失：我们不需要实现什么高级数据结构；用 C 语言也能写出优雅的代码，就像 xv6 那样。还有两点额外好处：

    - C 语言代码始终有非常直白的汇编语言一致性。
    - 通过在 C 语言编程时体会缺失的部分，能更好地理解现代编程语言中的机制。如果你熟悉现代 C++/Rust，你就会对对象的 ownership 非常敏感。即便你在写 C，这种好的思维习惯依然会时刻保护你。如果你想得更远一些，你依然可以在 C 中通过 assertions 近似地表达出 [Refinement Types](https://prl.ccs.neu.edu/blog/static/refinement_types_lecture.pdf)。

    Golang/Rust/C++ 都可以用来实现操作系统，不过似乎现在对大家来说负担稍稍有些重。

---

- Q: **我想退课/蹭课？**
- A: 上课可以督促你写好代码。而**不写代码这门课就白上了**；理解这一点，欢迎蹭课。如果觉得基础没有打好，就先努力学好 C 语言。这门课的唯一要求就是**会使用 C 语言编程**，还有**能读懂手册**。

------

- Q: **我想做纯理论。代码什么的关我️✖️事？**
- A: 有那个智力和坚持，写点 C 代码真是太简单了。万一有一天纯理论做不下去要去当码农了呢？遇到这麻烦的人我没少见过。

------

- Q: **我还是好怕。**
- A: Don't Panic。不要慌。也许我们可以来办公室聊一聊。
