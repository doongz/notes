# Lab4: traps

本实验探索如何使用陷阱实现系统调用。您将首先使用栈做一个热身练习，然后实现一个用户级陷阱处理的示例。

> [!WARNING|label:Attention]
> 开始编码之前，请阅读xv6手册的第4章和相关源文件：
>
> - ***kernel/trampoline.S***：涉及从用户空间到内核空间再到内核空间的转换的程序集
> - ***kernel/trap.c***：处理所有中断的代码

要启动实验，请切换到`traps`分支：

```bash
$ git fetch
$ git checkout traps
$ make clean
```

# RISC-V assembly (easy)

理解一点RISC-V汇编是很重要的，你应该在6.004中接触过。xv6仓库中有一个文件***user/call.c***。执行`make fs.img`编译它，并在***user/call.asm***中生成可读的汇编版本。

阅读***call.asm***中函数`g`、`f`和`main`的代码。RISC-V的使用手册在[参考页](https://pdos.csail.mit.edu/6.828/2020/reference.html)上。以下是您应该回答的一些问题（将答案存储在***answers-traps.txt***文件中）：

1. 哪些寄存器保存函数的参数？例如，在`main`对`printf`的调用中，哪个寄存器保存13？
2. `main`的汇编代码中对函数`f`的调用在哪里？对`g`的调用在哪里(提示：编译器可能会将函数内联）
3. `printf`函数位于哪个地址？
4. 在`main`中`printf`的`jalr`之后的寄存器`ra`中有什么值？
5. 运行以下代码。

```c
unsigned int i = 0x00646c72;
printf("H%x Wo%s", 57616, &i);
```

程序的输出是什么？这是将字节映射到字符的[ASCII码表](http://web.cs.mun.ca/~michael/c/ascii-table.html)。

输出取决于RISC-V小端存储的事实。如果RISC-V是大端存储，为了得到相同的输出，你会把`i`设置成什么？是否需要将`57616`更改为其他值？

[这里有一个小端和大端存储的描述](http://www.webopedia.com/TERM/b/big_endian.html)和一个[更异想天开的描述](http://www.networksorcery.com/enp/ien/ien137.txt)。

6. 在下面的代码中，“`y=`”之后将打印什么(注：答案不是一个特定的值）？为什么会发生这种情况？

```c
printf("x=%d y=%d", 3);
```

答案：

**(1)**.  在a0-a7中存放参数，13存放在a2中 

**(2)**.  在C代码中，main调用f，f调用g。而在生成的汇编中，main函数进行了内联优化处理。

从代码`li a1,12`可以看出，main直接计算出了结果并储存 

**(3)**. 在`0x630`

**(4)**. `auipc`(Add Upper Immediate to PC)：`auipc rd imm`，将高位立即数加到PC上，从下面的指令格式可以看出，该指令将20位的立即数左移12位之后（右侧补0）加上PC的值，将结果保存到dest位置，图中为`rd`寄存器

![img](../doc/p1.png)

下面来看`jalr` (jump and link register)：`jalr rd, offset(rs1)`跳转并链接寄存器。jalr指令会将当前PC+4保存在rd中，然后跳转到指定的偏移地址`offset(rs1)`。

![img](../doc/p2.png)

来看XV6的代码：

```asm
  30: 00000097       auipc ra,0x0
  34: 600080e7       jalr  1536(ra) # 630 <printf>
```

`bin(int("00000097", 16)) `

`'0b10010111'`

第一行代码：`00000097H=00...0 0000 1001 0111B`，对比指令格式，可见imm=0，dest=00001，opcode=0010111，对比汇编指令可知，auipc的操作码是0010111，ra寄存器代码是00001。这行代码将0x0左移12位（还是0x0）加到PC（当前为0x30）上并存入ra中，即ra中保存的是0x30

第2行代码：`600080e7H=0110 0...0 1000 0000 1110 0111B`，可见imm=0110 0000 0000，rs1=00001，funct3=000，rd=00001，opcode=1100111，rs1和rd的知识码都是00001，即都为寄存器`ra`。这对比jalr的标准格式有所不同，可能是此两处使用寄存器相同时，汇编中可以省略`rd`部分。

ra中保存的是0x30，加上0x600后为0x630，即`printf`的地址，执行此行代码后，将跳转到printf函数执行，并将PC+4=0X34+0X4=0X38保存到`ra`中，供之后返回使用。

**(5)**. 57616=0xE110，0x00646c72小端存储为72-6c-64-00，对照ASCII码表

 72:r 6c:l 64:d 00:充当字符串结尾标识

```c
#include <stdio.h>

int main(){
  unsigned int i = 0x00646c72;
  printf("H%x Wo%s", 57616, &i);
}

// He110 World
```

 若为大端存储，i应改为0x726c6400，不需改变57616 

"0x" 16进制

"0b" 2进制

```
>>> hex(57616)
'0xe110'
```

**(6)**. 原本需要两个参数，却只传入了一个，因此y=后面打印的结果取决于之前a2中保存的数据 

```
x=3 y=-1154578488
x=3 y=-1171191864
```

b.c

```c
#include <stdio.h>

int main(){
	printf("x=%d y=%d", 3);
}
```

```shell
clang -S b.c
```

b.s

```assembly
	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 12, 0	sdk_version 12, 3
	.globl	_main                           ## -- Begin function main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	leaq	L_.str(%rip), %rdi
	movl	$3, %esi
	movb	$0, %al
	callq	_printf
	xorl	%eax, %eax
	popq	%rbp
	retq
	.cfi_endproc
                                        ## -- End function
	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"x=%d y=%d"

.subsections_via_symbols
```

`printf("x=%d y=%d", 3);`

```assembly
void main(void) {
   0:	1141                	addi	sp,sp,-16
   2:	e406                	sd	ra,8(sp)
   4:	e022                	sd	s0,0(sp)
   6:	0800                	addi	s0,sp,16
  printf("x=%d y=%d", 3);
   8:	458d                	li	a1,3
   a:	00000517          	auipc	a0,0x0
   e:	7ae50513          	addi	a0,a0,1966 # 7b8 <malloc+0xe8>
  12:	00000097          	auipc	ra,0x0
  16:	600080e7          	jalr	1536(ra) # 612 <printf>
  exit(0);
  1a:	4501                	li	a0,0
  1c:	00000097          	auipc	ra,0x0
  20:	27e080e7          	jalr	638(ra) # 29a <exit>
```

`printf("x=%d y=%d", 3, 5);`

```assembly
void main(void) {
   0:	1141                	addi	sp,sp,-16
   2:	e406                	sd	ra,8(sp)
   4:	e022                	sd	s0,0(sp)
   6:	0800                	addi	s0,sp,16
  printf("x=%d y=%d", 3, 5);
   8:	4615                	li	a2,5
   a:	458d                	li	a1,3
   c:	00000517          	auipc	a0,0x0
  10:	7ac50513          	addi	a0,a0,1964 # 7b8 <malloc+0xe6>
  14:	00000097          	auipc	ra,0x0
  18:	600080e7          	jalr	1536(ra) # 614 <printf>
  exit(0);
  1c:	4501                	li	a0,0
  1e:	00000097          	auipc	ra,0x0
  22:	27e080e7          	jalr	638(ra) # 29c <exit>
  
  
void
printf(const char *fmt, ...)
{
 614:	711d                	addi	sp,sp,-96
 616:	ec06                	sd	ra,24(sp)
 618:	e822                	sd	s0,16(sp)
 61a:	1000                	addi	s0,sp,32
 61c:	e40c                	sd	a1,8(s0)
 61e:	e810                	sd	a2,16(s0)
 620:	ec14                	sd	a3,24(s0)
 622:	f018                	sd	a4,32(s0)
 624:	f41c                	sd	a5,40(s0)
 626:	03043823          	sd	a6,48(s0)
 62a:	03143c23          	sd	a7,56(s0)
  va_list ap;

  va_start(ap, fmt);
 62e:	00840613          	addi	a2,s0,8
 632:	fec43423          	sd	a2,-24(s0)
  vprintf(1, fmt, ap);
 636:	85aa                	mv	a1,a0
 638:	4505                	li	a0,1
 63a:	00000097          	auipc	ra,0x0
 63e:	dce080e7          	jalr	-562(ra) # 408 <vprintf>
}
```

调试：

```
make qemu-gdb
riscv64-unknown-elf-gdb

(gdb) b *0x612
(gdb) c
```



# Backtrace(moderate)

回溯(Backtrace)通常对于调试很有用：它是一个存放于栈上用于指示错误发生位置的函数调用列表。

在***kernel/printf.c***中实现名为`backtrace()`的函数。在`sys_sleep`中插入一个对此函数的调用，然后运行`bttest`，它将会调用`sys_sleep`。你的输出应该如下所示：

```bash
backtrace:
0x0000000080002cda
0x0000000080002bb6
0x0000000080002898
```

在`bttest`退出qemu后。在你的终端：地址或许会稍有不同，但如果你运行`addr2line -e kernel/kernel`（或`riscv64-unknown-elf-addr2line -e kernel/kernel`），并将上面的地址剪切粘贴如下：

```bash
$ addr2line -e kernel/kernel
0x0000000080002de2
0x0000000080002f4a
0x0000000080002bfc
Ctrl-D
```

你应该看到类似下面的输出：

```
kernel/sysproc.c:74
kernel/syscall.c:224
kernel/trap.c:85
```

编译器向每一个栈帧中放置一个帧指针（frame pointer）保存调用者帧指针的地址。你的`backtrace`应当使用这些帧指针来遍历栈，并在每个栈帧中打印保存的返回地址。

**提示：**

- 在***kernel/defs.h***中添加`backtrace`的原型，那样你就能在`sys_sleep`中引用`backtrace`

- GCC编译器将当前正在执行的函数的帧指针保存在`s0`寄存器，将下面的函数添加到***kernel/riscv.h***

```c
static inline uint64
r_fp()
{
  uint64 x;
  asm volatile("mv %0, s0" : "=r" (x) );
  return x;
}
```

并在`backtrace`中调用此函数来读取当前的帧指针。这个函数使用[内联汇编](https://gcc.gnu.org/onlinedocs/gcc/Using-Assembly-Language-with-C.html)来读取`s0`

- 这个[课堂笔记](https://pdos.csail.mit.edu/6.828/2020/lec/l-riscv-slides.pdf)中有张栈帧布局图。注意返回地址位于栈帧帧指针的固定偏移(-8)位置，并且保存的帧指针位于帧指针的固定偏移(-16)位置

![img](../doc/p2-333.png)

- XV6在内核中以页面对齐的地址为每个栈分配一个页面。你可以通过`PGROUNDDOWN(fp)`和`PGROUNDUP(fp)`（参见***kernel/riscv.h***）来计算栈页面的顶部和底部地址。这些数字对于`backtrace`终止循环是有帮助的。

一旦你的`backtrace`能够运行，就在***kernel/printf.c***的`panic`中调用它，那样你就可以在`panic`发生时看到内核的`backtrace`。

**解答**

kernel/printf.c

这个函数就是实现曾经调用函数地址的回溯，这个功能在日常的编程中也经常见到，编译器报错时就是类似的逻辑，只不过题目的要求较为简单，只用打印程序地址，而实际的报错中往往打印程序文件名，函数名以及行号等信息（最后的可选练习就是实现这样的功能）。

```c
/**
 * @brief backtrace 回溯函数调用的返回地址
 */
void
backtrace(void) {
  printf("backtrace:\n");
  // 读取当前帧指针
  uint64 fp = r_fp();
  while (PGROUNDUP(fp) - PGROUNDDOWN(fp) == PGSIZE) {
    // 返回地址保存在-8偏移的位置
    uint64 ret_addr = *(uint64*)(fp - 8);
    printf("%p\n", ret_addr);
    // 前一个帧指针保存在-16偏移的位置
    fp = *(uint64*)(fp - 16);
  }
}
```

根据提示：返回地址位于栈帧帧指针的固定偏移(-8)位置，并且保存的帧指针位于帧指针的固定偏移(-16)位置。先使用`r_fp()`读取当前的帧指针，然后读出返回地址并打印，再将`fp`定位到前一个帧指针的位置继续读取即可。

根据提示：XV6在内核中以页面对齐的地址为每个栈分配一个页面。使用`PGROUNDUP(fp) - PGROUNDDOWN(fp) == PGSIZE`判断当前的`fp`是否被分配了一个页面来终止循环。

kernel/sysproc.c

```c
backtrace();
```

kernel/defs.h

```c
// sysproc.c
void backtrace(void);
```

```
$ bttest
backtrace:
0x0000000080002cec
0x0000000080002bc6
0x00000000800028b0

riscv64-unknown-elf-addr2line -e kernel/kernel
0x0000000080002cec
0x0000000080002bc6
0x00000000800028b0

xv6-labs-2020/kernel/sysproc.c:63
xv6-labs-2020/kernel/syscall.c:140
xv6-labs-2020/kernel/trap.c:76
```



# Alarm(Hard)

> [!TIP|label:YOUR JOB]
> 在这个练习中你将向XV6添加一个特性，在进程使用CPU的时间内，XV6定期向进程发出警报。这对于那些希望限制CPU时间消耗的受计算限制的进程，或者对于那些计算的同时执行某些周期性操作的进程可能很有用。更普遍的来说，你将实现用户级中断/故障处理程序的一种初级形式。例如，你可以在应用程序中使用类似的一些东西处理页面故障。如果你的解决方案通过了`alarmtest`和`usertests`就是正确的。

你应当添加一个新的`sigalarm(interval, handler)`系统调用，如果一个程序调用了`sigalarm(n, fn)`，那么每当程序消耗了CPU时间达到n个“滴答”，内核应当使应用程序函数`fn`被调用。当`fn`返回时，应用应当在它离开的地方恢复执行。在XV6中，一个滴答是一段相当任意的时间单元，取决于硬件计时器生成中断的频率。如果一个程序调用了`sigalarm(0, 0)`，系统应当停止生成周期性的报警调用。

你将在XV6的存储库中找到名为***user/alarmtest.c***的文件。将其添加到***Makefile***。注意：你必须添加了`sigalarm`和`sigreturn`系统调用后才能正确编译（往下看）。

`alarmtest`在`test0`中调用了`sigalarm(2, periodic)`来要求内核每隔两个滴答强制调用`periodic()`，然后旋转一段时间。你可以在***user/alarmtest.asm***中看到`alarmtest`的汇编代码，这或许会便于调试。当`alarmtest`产生如下输出并且`usertests`也能正常运行时，你的方案就是正确的：

```bash
$ alarmtest
test0 start
........alarm!
test0 passed
test1 start
...alarm!
..alarm!
...alarm!
..alarm!
...alarm!
..alarm!
...alarm!
..alarm!
...alarm!
..alarm!
test1 passed
test2 start
................alarm!
test2 passed
$ usertests
...
ALL TESTS PASSED
$
```

当你完成后，你的方案也许仅有几行代码，但如何正确运行是一个棘手的问题。我们将使用原始存储库中的***alarmtest.c***版本测试您的代码。你可以修改***alarmtest.c***来帮助调试，但是要确保原来的`alarmtest`显示所有的测试都通过了。

## test0: invoke handler(调用处理程序)

首先修改内核以跳转到用户空间中的报警处理程序，这将导致`test0`打印“alarm!”。不用担心输出“alarm!”之后会发生什么；如果您的程序在打印“alarm！”后崩溃，对于目前来说也是正常的。以下是一些**提示**：

- 您需要修改***Makefile***以使***alarmtest.c***被编译为xv6用户程序。

- 放入***user/user.h***的正确声明是：

```c
int sigalarm(int ticks, void (*handler)());
int sigreturn(void);
```

- 更新***user/usys.pl***（此文件生成***user/usys.S***）、***kernel/syscall.h***和***kernel/syscall.c***以允许`alarmtest`调用`sigalarm`和`sigreurn`系统调用。

- 目前来说，你的`sys_sigreturn`系统调用返回应该是零。

- 你的`sys_sigalarm()`应该将报警间隔和指向处理程序函数的指针存储在`struct proc`的新字段中（位于***kernel/proc.h***）。

- 你也需要在`struct proc`新增一个新字段。用于跟踪自上一次调用（或直到下一次调用）到进程的报警处理程序间经历了多少滴答；您可以在***proc.c***的`allocproc()`中初始化`proc`字段。

- 每一个滴答声，硬件时钟就会强制一个中断，这个中断在***kernel/trap.c***中的`usertrap()`中处理。

- 如果产生了计时器中断，您只想操纵进程的报警滴答；你需要写类似下面的代码

```c
if(which_dev == 2) ...
```

- 仅当进程有未完成的计时器时才调用报警函数。请注意，用户报警函数的地址可能是0（例如，在***user/alarmtest.asm***中，`periodic`位于地址0）。

- 您需要修改`usertrap()`，以便当进程的报警间隔期满时，用户进程执行处理程序函数。当RISC-V上的陷阱返回到用户空间时，什么决定了用户空间代码恢复执行的指令地址？

- 如果您告诉qemu只使用一个CPU，那么使用gdb查看陷阱会更容易，这可以通过运行

```bash
make CPUS=1 qemu-gdb
```

- 如果`alarmtest`打印“alarm!”，则您已成功。

## test1/test2(): resume interrupted code(恢复被中断的代码)

`alarmtest`打印“alarm!”后，很可能会在`test0`或`test1`中崩溃，或者`alarmtest`（最后）打印“test1 failed”，或者`alarmtest`未打印“test1 passed”就退出。要解决此问题，必须确保完成报警处理程序后返回到用户程序最初被计时器中断的指令执行。必须确保寄存器内容恢复到中断时的值，以便用户程序在报警后可以不受干扰地继续运行。最后，您应该在每次报警计数器关闭后“重新配置”它，以便周期性地调用处理程序。

作为一个起始点，我们为您做了一个设计决策：用户报警处理程序需要在完成后调用`sigreurn`系统调用。请查看***alarmtest.c***中的`periodic`作为示例。这意味着您可以将代码添加到`usertrap`和`sys_sigreurn`中，这两个代码协同工作，以使用户进程在处理完警报后正确恢复。

**提示：**

- 您的解决方案将要求您保存和恢复寄存器——您需要保存和恢复哪些寄存器才能正确恢复中断的代码？(提示：会有很多）

- 当计时器关闭时，让`usertrap`在`struct proc`中保存足够的状态，以使`sigreurn`可以正确返回中断的用户代码。

- 防止对处理程序的重复调用——如果处理程序还没有返回，内核就不应该再次调用它。`test2`测试这个。

- 一旦通过`test0`、`test1`和`test2`，就运行`usertests`以确保没有破坏内核的任何其他部分。

---

这项练习要实现定期的警报。首先是要通过`test0`，如何调用处理程序是主要的问题。程序计数器的过程是这样的：

1. `ecall`指令中将PC保存到SEPC
2. 在`usertrap`中将SEPC保存到`p->trapframe->epc`
3. `p->trapframe->epc`加4指向下一条指令
4. 执行系统调用
5. 在`usertrapret`中将SEPC改写为`p->trapframe->epc`中的值
6. 在`sret`中将PC设置为SEPC的值

可见执行系统调用后返回到用户空间继续执行的指令地址是由`p->trapframe->epc`决定的，因此在`usertrap`中主要就是完成它的设置工作。

**(1)**. 在`struct proc`中增加字段，同时记得在`allocproc`中将它们初始化为0，并在`freeproc`中也设为0

```c
int alarm_interval;          // 报警间隔
void (*alarm_handler)();     // 报警处理函数
int ticks_count;             // 两次报警间的滴答计数
```

**(2)**. 在`sys_sigalarm`中读取参数

```c
uint64
sys_sigalarm(void) {
  if(argint(0, &myproc()->alarm_interval) < 0 ||
    argaddr(1, (uint64*)&myproc()->alarm_handler) < 0)
    return -1;

  return 0;
}
```

**(3)**. 修改usertrap()

```c
// give up the CPU if this is a timer interrupt.
if(which_dev == 2) {
    if(++p->ticks_count == p->alarm_interval) {
        // 更改陷阱帧中保留的程序计数器
        p->trapframe->epc = (uint64)p->alarm_handler;
        p->ticks_count = 0;
    }
    yield();
}
```

接下来要通过`test1`和`test2`，要解决的主要问题是寄存器保存恢复和防止重复执行的问题。考虑一下没有alarm时运行的大致过程

1. 进入内核空间，保存用户寄存器到进程陷阱帧
2. 陷阱处理过程
3. 恢复用户寄存器，返回用户空间

而当添加了alarm后，变成了以下过程

1. 进入内核空间，保存用户寄存器到进程陷阱帧
2. 陷阱处理过程
3. 恢复用户寄存器，返回用户空间，但此时返回的并不是进入陷阱时的程序地址，而是处理函数`handler`的地址，而`handler`可能会改变用户寄存器

因此我们要在`usertrap`中再次保存用户寄存器，当`handler`调用`sigreturn`时将其恢复，并且要防止在`handler`执行过程中重复调用，过程如下

**(1)**. 再在`struct proc`中新增两个字段

```c
int is_alarming;                    // 是否正在执行告警处理函数
struct trapframe* alarm_trapframe;  // 告警陷阱帧
```

**(2)**. 在allocproc和freeproc中设定好相关分配，回收内存的代码

```c
/**
 * allocproc.c
 */
// 初始化告警字段
if((p->alarm_trapframe = (struct trapframe*)kalloc()) == 0) {
    freeproc(p);
    release(&p->lock);
    return 0;
}
p->is_alarming = 0;
p->alarm_interval = 0;
p->alarm_handler = 0;
p->ticks_count = 0;

/**
 * freeproc.c
 */
if(p->alarm_trapframe)
    kfree((void*)p->alarm_trapframe);
p->alarm_trapframe = 0;
p->is_alarming = 0;
p->alarm_interval = 0;
p->alarm_handler = 0;
p->ticks_count = 0;
```

**(3)**. 更改usertrap函数，保存进程陷阱帧`p->trapframe`到`p->alarm_trapframe`

```c
// give up the CPU if this is a timer interrupt.
if(which_dev == 2) {
  if(p->alarm_interval != 0 && ++p->ticks_count == p->alarm_interval && p->is_alarming == 0) {
    // 保存寄存器内容
    memmove(p->alarm_trapframe, p->trapframe, sizeof(struct trapframe));
    // 更改陷阱帧中保留的程序计数器，注意一定要在保存寄存器内容后再设置epc
    p->trapframe->epc = (uint64)p->alarm_handler;
    p->ticks_count = 0;
    p->is_alarming = 1;
  }
  yield();
}
```

**(4)**. 更改`sys_sigreturn`，恢复陷阱帧

```c
uint64
sys_sigreturn(void) {
  memmove(myproc()->trapframe, myproc()->alarm_trapframe, sizeof(struct trapframe));
  myproc()->is_alarming = 0;
  return 0;
}
```

https://github.com/dowalle/xv6-labs-2020/commit/a1cfc6bb3d398513f13153f6ad4f8de329486114







# 可选的挑战练习

- 在`backtrace()`中打印函数的名称和行号，而不仅仅是数字化的地址。(hard)