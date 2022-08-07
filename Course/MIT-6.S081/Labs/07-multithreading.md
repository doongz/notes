# Lab7: Multithreading

本实验将使您熟悉多线程。您将在用户级线程包中实现线程之间的切换，使用多个线程来加速程序，并实现一个屏障。

> [!WARNING|label:Attention]
> 在编写代码之前，您应该确保已经阅读了xv6手册中的“第7章: 调度”，并研究了相应的代码。

要启动实验，请切换到thread分支：

```bash
$ git fetch
$ git checkout thread
$ make clean
```

# Uthread: switching between threads (moderate)

在本练习中，您将为用户级线程系统设计上下文切换机制，然后实现它。为了让您开始，您的xv6有两个文件：***user/uthread.c***和***user/uthread_switch.S***，以及一个规则：运行在***Makefile***中以构建`uthread`程序。***uthread.c***包含大多数用户级线程包，以及三个简单测试线程的代码。线程包缺少一些用于创建线程和在线程之间切换的代码。

> [!TIP|label:YOUR JOB]
> 您的工作是提出一个创建线程和保存/恢复寄存器以在线程之间切换的计划，并实现该计划。完成后，`make grade`应该表明您的解决方案通过了`uthread`测试。

完成后，在xv6上运行`uthread`时应该会看到以下输出（三个线程可能以不同的顺序启动）：

```bash
$ make qemu
...
$ uthread
thread_a started
thread_b started
thread_c started
thread_c 0
thread_a 0
thread_b 0
thread_c 1
thread_a 1
thread_b 1
...
thread_c 99
thread_a 99
thread_b 99
thread_c: exit after 100
thread_a: exit after 100
thread_b: exit after 100
thread_schedule: no runnable threads
$
```

该输出来自三个测试线程，每个线程都有一个循环，该循环打印一行，然后将CPU让出给其他线程。

然而在此时还没有上下文切换的代码，您将看不到任何输出。

您需要将代码添加到***user/uthread.c***中的`thread_create()`和`thread_schedule()`，以及***user/uthread_switch.S***中的`thread_switch`。一个目标是确保当`thread_schedule()`第一次运行给定线程时，该线程在自己的栈上执行传递给`thread_create()`的函数。另一个目标是确保`thread_switch`保存被切换线程的寄存器，恢复切换到线程的寄存器，并返回到后一个线程指令中最后停止的点。您必须决定保存/恢复寄存器的位置；修改`struct thread`以保存寄存器是一个很好的计划。您需要在`thread_schedule`中添加对`thread_switch`的调用；您可以将需要的任何参数传递给`thread_switch`，但目的是将线程从`t`切换到`next_thread`。



**提示：**

- `thread_switch`只需要保存/还原被调用方保存的寄存器（callee-save register，参见LEC5使用的文档《Calling Convention》）。为什么？
- 您可以在***user/uthread.asm***中看到`uthread`的汇编代码，这对于调试可能很方便。
- 这可能对于测试你的代码很有用，使用`make qemu-gdb` `riscv64-linux-gnu-gdb`的单步调试通过你的`thread_switch`，你可以按这种方法开始：

```bash
(gdb) file user/_uthread
Reading symbols from user/_uthread...
(gdb) b uthread.c:60
(gdb) c
Continuing. 
```

```
xv6 kernel is booting
hart 2 starting
hart 1 starting
init: starting sh
$ uthread

```

这将在***uthread.c***的第60行设置断点。断点可能会（也可能不会）在运行`uthread`之前触发。为什么会出现这种情况？

一旦您的xv6 shell运行，键入“`uthread`”，gdb将在第60行停止。现在您可以键入如下命令来检查`uthread`的状态：

`(gdb) p/x *next_thread`

使用“`x`”，您可以检查内存位置的内容：

`(gdb) x/x next_thread->stack`

您可以跳到`thread_switch` 的开头，如下：

`(gdb) b thread_switch`

`(gdb) c`

您可以使用以下方法单步执行汇编指令：

`(gdb) si`

gdb的在线文档在[这里](https://sourceware.org/gdb/current/onlinedocs/gdb/)。

---

本实验是在给定的代码基础上实现用户级线程切换，相比于XV6中实现的内核级线程，这个要简单许多。因为是用户级线程，不需要设计用户栈和内核栈，用户页表和内核页表等等切换，所以本实验中只需要一个类似于`context`的结构，而不需要费尽心机的维护`trapframe`

(1). 定义存储上下文的结构体`tcontext`

```c
// 用户线程的上下文结构体
struct tcontext {
  uint64 ra;
  uint64 sp;

  // callee-saved
  uint64 s0;
  uint64 s1;
  uint64 s2;
  uint64 s3;
  uint64 s4;
  uint64 s5;
  uint64 s6;
  uint64 s7;
  uint64 s8;
  uint64 s9;
  uint64 s10;
  uint64 s11;
};
```

(2). 修改`thread`结构体，添加`context`字段

```c
struct thread {
  char            stack[STACK_SIZE];  /* the thread's stack */
  int             state;              /* FREE, RUNNING, RUNNABLE */
  struct tcontext context;            /* 用户进程上下文 */
};
```

(3). 模仿***kernel/swtch.S，***在***kernel/uthread_switch.S***中写入如下代码

首先.globl表示这是swtch函数，然后开始swtch函数的汇编实现。

因为a0会被内核刷新成当前进程的结构体起始地址，所以要对a0（a0对应函数的第一个参数，也就是old）做偏移以存放13个寄存器（ra,sp和s0~s11），因为这些寄存器都是64位的，所以每次都要偏移8个字节。sd指的是将寄存器的内容存储到存储器中（如 s0 往 a0 的第16 位开始存）。

ld则相反，会从存储器a1（a1对应函数的第二个参数，也就是new）中读取13个寄存器，完成进程上下文的切换。

这个时候ret，因为ra已经被刷新了，所以会跳转到新进程的指定语句执行新进程。

```asm
.text

/*
* save the old thread's registers,
* restore the new thread's registers.
*/

.globl thread_switch
thread_switch:
    /* YOUR CODE HERE */
    sd ra, 0(a0)
    sd sp, 8(a0)
    sd s0, 16(a0)
    sd s1, 24(a0)
    sd s2, 32(a0)
    sd s3, 40(a0)
    sd s4, 48(a0)
    sd s5, 56(a0)
    sd s6, 64(a0)
    sd s7, 72(a0)
    sd s8, 80(a0)
    sd s9, 88(a0)
    sd s10, 96(a0)
    sd s11, 104(a0)

    ld ra, 0(a1)
    ld sp, 8(a1)
    ld s0, 16(a1)
    ld s1, 24(a1)
    ld s2, 32(a1)
    ld s3, 40(a1)
    ld s4, 48(a1)
    ld s5, 56(a1)
    ld s6, 64(a1)
    ld s7, 72(a1)
    ld s8, 80(a1)
    ld s9, 88(a1)
    ld s10, 96(a1)
    ld s11, 104(a1)
    ret    /* return to ra */
```

(4). 修改`thread_scheduler`，添加线程切换语句

```c
...
if (current_thread != next_thread) {         /* switch threads?  */
  ...
  /* YOUR CODE HERE */
  thread_switch((uint64)&t->context, (uint64)&current_thread->context);
} else
  next_thread = 0;
```

(5). 在`thread_create`中对`thread`结构体做一些初始化设定，主要是`ra`返回地址和`sp`栈指针，其他的都不重要

```c
// YOUR CODE HERE
t->context.ra = (uint64)func;                   // 设定函数返回地址
t->context.sp = (uint64)t->stack + STACK_SIZE;  // 设定栈指针
```

---

user/uthread.c 详解，一个很简单的 用户态线程，但也挺重要的

```c
#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

/* Possible states of a thread: */
#define FREE        0x0
#define RUNNING     0x1
#define RUNNABLE    0x2

#define STACK_SIZE  8192
#define MAX_THREAD  4

// 用户线程的上下文结构体
struct tcontext {
  uint64 ra;
  uint64 sp;

  // callee-saved
  uint64 s0;
  uint64 s1;
  uint64 s2;
  uint64 s3;
  uint64 s4;
  uint64 s5;
  uint64 s6;
  uint64 s7;
  uint64 s8;
  uint64 s9;
  uint64 s10;
  uint64 s11;
};

struct thread {
  char       stack[STACK_SIZE]; /* the thread's stack */
  int        state;             /* FREE, RUNNING, RUNNABLE */
  char       name[16];          /* thread name (debugging) */
  struct tcontext context;      /* 用户进程上下文 */
};

struct thread all_thread[MAX_THREAD];
struct thread *current_thread;
extern void thread_switch(uint64, uint64);

char*
safestrcpy(char *s, const char *t, int n)
{
  char *os;

  os = s;
  if(n <= 0)
    return os;
  while(--n > 0 && (*s++ = *t++) != 0)
    ;
  *s = 0;
  return os;
}
       
void 
thread_init(void)
{
  // main() is thread 0, which will make the first invocation to
  // thread_schedule().  it needs a stack so that the first thread_switch() can
  // save thread 0's state.  thread_schedule() won't run the main thread ever
  // again, because its state is set to RUNNING, and thread_schedule() selects
  // a RUNNABLE thread.
  current_thread = &all_thread[0];
  current_thread->state = RUNNING;
  safestrcpy(current_thread->name, "main", sizeof(current_thread->name));
}

void 
thread_schedule(void)
{
  struct thread *t, *next_thread;

  /* Find another runnable thread. */
  next_thread = 0;
  t = current_thread + 1;
  for(int i = 0; i < MAX_THREAD; i++){
    if(t >= all_thread + MAX_THREAD)
      t = all_thread;
    if(t->state == RUNNABLE) {
      next_thread = t;
      break;
    }
    t = t + 1;
  }

  // thread_a b c 函数中的内容都执行完毕后
  // 会将 current_thread->state = FREE;
  // 因此，thread_a b c 函数中最后一次调用thread_schedule
  // 线程池中的线程都是free，所以 next_thread = 0
  // 所以 最最后只会打印 一条 “thread_schedule: no runnable threads”
  // 整个程序在main函数的thread_schedule(); 就退出了
  // 不会走到 exit(0)
  if (next_thread == 0) {
    printf("thread_schedule: no runnable threads\n");
    exit(-1);
  }

  if (current_thread != next_thread) {         /* switch threads?  */
    next_thread->state = RUNNING;
    t = current_thread;
    current_thread = next_thread;
    /* YOUR CODE HERE
     * Invoke thread_switch to switch from t to next_thread:
     * thread_switch(??, ??);
     */
    thread_switch((uint64)&t->context, (uint64)&current_thread->context);
  } else
    next_thread = 0;
}

void 
thread_create(void (*func)(), const char *thread_name)
{
  struct thread *t;
  // 找到一个空闲的线程
  for (t = all_thread; t < all_thread + MAX_THREAD; t++) {
    if (t->state == FREE) break;
  }
  t->state = RUNNABLE;
  // YOUR CODE HERE
  t->context.ra = (uint64)func;                   // 设定函数返回地址
  t->context.sp = (uint64)t->stack + STACK_SIZE;  // 设定栈指针
  safestrcpy(t->name, thread_name, sizeof(t->name));
}

void 
thread_yield(void)
{
  current_thread->state = RUNNABLE;
  thread_schedule();
}

volatile int a_started, b_started, c_started;
volatile int a_n, b_n, c_n;

void 
thread_a(void)
{
  int i;
  printf("thread_a started\n");
  a_started = 1;  // 标记 thread_a 已经准备好开始执行了
  while(b_started == 0 || c_started == 0)
    // 但是检查了下另外两个线程，还没有准备好
    // 因此 thread_yield 把当前 thread_a 挂起，让出cpu的执行权
    // 再进入 thread_schedule，这个时候 current_thread 还是 a
    // 通过 t = current_thread + 1; next_thread = t;
    // 把 线程b 作为next_thread
    // 再之后就把就执行到 线程b里面
    thread_yield();
  
  for (i = 0; i < 100; i++) {
    printf("thread_a %d\n", i);
    a_n += 1;
    thread_yield();
  }
  printf("thread_a: exit after %d\n", a_n);

  current_thread->state = FREE;
  thread_schedule();
}

void 
thread_b(void)
{
  int i;
  printf("thread_b started\n");
  b_started = 1;
  while(a_started == 0 || c_started == 0)
    // 同样的处理，转到 线程c
    thread_yield();
  
  for (i = 0; i < 100; i++) {
    printf("thread_b %d\n", i);
    b_n += 1;
    thread_yield();
  }
  printf("thread_b: exit after %d\n", b_n);

  current_thread->state = FREE;
  thread_schedule();
}

void 
thread_c(void)
{
  int i;
  printf("thread_c started\n");
  c_started = 1;
  while(a_started == 0 || b_started == 0)
    thread_yield();
  // 此时所有的线程都准备好执行，因此先打印的是 thread_c 0
  // c_n 每增加一 就出让cpu
  for (i = 0; i < 100; i++) {
    printf("thread_c %d\n", i);
    c_n += 1;
    thread_yield();
  }
  printf("thread_c: exit after %d\n", c_n);

  current_thread->state = FREE;
  thread_schedule();
}

int 
main(int argc, char *argv[]) 
{
  a_started = b_started = c_started = 0;
  a_n = b_n = c_n = 0;
  thread_init();
  thread_create(thread_a, "thread_a");
  thread_create(thread_b, "thread_b");
  thread_create(thread_c, "thread_c");
  thread_schedule();
  /* 第一次触发 thread_schedule 时
  会检查线程池 all_thread 中哪个线程是RUNNABLE状态
  这时候先检查出来是 thread_a
  把 main 线程的寄存器信息保存在 main线程的context里面
  再把 thread_a 线程的context信息恢复到寄存器里面
  因此开始执行 thread_a 中的内容，第一行打印的是 thread_a started
  */
  exit(0);
}
```



# Using threads (moderate)

在本作业中，您将探索使用哈希表的线程和锁的并行编程。您应该在具有多个内核的真实Linux或MacOS计算机（不是xv6，不是qemu）上执行此任务。最新的笔记本电脑都有多核处理器。

这个作业使用UNIX的pthread线程库。您可以使用`man pthreads`在手册页面上找到关于它的信息，您可以在web上查看，例如[这里](https://pubs.opengroup.org/onlinepubs/007908799/xsh/pthread_mutex_lock.html)、[这里](https://pubs.opengroup.org/onlinepubs/007908799/xsh/pthread_mutex_init.html)和[这里](https://pubs.opengroup.org/onlinepubs/007908799/xsh/pthread_create.html)。

文件***notxv6/ph.c***包含一个简单的哈希表，如果单个线程使用，该哈希表是正确的，但是多个线程使用时，该哈希表是不正确的。在您的xv6主目录（可能是`~/xv6-labs-2020`）中，键入以下内容：

```bash
$ make ph
$ ./ph 1
```

请注意，要构建`ph`，***Makefile***使用操作系统的gcc，而不是6.S081的工具。`ph`的参数指定在哈希表上执行`put`和`get`操作的线程数。运行一段时间后，`ph 1`将产生与以下类似的输出：

```
100000 puts, 3.991 seconds, 25056 puts/second
0: 0 keys missing
100000 gets, 3.981 seconds, 25118 gets/second
```

您看到的数字可能与此示例输出的数字相差两倍或更多，这取决于您计算机的速度、是否有多个核心以及是否正在忙于做其他事情。

`ph`运行两个基准程序。首先，它通过调用`put()`将许多键添加到哈希表中，并以每秒为单位打印puts的接收速率。之后它使用`get()`从哈希表中获取键。它打印由于puts而应该在哈希表中但丢失的键的数量（在本例中为0），并以每秒为单位打印gets的接收数量。

通过给`ph`一个大于1的参数，可以告诉它同时从多个线程使用其哈希表。试试`ph 2`：

```bash
$ ./ph 2
100000 puts, 1.885 seconds, 53044 puts/second
1: 16579 keys missing
0: 16579 keys missing
200000 gets, 4.322 seconds, 46274 gets/second
```

这个`ph 2`输出的第一行表明，当两个线程同时向哈希表添加条目时，它们达到每秒53044次插入的总速率。这大约是运行`ph 1`的单线程速度的两倍。这是一个优秀的“并行加速”，大约达到了人们希望的2倍（即两倍数量的核心每单位时间产出两倍的工作）。

然而，声明`16579 keys missing`的两行表示散列表中本应存在的大量键不存在。也就是说，puts应该将这些键添加到哈希表中，但出现了一些问题。请看一下***notxv6/ph.c***，特别是`put()`和`insert()`。

> [!TIP|label:YOUR JOB]
> 为什么两个线程都丢失了键，而不是一个线程？确定可能导致键丢失的具有2个线程的事件序列。在***answers-thread.txt***中提交您的序列和简短解释。

> [!TIP]
> 为了避免这种事件序列，请在***notxv6/ph.c***中的`put`和`get`中插入`lock`和`unlock`语句，以便在两个线程中丢失的键数始终为0。相关的pthread调用包括：
>
> * `pthread_mutex_t lock;            // declare a lock`
> * `pthread_mutex_init(&lock, NULL); // initialize the lock`
> * `pthread_mutex_lock(&lock);       // acquire lock`
> * `pthread_mutex_unlock(&lock);     // release lock`
>
> 当`make grade`说您的代码通过`ph_safe`测试时，您就完成了，该测试需要两个线程的键缺失数为0。在此时，`ph_fast`测试失败是正常的。

不要忘记调用`pthread_mutex_init()`。首先用1个线程测试代码，然后用2个线程测试代码。您主要需要测试：程序运行是否正确呢（即，您是否消除了丢失的键？）？与单线程版本相比，双线程版本是否实现了并行加速（即单位时间内的工作量更多）？

在某些情况下，并发`put()`在哈希表中读取或写入的内存中没有重叠，因此不需要锁来相互保护。您能否更改***ph.c***以利用这种情况为某些`put()`获得并行加速？提示：每个散列桶加一个锁怎么样？

> [!TIP|label:YOUR JOB]
> 修改代码，使某些`put`操作在保持正确性的同时并行运行。当`make grade`说你的代码通过了`ph_safe`和`ph_fast`测试时，你就完成了。`ph_fast`测试要求两个线程每秒产生的`put`数至少是一个线程的1.25倍。

---

来看一下程序的运行过程：设定了五个散列桶，根据键除以5的余数决定插入到哪一个散列桶中，插入方法是头插法，下面是图示

不支持在 Docs 外粘贴 block

这个实验比较简单，首先是问为什么为造成数据丢失：

> 假设现在有两个线程T1和T2，两个线程都走到put函数，且假设两个线程中key%NBUCKET相等，即要插入同一个散列桶中。两个线程同时调用insert(key, value, &table[i], table[i])，insert是通过头插法实现的。如果先insert的线程还未返回另一个线程就开始insert，那么前面的数据会被覆盖

因此只需要对插入操作上锁即可

(1). 为每个散列桶定义一个锁，将五个锁放在一个数组中，并进行初始化

```c
pthread_mutex_t lock[NBUCKET] = { PTHREAD_MUTEX_INITIALIZER }; // 每个散列桶一把锁
```

(2). 在`put`函数中对`insert`上锁

```c
if(e){
    // update the existing key.
    e->value = value;
} else {
    pthread_mutex_lock(&lock[i]);
    // the new is new.
    insert(key, value, &table[i], table[i]);
    pthread_mutex_unlock(&lock[i]);
}
```

https://github.com/doongz/xv6-labs-2020/commit/03b95a1b7a24e7bf373ff478d45e7514ef4b8232

# Barrier(moderate)

在本作业中，您将实现一个[屏障](http://en.wikipedia.org/wiki/Barrier_(computer_science))（Barrier）：应用程序中的一个点，所有参与的线程在此点上必须等待，直到所有其他参与线程也达到该点。您将使用pthread条件变量，这是一种序列协调技术，类似于xv6的`sleep`和`wakeup`。

您应该在真正的计算机（不是xv6，不是qemu）上完成此任务。

文件***notxv6/barrier.c***包含一个残缺的屏障实现。

```bash
$ make barrier
$ ./barrier 2
barrier: notxv6/barrier.c:42: thread: Assertion `i == t' failed.
```

2指定在屏障上同步的线程数（***barrier.c***中的`nthread`）。每个线程执行一个循环。在每次循环迭代中，线程都会调用`barrier()`，然后以随机微秒数休眠。如果一个线程在另一个线程到达屏障之前离开屏障将触发断言（assert）。期望的行为是每个线程在`barrier()`中阻塞，直到`nthreads`的所有线程都调用了`barrier()`。

> [!TIP|label:YOUR JOB]
> 您的目标是实现期望的屏障行为。除了在`ph`作业中看到的lock原语外，还需要以下新的pthread原语；详情请看[这里](https://pubs.opengroup.org/onlinepubs/007908799/xsh/pthread_cond_wait.html)和[这里](https://pubs.opengroup.org/onlinepubs/007908799/xsh/pthread_cond_broadcast.html)。
>
> * `// 在cond上进入睡眠，释放锁mutex，在醒来时重新获取`
> * `pthread_cond_wait(&cond, &mutex);`
> * `// 唤醒睡在cond的所有线程`
> * `pthread_cond_broadcast(&cond);`

确保您的方案通过`make grade`的`barrier`测试。

`pthread_cond_wait`在调用时释放`mutex`，并在返回前重新获取`mutex`。

我们已经为您提供了`barrier_init()`。您的工作是实现`barrier()`，这样panic就不会发生。我们为您定义了`struct barrier`；它的字段供您使用。

**有两个问题使您的任务变得复杂：**

- 你必须处理一系列的`barrier`调用，我们称每一连串的调用为一轮（round）。`bstate.round`记录当前轮数。每次当所有线程都到达屏障时，都应增加`bstate.round`。
- 您必须处理这样的情况：一个线程在其他线程退出`barrier`之前进入了下一轮循环。特别是，您在前后两轮中重复使用`bstate.nthread`变量。确保在前一轮仍在使用`bstate.nthread`时，离开`barrier`并循环运行的线程不会增加`bstate.nthread`。

使用一个、两个和两个以上的线程测试代码。

---

额。。。这个也比较简单，只要保证下一个round的操作不会影响到上一个还未结束的round中的数据就可

```c
static void 
barrier()
{
  // 申请持有锁
  pthread_mutex_lock(&bstate.barrier_mutex);

  bstate.nthread++;
  if(bstate.nthread == nthread) {
    // 所有线程已到达
    bstate.round++;
    bstate.nthread = 0;
    pthread_cond_broadcast(&bstate.barrier_cond);
  } else {
    // 等待其他线程
    // 调用pthread_cond_wait时，mutex必须已经持有
    pthread_cond_wait(&bstate.barrier_cond, &bstate.barrier_mutex);
  }
  // 释放锁
  pthread_mutex_unlock(&bstate.barrier_mutex);
}
```

