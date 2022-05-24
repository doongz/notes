# [OS organization and system calls](https://pdos.csail.mit.edu/6.828/2020/lec/l-os.txt)

## 3.1 讨论话题

今天我们主要讨论4个话题：

- Isolation。隔离性是设计操作系统组织结构的驱动力。

- Kernel和User mode。这两种模式用来隔离操作系统内核和用户应用程序。

- System calls。系统调用是你的应用程序能够转换到内核执行的基本方法，这样你的用户态应用程序才能使用内核服务。

- 最后我们会看到所有的这些是如何以一种简单的方式在XV6中实现

对操作系统的结构有个大致的认知:

- 首先，会有类似于Shell，echo，find或者任何你实现的工具程序，这些程序运行在操作系统之上。
- 而操作系统又抽象了一些硬件资源，例如磁盘，CPU。
- 通常来说操作系统和应用程序之前的接口被称为系统调用接口（System call interface），我们这门课程看到的接口都是Unix风格的接口。基于这些Unix接口，你们在lab1中，完成了不同的应用程序。

## 3.2 操作系统隔离性 Isolation

隔离性（isolation），以及介绍为什么它很重要，为什么我们需要关心它？

- 需要在不同的应用程序之间有强隔离性。
- 需要在应用程序和操作系统之间有强隔离性

如果没有操作系统会怎样？

**应用程序会直接与硬件交互**

### CPU角度

使用操作系统的一个目的是**为了同时运行多个应用程序**，所以时不时的，CPU会从一个应用程序切换到另一个应用程序。我们假设硬件资源里只有一个CPU核，并且我们现在在这个CPU核上运行Shell。但是时不时的，也需要让其他的应用程序也可以运行。现在我们没有操作系统来帮我们完成切换，所以Shell就需要时不时的释放CPU资源。

为了不变成一个恶意程序，Shell在发现自己运行了一段时间之后，需要让别的程序也有机会能运行。这种机制有时候称为协同调度（Cooperative Scheduling）。但是这里的场景并没有很好的隔离性，比如说Shell中的某个函数有一个死循环，那么Shell永远也不会释放CPU，进而其他的应用程序也不能够运行，甚至都不能运行一个第三方的程序来停止或者杀死Shell程序。所以这种场景下，我们基本上得不到真正的multiplexing（CPU在多进程同分时复用）。而这个特性是非常有用的，**不论应用程序在执行什么操作，multiplexing都会迫使应用程序时不时的释放CPU，这样其他的应用程序才能运行**。

### 物理内存角度

从内存的角度来说，如果应用程序直接运行在硬件资源之上，那么每个应用程序的文本，代码和数据都直接保存在物理内存中。物理内存中的一部分被Shell使用，另一部分被echo使用。因为两个应用程序的内存之间没有边界，如果echo程序将数据存储在属于Shell的一个内存地址中（下图中的1000），那么就echo就会覆盖Shell程序内存中的内容。

这类的问题是非常难定位的。所以这里也没有为我们提供好的隔离性。我们希望不同应用程序之间的内存是隔离的，这样一个应用程序就不会覆盖另一个应用程序的内存

### 使用操作系统的主要原因

使用操作系统的一个原因，甚至可以说是**主要原因就是为了实现multiplexing和内存隔离**。如果你不使用操作系统，并且应用程序直接与硬件交互，就很难实现这两点。所以，将操作系统设计成一个库，并不是一种常见的设计。你或许可以在一些实时操作系统中看到这样的设计，因为在这些实时操作系统中，应用程序之间彼此相互信任。但是在大部分的其他操作系统中，都会强制实现硬件资源的隔离。

如果我们从隔离的角度来稍微看看Unix接口，那么我们可以发现，接口被精心设计以实现资源的强隔离，也就是multiplexing和物理内存的隔离。接口通过抽象硬件资源，从而使得提供强隔离性成为可能。

### 举几个例子

例子一

之前通过**fork创建了进程。进程本身不是CPU，但是它们对应了CPU**，它们使得你可以在CPU上运行计算任务。所以你懂的，应用程序不能直接与CPU交互，只能与进程交互。操作系统内核会完成不同进程在CPU上的切换。所以，操作系统不是直接将CPU提供给应用程序，而是向应用程序提供“进程”，进程抽象了CPU，这样操作系统才能在多个应用程序之间复用一个或者多个CPU。

> 学生提问：这里说进程抽象了CPU，是不是说一个进程使用了部分的CPU，另一个进程使用了CPU的另一部分？这里CPU和进程的关系是什么？
>
> Frans教授：我这里真实的意思是，我们在实验中使用的RISC-V处理器实际上是有4个核。所以你可以同时运行4个进程，一个进程占用一个核。但是假设你有8个应用程序，操作系统会分时复用这些CPU核，比如说对于一个进程运行100毫秒，之后内核会停止运行并将那个进程从CPU中卸载，再加载另一个应用程序并再运行100毫秒。通过这种方式使得每一个应用程序都不会连续运行超过100毫秒。这里只是一些基本概念，我们在接下来的几节课中会具体的看这里是如何实现的。
>
> 学生提问：好的，但是多个进程不能在同一时间使用同一个CPU核，对吧？
>
> Frans教授：是的，这里是分时复用。CPU运行一个进程一段时间，再运行另一个进程。

例子二

我们可以认为**exec抽象了内存**。当我们在执行exec系统调用的时候，我们会传入一个文件名，而这个文件名对应了一个应用程序的内存镜像。内存镜像里面包括了程序对应的指令，全局的数据。应用程序可以逐渐扩展自己的内存，但是应用程序并没有直接访问物理内存的权限，例如应用程序不能直接访问物理内存的1000-2000这段地址。不能直接访问的原因是，操作系统会提供内存隔离并控制内存，操作系统会在应用程序和硬件资源之间提供一个中间层。exec是这样一种系统调用，它表明了应用程序不能直接访问物理内存。

例子三

另一个例子是files，**files基本上来说抽象了磁盘**。应用程序不会直接读写挂在计算机上的磁盘本身，并且在Unix中这也是不被允许的。在Unix中，与存储系统交互的唯一方式就是通过files。Files提供了非常方便的磁盘抽象，你可以对文件命名，读写文件等等。之后，操作系统会决定如何将文件与磁盘中的块对应，确保一个磁盘块只出现在一个文件中，并且确保用户A不能操作用户B的文件。通过files的抽象，可以实现不同用户之间和同一个用户的不同进程之间的文件强隔离。

这些接口看起来像是经过精心的设计以抽象计算机资源，这样这些接口的实现，或者说**操作系统本身可以在多个应用程序之间复用计算机硬件资源，同时还提供了强隔离性。缺陷就是效率比实时操作系统慢**

> 学生提问：更复杂的内核会不会尝试将进程调度到同一个CPU核上来减少Cache Miss？
>
> Frans教授：是的。有一种东西叫做Cache affinity。现在的操作系统的确非常复杂，并且会尽量避免Cache miss和类似的事情来提升性能。我们在这门课程后面介绍高性能网络的时候会介绍更多相关的内容。
>
> 学生提问：XV6的代码中，哪一部分可以看到操作系统为多个进程复用了CPU？
>
> Frans教授：有挺多文件与这个相关，但是proc.c应该是最相关的一个。两三周之后的课程中会有一个话题介绍这个内容。我们会看大量的细节，并展示操作系统的multiplexing是如何发生的。所以可以这么看待这节课，这节课的内容是对许多不同内容的初始介绍，因为我们总得从某个地方开始吧。

## 3.3 操作系统防御性 Defensive

操作系统应该具有防御性（Defensive）

当你在做内核开发时，这是一种你需要熟悉的重要思想。操作系统需要确保所有的组件都能工作，所以它需要做好准备抵御来自应用程序的攻击。如果说应用程序无意或者恶意的向系统调用传入一些错误的参数就会导致操作系统崩溃，那就太糟糕了。在这种场景下，操作系统因为崩溃了会拒绝为其他所有的应用程序提供服务。所以操作系统需要以这样一种方式来完成：**操作系统需要能够应对恶意的应用程序**。

另一个需要考虑的是，**应用程序不能够打破对它的隔离**。应用程序非常有可能是恶意的，它或许是由攻击者写出来的，攻击者或许想要打破对应用程序的隔离，进而控制内核。一旦有了对于内核的控制能力，你可以做任何事情，因为内核控制了所有的硬件资源。

通常来说，**需要通过硬件来实现这的强隔离性**。我们这节课会简单介绍一些硬件隔离的内容，但是在后续的课程我们会介绍的更加详细。这里的硬件支持包括了两部分，

- 第一部分是user/kernel mode，kernel mode在RISC-V中被称为Supervisor mode但是其实是同一个东西；
- 第二部分是page table或者虚拟内存（Virtual Memory）。

所以，**所有的处理器，如果需要运行能够支持多个应用程序的操作系统，需要同时支持user/kernle mode和虚拟内存**。具体的实现或许会有细微的差别，但是基本上来说所有的处理器需要能支持这些。我们在这门课中使用的RISC-V处理器就支持了这些功能。

## 3.4 硬件对于强隔离的支持

硬件对于强隔离的支持包括了：user/kernle mode和虚拟内存。

### user/kernel mode

首先，我们来看一下user/kernel mode，这里会以尽可能全局的视角来介绍，有很多重要的细节在这节课中都不会涉及。为了支持user/kernel mode，处理器会有两种操作模式，第一种是user mode，第二种是kernel mode。当运行在kernel mode时，CPU可以运行特定权限的指令（privileged instructions）；当运行在user mode时，CPU只能运行普通权限的指令（unprivileged instructions）。

- 普通权限的指令都是一些你们熟悉的指令，例如将两个寄存器相加的指令ADD、将两个寄存器相减的指令SUB、跳转指令JRC、BRANCH指令等等。这些都是普通权限指令，所有的应用程序都允许执行这些指令。

- 特殊权限指令主要是一些直接操纵硬件的指令和设置保护的指令，例如设置page table寄存器、关闭时钟中断。在处理器上有各种各样的状态，操作系统会使用这些状态，但是只能通过特殊权限指令来变更这些状态。

举个例子，当一个应用程序尝试执行一条特殊权限指令，因为不允许在user mode执行特殊权限指令，处理器会拒绝执行这条指令。通常来说，这时会将控制权限从user mode切换到kernel mode，当操作系统拿到控制权之后，或许会杀掉进程，因为应用程序执行了不该执行的指令。

下图是RISC-V privilege架构的文档，这个文档包括了所有的特殊权限指令。在接下来的一个月，你们都会与这些特殊权限指令打交道。我们下节课就会详细介绍其中一些指令。这里我们先对这些指令有一些初步的认识：应用程序不应该执行这些指令，**这些指令只能被内核执行**。

> 学生提问：如果kernel mode允许一些指令的执行，user mode不允许一些指令的执行，那么是谁在检查当前的mode并实际运行这些指令，并且怎么知道当前是不是kernel mode？是有什么标志位吗？
>
> Frans教授：是的，在处理器里面有一个flag。在处理器的一个bit，当它为1的时候是user mode，当它为0时是kernel mode。当处理器在解析指令时，如果指令是特殊权限指令，并且该bit被设置为1，处理器会拒绝执行这条指令，就像在运算时不能除以0一样。
>
> 同一个学生继续问：所以，唯一的控制方式就是通过某种方式更新了那个bit？
>
> Frans教授：你认为是什么指令更新了那个bit位？是特殊权限指令还是普通权限指令？（等了一会，那个学生没有回答）。很明显，设置那个bit位的指令必须是特殊权限指令，因为应用程序不应该能够设置那个bit到kernel mode，否则的话应用程序就可以运行各种特殊权限指令了。所以那个bit是被保护的，这样回答了你的问题吗？

许多同学都已经知道了，实际上RISC-V还有第三种模式称为machine mode。在大多数场景下，我们会忽略这种模式，所以我也不太会介绍这种模式。 所以实际上我们有三级权限（user/kernel/machine），而不是两级(user/kernel)。

> 学生提问：考虑到安全性，所有的用户代码都会通过内核访问硬件，但是有没有可能一个计算机的用户可以随意的操纵内核？
>
> Frans教授：并不会，至少小心的设计就不会发生这种事。或许一些程序会有额外的权限，操作系统也会认可这一点。但是这些额外的权限并不会给每一个用户，比如只有root用户有特定的权限来完成安全相关的操作。
>
> 同一个学生提问：那BIOS呢？BIOS会在操作系统之前运行还是之后？
>
> Frans教授：BIOS是一段计算机自带的代码，它会先启动，之后它会启动操作系统，所以BIOS需要是一段可被信任的代码，它最好是正确的，且不是恶意的。
>
> 学生提问：之前提到，设置处理器中kernel mode的bit位的指令是一条特殊权限指令，那么一个用户程序怎么才能让内核执行任何内核指令？因为现在切换到kernel mode的指令都是一条特殊权限指令了，对于用户程序来说也没法修改那个bit位。
>
> Frans教授：你说的对，这也是我们想要看到的结果。可以这么来看这个问题，首先这里不是完全按照你说的方式工作，在RISC-V中，如果你在用户空间（user space）尝试执行一条特殊权限指令，用户程序会通过系统调用来切换到kernel mode。当用户程序执行系统调用，会通过ECALL触发一个软中断（software interrupt），软中断会查询操作系统预先设定的中断向量表，并执行中断向量表中包含的中断处理程序。中断处理程序在内核中，这样就完成了user mode到kernel mode的切换，并执行用户程序想要执行的特殊权限指令。

### 虚拟内存

我们接下来看看硬件对于支持强隔离性的第二个特性，基本上所有的CPU都支持虚拟内存。我下节课会更加深入的讨论虚拟内存，这里先简单看一下。基本上来说，处理器包含了page table，而page table将虚拟内存地址与物理内存地址做了对应。

**每一个进程都会有自己独立的page table，这样的话，每一个进程只能访问出现在自己page table中的物理内存**。操作系统会设置page table，使得每一个进程都有不重合的物理内存，这样一个进程就不能访问其他进程的物理内存，因为其他进程的物理内存都不在它的page table中。一个进程甚至都不能随意编造一个内存地址，然后通过这个内存地址来访问其他进程的物理内存。这样就给了我们内存的强隔离性。

基于硬件的支持，我们可以重新画一下之前的一张图，我们先画一个矩形，ls程序位于这个矩形中；再画一个矩形，echo程序位于这个矩形中。每个矩形都有一个虚拟内存地址，从0开始到2的n次方。

这样，ls程序有了一个内存地址0，echo程序也有了一个内存地址0。但是操作系统会将两个程序的内存地址0映射到不同的物理内存地址，所以ls程序不能访问echo程序的内存，同样echo程序也不能访问ls程序的内存。

类似的，内核位于应用程序下方，假设是XV6，那么它也有自己的内存地址空间，并且与应用程序完全独立。

## 3.5 **User/Kernel mode切换**

我们可以认为user/kernel mode是分隔用户空间和内核空间的边界，用户空间运行的程序运行在user mode，内核空间的程序运行在kernel mode。操作系统位于内核空间。

![6s081-2](./doc/6s081-2.png)

例如当ls程序运行的时候，会调用read/write系统调用；Shell程序会调用fork或者exec系统调用，所以必须要有一种方式可以使得用户的应用程序能够将控制权以一种协同工作的方式转移到内核，这样内核才能提供相应的服务。

所以，需要有一种方式能够让应用程序可以将控制权转移给内核（Entering Kernel）

在RISC-V中，有一个专门的指令用来实现这个功能，叫做ECALL。ECALL接收一个数字参数，当一个用户程序想要将程序执行的控制权转移到内核，它只需要执行ECALL指令，并传入一个数字。这里的数字参数代表了应用程序想要调用的System Call。

ECALL会跳转到内核中一个特定，由内核控制的位置。我们在这节课的最后可以看到**在XV6中存在一个唯一的系统调用接入点，每一次应用程序执行ECALL指令，应用程序都会通过这个接入点进入到内核中**。举个例子，不论是Shell还是其他的应用程序，当它在用户空间执行fork时，它并不是直接调用操作系统中对应的函数，而是调用ECALL指令，并将fork对应的数字作为参数传给ECALL。之后再通过ECALL跳转到内核。

下图中通过一根竖线来区分用户空间和内核空间，左边是用户空间，右边是内核空间。在内核侧，有一个位于syscall.c的函数syscall，每一个从应用程序发起的系统调用都会调用到这个syscall函数，syscall函数会检查ECALL的参数，通过这个参数内核可以知道需要调用的是fork（3.9会有相应的代码跟踪介绍）。

![6s081-3](./doc/6s081-3.png)

这里需要澄清的是，**用户空间和内核空间的界限是一个硬性的界限**，用户不能直接调用fork，用户的应用程序执行系统调用的唯一方法就是通过这里的ECALL指令。

假设我现在要执行另一个系统调用write，相应的流程是类似的，write系统调用不能直接调用内核中的write代码，而是由封装好的系统调用函数执行ECALL指令。所以write函数实际上调用的是ECALL指令，指令的参数是代表了write系统调用的数字。之后控制权到了syscall函数，syscall会实际调用write系统调用。

> 学生提问：操作系统在什么时候检查是否允许执行fork或者write？现在看起来应用程序只需要执行ECALL再加上系统调用对应的数字就能完成调用，但是内核在什么时候决定这个应用程序是否有权限执行特定的系统调用？
>
> Frans教授：是个好问题。原则上来说，在内核侧实现fork的位置可以实现任何的检查，例如检查系统调用的参数，并决定应用程序是否被允许执行fork系统调用。在Unix中，任何应用程序都能调用fork，我们以write为例吧，write的实现需要检查传递给write的地址（需要写入数据的指针）属于用户应用程序，这样内核才不会被欺骗从别的不属于应用程序的位置写入数据。
>
> 学生提问：当应用程序表现的恶意或者就是在一个死循环中，内核是如何夺回控制权限的？
>
> Frans教授：内核会通过硬件设置一个定时器，定时器到期之后会将控制权限从用户空间转移到内核空间，之后内核就有了控制能力并可以重新调度CPU到另一个进程中。我们接下来会看一些更加详细的细节。
>
> 学生提问：这其实是一个顶层设计的问题，是什么驱动了操作系统的设计人员使用编程语言C？
>
> Frans教授：啊，这是个好问题。C提供了很多对于硬件的控制能力，比如说当你需要去编程一个定时器芯片时，这更容易通过C来完成，因为你可以得到更多对于硬件资源的底层控制能力。所以，如果你要做大量的底层开发，C会是一个非常方便的编程语言，尤其是需要与硬件交互的时候。当然，不是说你不能用其他的编程语言，但是这是C成功的一个历史原因。
>
> 学生提问：为什么C比C++流行的多？仅仅是因为历史原因吗？有没有其他的原因导致大部分的操作系统并没有采用C++？
>
> Frans教授：我认为有一些操作系统是用C++写的，这完全是可能的。但是大部分你知道的操作系统并不是用C++写的，这里的主要原因是Linus不喜欢C++，所以Linux主要是C语言实现。

## 3.6 **宏内核 vs 微内核 （Monolithic Kernel vs Micro Kernel）**

现在，我们有了一种方法，可以通过系统调用或者说ECALL指令，将控制权从应用程序转到操作系统中。之后内核负责实现具体的功能并检查参数以确保不会被一些坏的参数所欺骗。所以内核有时候也被称为可被信任的计算空间（Trusted Computing Base），在一些安全的术语中也被称为TCB。

基本上来说，要被称为TCB，内核首先要是正确且没有Bug的。假设内核中有Bug，攻击者可能会利用那个Bug，并将这个Bug转变成漏洞，这个漏洞使得攻击者可以打破操作系统的隔离性并接管内核。所以内核真的是需要越少的Bug越好（但是谁不是呢）。

另一方面，内核必须要将用户应用程序或者进程当做是恶意的。

一个有趣的问题是，什么程序应该运行在kernel mode？敏感的代码肯定是运行在kernel mode，因为这是Trusted Computing Base。

### 宏内核

其中一个选项是让整个操作系统代码都运行在kernel mode。大多数的Unix操作系统实现都运行在kernel mode。比如，XV6中，**所有的操作系统服务都在kernel mode中，这种形式被称为Monolithic Kernel Design**（[宏内核](https://en.wikipedia.org/wiki/Monolithic_kernel)）。

这里有几件事情需要注意：

- 首先，如果考虑Bug的话，这种方式不太好。**在一个宏内核中，任何一个操作系统的Bug都有可能成为漏洞**。因为我们现在在内核中运行了一个巨大的操作系统，出现Bug的可能性更大了。你们可以去查一些统计信息，平均每3000行代码都会有几个Bug，所以如果有许多行代码运行在内核中，那么出现严重Bug的可能性也变得更大。**所以从安全的角度来说，在内核中有大量的代码是宏内核的缺点**。
- 另一方面，如果你去看一个操作系统，它包含了各种各样的组成部分，比如说文件系统，虚拟内存，进程管理，这些都是操作系统内实现了特定功能的子模块。宏内核的优势在于，因为这些**子模块现在都位于同一个程序中，它们可以紧密的集成在一起，这样的集成提供很好的性能**。例如Linux，它就有很不错的性能。

### 微内核

另一种设计主要关注点是**减少内核中的代码，它被称为Micro Kernel Design**（[微内核](https://en.wikipedia.org/wiki/Microkernel)）。在这种模式下，希望在kernel mode中运行尽可能少的代码。所以这种设计下还是有内核，但是内核只有非常少的几个模块，例如，内核通常会有一些IPC的实现或者是Message passing；非常少的虚拟内存的支持，可能只支持了page table；以及分时复用CPU的一些支持。

微内核的目的在于将大部分的操作系统运行在内核之外。所以，我们还是会有user mode以及user/kernel mode的边界。但是我们现在会将原来在内核中的其他部分，作为普通的用户程序来运行。比如文件系统可能就是个常规的用户空间程序。这个文件系统我不小心画成了红色，其实我想画成黑色的。

现在，文件系统运行的就像一个普通的用户程序，就像echo，Shell一样，这些程序都运行在用户空间。可能还会有一些其他的用户应用程序，例如虚拟内存系统的一部分也会以一个普通的应用程序的形式运行在user mode。

某种程度上来说，这是一种好的设计。因为在内核中的代码的数量较小，更少的代码意味着更少的Bug。

但是这种设计也有相应的问题。假设我们需要让Shell能与文件系统交互，比如Shell调用了exec，必须有种方式可以接入到文件系统中。通常来说，这里工作的方式是，Shell会通过内核中的IPC系统发送一条消息，内核会查看这条消息并发现这是给文件系统的消息，之后内核会把消息发送给文件系统。

文件系统会完成它的工作之后会向IPC系统发送回一条消息说，这是你的exec系统调用的结果，之后IPC系统再将这条消息发送给Shell。

![6s081-4](./doc/6s081-4.png)

所以，这里是典型的通过消息来实现传统的系统调用。现在，对于任何文件系统的交互，都需要分别完成2次用户空间<->内核空间的跳转。与宏内核对比，在宏内核中如果一个应用程序需要与文件系统交互，只需要完成1次用户空间<->内核空间的跳转，所以微内核的的跳转是宏内核的两倍。**通常微内核的挑战在于性能更差**，这里有两个方面需要考虑：

1. 在user/kernel mode反复跳转带来的性能损耗。
2. 在一个类似宏内核的紧耦合系统，各个组成部分，例如文件系统和虚拟内存系统，可以很容易的共享page cache。而在微内核中，每个部分之间都很好的隔离开了，这种共享更难实现。进而导致更难在微内核中得到更高的性能。

我们这里介绍的有关宏内核和微内核的区别都特别的笼统。在实际中，两种内核设计都会出现，出于历史原因大部分的桌面操作系统是宏内核，如果你运行需要大量内核计算的应用程序，**例如在数据中心服务器上的操作系统，通常也是使用的宏内核，主要的原因是Linux提供了很好的性能。但是很多嵌入式系统，例如Minix，Cell，这些都是微内核设计**。这两种设计都很流行，如果你从头开始写一个操作系统，你可能会从一个微内核设计开始。但是一旦你有了类似于Linux这样的宏内核设计，将它重写到一个微内核设计将会是巨大的工作。并且这样重构的动机也不足，因为人们总是想把时间花在实现新功能上，而不是重构他们的内核。

所以这里是操作系统的两种主要设计。如你们所知的，XV6是一种宏内核设计，如大多数经典的Unix系统一样。但是在这个学期的后半部分，我们会讨论更多有关微内核设计的内容。

## **3.7 编译运行kernel**

来看一下XV6是如何工作的。代码主要有三个部分组成：

- 第一个是kernel。我们可以ls kernel的内容，里面包含了基本上所有的内核文件。因为XV6是一个宏内核结构，这里所有的文件会被编译成一个叫做kernel的二进制文件，然后这个二进制文件会被运行在kernle mode中。
- 第二个部分是user。这基本上是运行在user mode的程序。这也是为什么一个目录称为kernel，另一个目录称为user的原因。
- 第三部分叫做mkfs。它会创建一个空的文件镜像，我们会将这个镜像存在磁盘上，这样我们就可以直接使用一个空的文件系统。

接下来，我想简单的介绍一下内核是如何编译的。你们可能已经编译过内核，但是还没有真正的理解编译过程，这个过程还是比较重要的。

首先，Makefile（XV6目录下的文件）会读取一个C文件，例如proc.c；之后调用gcc编译器，生成一个文件叫做proc.s，这是RISC-V 汇编语言文件；之后再走到汇编解释器，生成proc.o，这是汇编语言的二进制格式。

Makefile会为所有内核文件做相同的操作，比如说pipe.c，会按照同样的套路，先经过gcc编译成pipe.s，再通过汇编解释器生成pipe.o。

之后，系统加载器（Loader）会收集所有的.o文件，将它们链接在一起，并生成内核文件。

这里生成的内核文件就是我们将会在QEMU中运行的文件。同时，为了你们的方便，Makefile还会创建kernel.asm，这里包含了内核的完整汇编语言，你们可以通过查看它来定位究竟是哪个指令导致了Bug。比如，我接下来查看kernel.asm文件，我们可以看到用汇编指令描述的内核：

![6s081-5](./doc/6s081-5.png)

这里你们可能已经注意到了，第一个指令位于地址0x80000000，对应的是一个RISC-V指令：auipc指令。有人知道第二列，例如0x0000a117、0x83010113、0x6505，是什么意思吗？有人想来回答这个问题吗？

> 学生回答：这是汇编指令的16进制表现形式对吗？
>
> 是的，完全正确。所以这里0x0000a117就是auipc，这里是二进制编码后的指令。因为每个指令都有一个二进制编码，kernel的asm文件会显示这些二进制编码。当你在运行gdb时，如果你想知道具体在运行什么，你可以看具体的二进制编码是什么，有的时候这还挺方便的。

接下来，让我们不带gdb运行XV6（make会读取Makefile文件中的指令）。这里会编译文件，然后调用QEMU（qemu-system-riscv64指令）。这里本质上是通过C语言来模拟仿真RISC-V处理器。

我们来看传给QEMU的几个参数：

- kernel：这里传递的是内核文件（kernel目录下的kernel文件），这是将在QEMU中运行的程序文件。
- m：这里传递的是RISC-V虚拟机将会使用的内存数量
- smp：这里传递的是虚拟机可以使用的CPU核数
- drive：传递的是虚拟机使用的磁盘驱动，这里传入的是fs.img文件

这样，XV6系统就在QEMU中启动了。

## **3.8 QEMU**

QEMU表现的就像一个真正的计算机一样。当你想到QEMU时，你不应该认为它是一个C程序，你应该把它想成是下图，一个真正的主板。

![6s081-6](./doc/6s081-6.png)

图中是一个我办公室中的RISC-V主板，它可以启动一个XV6。当你通过QEMU来运行你的内核时，你应该认为你的内核是运行在这样一个主板之上。主板有一个开关，一个RISC-V处理器，有支持外设的空间，比如说一个接口是连接网线的，一个是PCI-E插槽，主板上还有一些内存芯片，这是一个你可以在上面编程的物理硬件，而XV6操作系统管理这样一块主板，你在你的脑海中应该有这么一张图。

对于RISC-V，有完整的文档介绍，比如说下图是一个RISC-V的结构图：

![6s081-7](./doc/6s081-7.png)

这个图里面有：

- 4个核：U54 Core 1-4
- L2 cache：Banked L2
- 连接DRAM的连接器：DDR Controller
- 各种连接外部设备的方式，比如说UART0，一端连接了键盘，另一端连接了terminal。
- 以及连接了时钟的接口：Clock Generation

我们后面会讨论更多的细节，但是这里基本上就是RISC-V处理器的所有组件，你通过它与实际的硬件交互。

当我们说QEMU仿真了RISC-V处理器时，背后的含义是什么？

直观来看，QEMU是一个大型的开源C程序，你可以下载或者git clone它。但是在内部，在QEMU的主循环中，只在做一件事情：

- 读取4字节或者8字节的RISC-V指令。
- 解析RISC-V指令，并找出对应的操作码（op code）。我们之前在看kernel.asm的时候，看过一些操作码的二进制版本。通过解析，或许可以知道这是一个ADD指令，或者是一个SUB指令
- 之后，在软件中执行相应的指令。

这基本上就是QEMU的全部工作了，对于每个CPU核，QEMU都会运行这么一个循环。

为了完成这里的工作，QEMU的主循环需要维护寄存器的状态。所以QEMU会有以C语言声明的类似于X0，X1寄存器等等。

当QEMU在执行一条指令，比如(ADD a0, 7, 1)，这里会将常量7和1相加，并将结果存储在a0寄存器中，所以在这个例子中，寄存器X0会是7。

![6s081-8](./doc/6s081-8.png)

之后QEMU会执行下一条指令，并持续不断的执行指令。除了仿真所有的普通权限指令之外，QEMU还会仿真所有的特殊权限指令，这就是QEMU的工作原理。对于你们来说，你们只需要认为你们跑在QEMU上的代码跟跑在一个真正的RISC-V处理器上是一样的，就像你们在6.004这门课程中使用过的RISC-V处理器一样。

> 学生提问：我想知道，QEMU有没有什么欺骗硬件的实现，比如说overlapping instruction？
>
> Frans教授：并没有，真正的CPU运行在QEMU的下层。当你运行QEMU时，很有可能你是运行在一个x86处理器上，这个x86处理器本身会做各种处理，比如顺序解析指令。所以QEMU对你来说就是个C语言程序。
>
> 学生提问：那多线程呢？程序能真正跑在4个核上吗？还是只能跑在一个核上？如果能跑在多个核上，那么QEMU是不是有多线程？
>
> Frans教授：我们在Athena上使用的QEMU还有你们下载的QEMU，它们会使用多线程。QEMU在内部通过多线程实现并行处理。所以，当QEMU在仿真4个CPU核的时候，它是并行的模拟这4个核。我们在后面有个实验会演示这里是如何工作的。所以，（当QEMU仿真多个CPU核时）这里真的是在不同的CPU核上并行运算。

## **3.9 XV6 启动过程**

[操作过程](https://mit-public-courses-cn-translatio.gitbook.io/mit6-s081/lec03-os-organization-and-system-calls/3.9-xv6-qi-dong-guo-cheng)

首先，我会启动QEMU，并打开gdb。本质上来说QEMU内部有一个gdb server，当我们启动之后，QEMU会等待gdb客户端连接。

```shell
$ make CPUS=1 qemu-gdb
sed "s/:1234/:25501/" < .gdbinit.tmpl-riscv > .gdbinit
*** Now run 'gdb' in another window.
qemu-system-riscv64 -machine virt -bios none -kernel kernel/kernel -m 128M -smp 1 -nographic -drive file=fs.img,if=none,format=raw,id=x0 -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 -S -gdb tcp::25501
```

我会在我的计算机上再启动一个gdb客户端，这里是一个RISC-V 64位Linux的gdb，有些同学的电脑可能是multi-arch或者其他版本的的gdb，但是基本上来说，这里的gdb是为RISC-V 64位处理器编译的。

```shell
$ riscv64-unknown-elf-gdb
Copyright (C) 2019 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "--host=x86_64-apple-darwin21.4.0 --target=riscv64-unknown-elf".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word".
(gdb) 
```

注意：有时候会出现个提示，按照要求把内容添加进去

```shell
For help, type "help".
Type "apropos word" to search for commands related to "word"...
"/Users/xxx/pj/xv6-labs-2020/xv6.out": not in executable format: file format not recognized
warning: File "/Users/xxx/pj/xv6-labs-2020/.gdbinit" auto-loading has been declined by your `auto-load safe-path' set to "$debugdir:$datadir/auto-load".
To enable execution of this file add
	add-auto-load-safe-path /Users/xxx/pj/xv6-labs-2020/.gdbinit
line to your configuration file "/Users/xxx/.gdbinit".
```

正确的样子应该是这样，会有 `0x0000000000001000 in ?? ()`

```shell
$ riscv64-unknown-elf-gdb
GNU gdb (GDB) 8.3.0.20190516-git
Copyright (C) 2019 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "--host=x86_64-apple-darwin21.4.0 --target=riscv64-unknown-elf".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word".
The target architecture is assumed to be riscv:rv64
warning: No executable has been specified and target does not support
determining executable automatically.  Try using the "file" command.
0x0000000000001000 in ?? ()
```

在连接上之后，我会在程序的入口处设置一个端点，因为我们知道这是QEMU会跳转到的第一个指令。

```shell
(gdb) b _entry
Breakpoint 1 at 0x8000000a
```

设置完断点之后，我运行程序，可以发现代码并没有停在0x8000000（见3.7 kernel.asm中，0x80000000是程序的起始位置），而是停在了0x8000000a。

```shell
(gdb) c
Continuing.

Breakpoint 1, 0x000000008000000a in _entry ()
=> 0x000000008000000a <_entry+10>:	f3 25 40 f1	csrr	a1,mhartid
```

如果我们查看kernel的汇编文件，

```shell
$ cat kernel/kernel.asm
kernel/kernel：     文件格式 elf64-littleriscv


Disassembly of section .text:

0000000080000000 <_entry>:
    80000000:	0000a117          	auipc	sp,0xa
    80000004:	83010113          	addi	sp,sp,-2000 # 80009830 <stack0>
    80000008:	6505                lui	a0,0x1
    8000000a:	f14025f3          	csrr	a1,mhartid
    8000000e:	0585                addi	a1,a1,1
    80000010:	02b50533          	mul	a0,a0,a1
    80000014:	912a                add	sp,sp,a0
    80000016:	070000ef          	jal	ra,80000086 <start>

000000008000001a <spin>:
    8000001a:	a001                	j	8000001a <spin>

```

我们可以看到，在地址0x8000000a读取了控制系统寄存器（Control System Register）mhartid，并将结果加载到了a1寄存器。所以QEMU会模拟执行这条指令，之后执行下一条指令。

地址0x80000000是一个被QEMU认可的地址。也就是说如果你想使用QEMU，那么第一个指令地址必须是它。所以，我们会让内核加载器从那个位置开始加载内核。如果我们查看kernel.ld，

```shell
$ cat kernel/kernel.ld
OUTPUT_ARCH( "riscv" )
ENTRY( _entry )

SECTIONS
{
  /*
   * ensure that entry.S / _entry is at 0x80000000,
   * where qemu's -kernel jumps.
   */
  . = 0x80000000;

  .text : {
    *(.text .text.*)
    . = ALIGN(0x1000);
    _trampoline = .;
    *(trampsec)
    . = ALIGN(0x1000);
    ASSERT(. - _trampoline == 0x1000, "error: trampoline larger than one page");
    PROVIDE(etext = .);
  }

  .rodata : {
    . = ALIGN(16);
    *(.srodata .srodata.*) /* do not need to distinguish this from .rodata */
    . = ALIGN(16);
    *(.rodata .rodata.*)
  }

  .data : {
    . = ALIGN(16);
    *(.sdata .sdata.*) /* do not need to distinguish this from .data */
    . = ALIGN(16);
    *(.data .data.*)
  }

  .bss : {
    . = ALIGN(16);
    *(.sbss .sbss.*) /* do not need to distinguish this from .bss */
    . = ALIGN(16);
    *(.bss .bss.*)
  }

  PROVIDE(end = .);
}
```

我们可以看到，这个文件定义了内核是如何被加载的，从这里也可以看到，内核使用的起始地址就是QEMU指定的0x80000000这个地址。这就是我们操作系统最初运行的步骤。

回到gdb，我们可以看到gdb也显示了指令的二进制编码

```shell
Breakpoint 1, 0x000000008000000a in _entry ()
=> 0x000000008000000a <_entry+10>:	f3 25 40 f1	csrr	a1,mhartid
(gdb) si
0x000000008000000e in _entry ()
=> 0x000000008000000e <_entry+14>:	85 05	addi	a1,a1,1
```

可以看出，csrr是一个4字节的指令，而addi是一个2字节的指令。

我们这里可以看到，XV6从entry.s开始启动，这个时候没有内存分页，没有隔离性，并且运行在M-mode（machine mode）。XV6会尽可能快的跳转到kernel mode或者说是supervisor mode。我们在main函数设置一个断点，main函数已经运行在supervisor mode了。接下来我运行程序，代码会在断点，也就是main函数的第一条指令停住。

```shell
(gdb) b main
Breakpoint 2 at 0x80000f18: file kernel/main.c, line 13.
(gdb) c
Continuing.

Breakpoint 2, main () at kernel/main.c:13
13	  if(cpuid() == 0){
```

上面gdb的断点显示，下面main函数的源码。

```c
#include "types.h"
#include "param.h"
#include "memlayout.h"
#include "riscv.h"
#include "defs.h"

volatile static int started = 0;

// start() jumps here in supervisor mode on all CPUs.
void
main()
{
  if(cpuid() == 0){
    consoleinit();
    printfinit();
    printf("\n");
    printf("xv6 kernel is booting\n");
    printf("\n");
    kinit();         // physical page allocator
    kvminit();       // create kernel page table
    kvminithart();   // turn on paging
    procinit();      // process table
    trapinit();      // trap vectors
    trapinithart();  // install kernel trap vector
    plicinit();      // set up interrupt controller
    plicinithart();  // ask PLIC for device interrupts
    binit();         // buffer cache
    iinit();         // inode cache
    fileinit();      // file table
    virtio_disk_init(); // emulated hard disk
    userinit();      // first user process
    __sync_synchronize();
    started = 1;
  } else {
    while(started == 0)
      ;
    __sync_synchronize();
    printf("hart %d starting\n", cpuid());
    kvminithart();    // turn on paging
    trapinithart();   // install kernel trap vector
    plicinithart();   // ask PLIC for device interrupts
  }

  scheduler();        
}

```

接下来，我想运行在gdb的layout split模式：

```
(gdb) layout split
```

![Snipaste_2022-05-15_01-00-22](./doc/Snipaste_2022-05-15_01-00-22.png)

从这个视图可以看出gdb要执行的下一条指令是什么，断点具体在什么位置。

这里我只在一个CPU上运行QEMU（见最初的make参数），这样会使得gdb调试更加简单。因为现在只指定了一个CPU核，QEMU只会仿真一个核，我可以单步执行程序（因为在单核或者单线程场景下，单个断点就可以停止整个程序的运行）。

通过在gdb中输入n，可以挑到下一条指令。这里调用了一个名为consoleinit的函数，它的工作与你想象的完全一样，也就是设置好console。一旦console设置好了，接下来可以向console打印输出（代码16、17行）。执行完16、17行之后，我们可以在QEMU看到相应的输出。

![Snipaste_2022-05-15_01-06-55](./doc/Snipaste_2022-05-15_01-06-55.png)

除了console之外，还有许多代码来做初始化。

kinit：设置好页表分配器（page allocator）

kvminit：设置好虚拟内存，这是下节课的内容

kvminithart：打开页表，也是下节课的内容

processinit：设置好初始进程或者说设置好进程表单

trapinit/trapinithart：设置好user/kernel mode转换代码

plicinit/plicinithart：设置好中断控制器PLIC（Platform Level Interrupt Controller），我们后面在介绍中断的时候会详细的介绍这部分，这是我们用来与磁盘和console交互方式

binit：分配buffer cache

iinit：初始化inode缓存

fileinit：初始化文件系统

virtio_disk_init：初始化磁盘

userinit：最后当所有的设置都完成了，操作系统也运行起来了，会通过userinit运行第一个进程，这里有点意思，接下来我们看一下userinit

> 在继续之前，这里有什么问题吗？
>
> 学生提问：这里的初始化函数的调用顺序重要吗？
>
> Frans教授：重要，哈哈。一些函数必须在另一些函数之后运行，某几个函数的顺序可能不重要，但是对它们又需要在其他的一些函数之后运行。

指到 `userinit();   // first user process` 这行的时候，可以通过gdb的s指令，跳到userinit内部。

![Snipaste_2022-05-15_01-16-45](./doc/Snipaste_2022-05-15_01-16-45.png)

```c
210 // Set up first user process.
211 void
212 userinit(void)
213 {
214   struct proc *p;
215 
216   p = allocproc();
217   initproc = p;
218 
219   // allocate one user page and copy init's instructions
220   // and data into it.
221   uvminit(p->pagetable, initcode, sizeof(initcode));
222   p->sz = PGSIZE;
223 
224   // prepare for the very first "return" from kernel to user.
225   p->trapframe->epc = 0;      // user program counter
226   p->trapframe->sp = PGSIZE;  // user stack pointer
227 
228   safestrcpy(p->name, "initcode", sizeof(p->name));
229   p->cwd = namei("/");
230 
231   p->state = RUNNABLE;
232 
233   release(&p->lock);
234 }
```

上图是userinit函数，右边是源码，左边是gdb视图。userinit有点像是胶水代码/Glue code（胶水代码不实现具体的功能，只是为了适配不同的部分而存在），它利用了XV6的特性，并启动了第一个进程。我们总是需要有一个用户进程在运行，这样才能实现与操作系统的交互，所以这里需要一个小程序来初始化第一个用户进程。这个小程序定义在initcode中。

```c
198 // a user program that calls exec("/init")
199 // od -t xC initcode
200 uchar initcode[] = {
201   0x17, 0x05, 0x00, 0x00, 0x13, 0x05, 0x45, 0x02,
202   0x97, 0x05, 0x00, 0x00, 0x93, 0x85, 0x35, 0x02,
203   0x93, 0x08, 0x70, 0x00, 0x73, 0x00, 0x00, 0x00,
204   0x93, 0x08, 0x20, 0x00, 0x73, 0x00, 0x00, 0x00,
205   0xef, 0xf0, 0x9f, 0xff, 0x2f, 0x69, 0x6e, 0x69,
206   0x74, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, 0x00,
207   0x00, 0x00, 0x00, 0x00
208 };
```

这里直接是程序的二进制形式，它会链接或者在内核中直接静态定义。实际上，这段代码对应了下面的汇编程序。

```assembly
$ cat user/initcode.S 
# Initial process that execs /init.
# This code runs in user space.

#include "syscall.h"

# exec(init, argv)
.globl start
start:
        la a0, init
        la a1, argv
        li a7, SYS_exec
        ecall

# for(;;) exit();
exit:
        li a7, SYS_exit
        ecall
        jal exit

# char init[] = "/init\0";
init:
  .string "/init\0"

# char *argv[] = { init, 0 };
.p2align 2
argv:
  .long init
  .long 0

```

这个汇编程序中，它首先将init中的地址加载到a0（la a0, init），argv中的地址加载到a1（la a1, argv），exec系统调用对应的数字加载到a7（li a7, SYS_exec），最后调用ECALL。所以这里执行了3条指令，之后在第4条指令将控制权交给了操作系统。

如果我在syscall中设置一个断点，

```shell
(gdb) b syscall
Breakpoint 3 at 0x80002b92: file kernel/syscall.c, line 164.
```

并让程序运行起来。userinit会创建初始进程，返回到用户空间，执行刚刚介绍的3条指令，再回到内核空间。这里是任何XV6用户会使用到的第一个系统调用。让我们来看一下会发生什么。通过在gdb中执行c，让程序运行起来，我们现在进入到了syscall函数。

![Snipaste_2022-05-15_01-34-22](./doc/Snipaste_2022-05-15_01-34-22.png)

我们可以查看syscall的代码，

![Snipaste_2022-05-15_01-36-09](./doc/Snipaste_2022-05-15_01-36-09.png)

*num = p->trapframe->a7* 会读取使用的系统调用对应的整数。当代码执行完这一行之后，我们可以在gdb中打印num，可以看到是7。

如果我们查看syscall.h，可以看到7对应的是exec系统调用。

```shell
$ cat kernel/syscall.h 
// ...
#define SYS_exec    7
// ...
```

所以，这里本质上是告诉内核，某个用户应用程序执行了ECALL指令，并且想要调用exec系统调用。

`*p->trapframe->a0 = syscall[num]()*` 这一行是实际执行系统调用。这里可以看出，num用来索引一个数组，这个数组是一个函数指针数组，可以预期的是syscall[7]对应了exec的入口函数。我们跳到这个函数中去，可以看到，我们现在在sys_exec函数中。

![Snipaste_2022-05-15_01-39-58](./doc/Snipaste_2022-05-15_01-39-58.png)



```c
$ vim kernel/sysfile.c 
415 uint64
416 sys_exec(void)
417 {
418   char path[MAXPATH], *argv[MAXARG];
419   int i;
420   uint64 uargv, uarg;
421 
422   if(argstr(0, path, MAXPATH) < 0 || argaddr(1, &uargv) < 0){
423     return -1;
424   }
425   memset(argv, 0, sizeof(argv));
426   for(i=0;; i++){
427     if(i >= NELEM(argv)){
428       goto bad;
429     }
430     if(fetchaddr(uargv+sizeof(uint64)*i, (uint64*)&uarg) < 0){
431       goto bad;
432     }
433     if(uarg == 0){
434       argv[i] = 0;
435       break;
436     }
437     argv[i] = kalloc();
438     if(argv[i] == 0)
439       goto bad;
440     if(fetchstr(uarg, argv[i], PGSIZE) < 0)
441       goto bad;
442   }
```

sys_exec中的第一件事情是从用户空间读取参数，它会读取path，也就是要执行程序的文件名。这里首先会为参数分配空间，然后从用户空间将参数拷贝到内核空间。之后我们打印path，

```shell
(gdb) p path
$2 = "/init\000\000\000\020\337\377\377?\000\000\000\060\337\377\377?\000\000\000\060\337\377\377?\000\000\000\b~\001\200\000\000\000\000\060\337\377\377?\000
\000\000P\337\377\377?\000\000\000D\r\000\200\000\000\000\000\000~\001\200\000\000\000\000\360}\001\200\000\000\000\000p\337\377\377?\000\000\000\240\060\000\
200\000\000\000\000\b\033\002\200\000\000\000\000\360}\001\200\000\000\000\000\220\337\377\377?\000\000\000\220\337\377\377?\000\000"
```

可以看到传入的就是init程序。所以，综合来看，initcode完成了通过exec调用init程序。让我们来看看init程序，

$ cat user/init.c

```c
// init: The initial user-level program

#include "kernel/types.h"
#include "kernel/stat.h"
#include "kernel/spinlock.h"
#include "kernel/sleeplock.h"
#include "kernel/fs.h"
#include "kernel/file.h"
#include "user/user.h"
#include "kernel/fcntl.h"

char *argv[] = { "sh", 0 };

int
main(void)
{
  int pid, wpid;

  if(open("console", O_RDWR) < 0){
    mknod("console", CONSOLE, 0);
    open("console", O_RDWR);
  }
  dup(0);  // stdout
  dup(0);  // stderr

  for(;;){
    printf("init: starting sh\n");
    pid = fork();
    if(pid < 0){
      printf("init: fork failed\n");
      exit(1);
    }
    if(pid == 0){
      exec("sh", argv);
      printf("init: exec sh failed\n");
      exit(1);
    }

    for(;;){
      // this call to wait() returns if the shell exits,
      // or if a parentless process exits.
      wpid = wait((int *) 0);
      if(wpid == pid){
        // the shell exited; restart it.
        break;
      } else if(wpid < 0){
        printf("init: wait returned an error\n");
        exit(1);
      } else {
        // it was a parentless process; do nothing.
      }
    }
  }
}

```

init会为用户空间设置好一些东西，比如配置好console，调用fork，并在fork出的子进程中执行shell。

最终的效果就是Shell运行起来了。如果我再次运行代码，我还会陷入到syscall中的断点，并且同样也是调用exec系统调用，只是这次是通过exec运行Shell。当Shell运行起来之后，我们可以从QEMU看到Shell。

```shell
$ make CPUS=1 qemu-gdb
sed "s/:1234/:25501/" < .gdbinit.tmpl-riscv > .gdbinit
*** Now run 'gdb' in another window.
qemu-system-riscv64 -machine virt -bios none -kernel kernel/kernel -m 128M -smp 1 -nographic -drive file=fs.img,if=none,format=raw,id=x0 -device virtio-blk-device,drive=x0,bus=virtio-mmio-bus.0 -S -gdb tcp::25501

xv6 kernel is booting

init: start

```

这里简单的介绍了一下XV6是如何从0开始直到第一个Shell程序运行起来。并且我们也看了一下第一个系统调用是在什么时候发生的。我们并没有看系统调用背后的具体机制，这个在后面会介绍。但是目前来说，这些对于你们完成这周的syscall lab是足够了。这些就是你们在实验中会用到的部分。这里有什么问题吗？

> 学生提问：我们会处理网络吗，比如说网络相关的实验？
>
> Frans教授：是的，最后一个lab中你们会实现一个网络驱动。你们会写代码与硬件交互，操纵连接在RISC-V主板上网卡的驱动，以及寄存器，再向以太网发送一些网络报文。

好的，最后让我总结一下。因为没有涉及到太多的细节，我认为syscall lab可能会比上一个utils lab简单些，但是下一个实验会更加的复杂。要想做好实验总是会比较难，别总是拖到最后才完成实验，这样有什么奇怪的问题我们还能帮帮你。好了就这样，我退了，下节课再见~
