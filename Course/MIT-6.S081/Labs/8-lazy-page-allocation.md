# Lab5: xv6 lazy page allocation

操作系统可以使用页表硬件的技巧之一是延迟分配用户空间堆内存（lazy allocation of user-space heap memory）。Xv6应用程序使用`sbrk()`系统调用向内核请求堆内存。在我们给出的内核中，`sbrk()`分配物理内存并将其映射到进程的虚拟地址空间。内核为一个大请求分配和映射内存可能需要很长时间。例如，考虑由262144个4096字节的页组成的千兆字节；即使单独一个页面的分配开销很低，但合起来如此大的分配数量将不可忽视。此外，有些程序申请分配的内存比实际使用的要多（例如，实现稀疏数组），或者为了以后的不时之需而分配内存。为了让`sbrk()`在这些情况下更快地完成，复杂的内核会延迟分配用户内存。也就是说，`sbrk()`不分配物理内存，只是记住分配了哪些用户地址，并在用户页表中将这些地址标记为无效。当进程第一次尝试使用延迟分配中给定的页面时，CPU生成一个页面错误（page fault），内核通过分配物理内存、置零并添加映射来处理该错误。您将在这个实验室中向xv6添加这个延迟分配特性。

> [!WARNING|label:Attention]
> 在开始编码之前，请阅读xv6手册的第4章（特别是4.6），以及可能要修改的相关文件：
> - ***kernel/trap.c***
> - ***kernel/vm.c***
> - ***kernel/sysproc.c***

要启动实验，请切换到`lazy`分支：

```bash
$ git fetch
$ git checkout lazy
$ make clean
```



# Eliminate allocation from sbrk() (easy)

> [!TIP|label:YOUR JOB]
> 你的首项任务是删除`sbrk(n)`系统调用中的页面分配代码（位于***sysproc.c***中的函数`sys_sbrk()`）。`sbrk(n)`系统调用将进程的内存大小增加n个字节，然后返回新分配区域的开始部分（即旧的大小）。新的`sbrk(n)`应该只将进程的大小（`myproc()->sz`）增加n，然后返回旧的大小。它不应该分配内存——因此您应该删除对`growproc()`的调用（但是您仍然需要增加进程的大小！）。

试着猜猜这个修改的结果是什么：将会破坏什么？

进行此修改，启动xv6，并在shell中键入`echo hi`。你应该看到这样的输出：

```bash
init: starting sh
$ echo hi
usertrap(): unexpected scause 0x000000000000000f pid=3
            sepc=0x0000000000001258 stval=0x0000000000004008
va=0x0000000000004000 pte=0x0000000000000000
panic: uvmunmap: not mapped
```

“`usertrap(): …`”这条消息来自***trap.c***中的用户陷阱处理程序；它捕获了一个不知道如何处理的异常。请确保您了解发生此页面错误的原因。“`stval=0x0..04008`”表示导致页面错误的虚拟地址是`0x4008`。

---

这个实验很简单，就仅仅改动`sys_sbrk()`函数即可，将实际分配内存的函数删除，而仅仅改变进程的`sz`属性

```c
uint64
sys_sbrk(void)
{
  int addr;
  int n;

  if(argint(0, &n) < 0)
    return -1;
  addr = myproc()->sz;
  // if(growproc(n) < 0)
  //   return -1;
  myproc()->sz + n;
  return addr;
}
```





# Lazy allocation (moderate)

> [!TIP|label:YOUR JOB]
> 修改***trap.c***中的代码以响应来自用户空间的页面错误，方法是新分配一个物理页面并映射到发生错误的地址，然后返回到用户空间，让进程继续执行。您应该在生成“`usertrap(): …`”消息的`printf`调用之前添加代码。你可以修改任何其他xv6内核代码，以使`echo hi`正常工作。

**提示：**

- 你可以在`usertrap()`中查看`r_scause()`的返回值是否为13或15来判断该错误是否为页面错误
- `stval`寄存器中保存了造成页面错误的虚拟地址，你可以通过`r_stval()`读取
- 参考***vm.c***中的`uvmalloc()`中的代码，那是一个`sbrk()`通过`growproc()`调用的函数。你将需要对`kalloc()`和`mappages()`进行调用
- 使用`PGROUNDDOWN(va)`将出错的虚拟地址向下舍入到页面边界
- 当前`uvmunmap()`会导致系统`panic`崩溃；请修改程序保证正常运行
- 如果内核崩溃，请在***kernel/kernel.asm***中查看`sepc`
- 使用pgtbl lab的`vmprint`函数打印页表的内容
- 如果您看到错误“incomplete type proc”，请include“spinlock.h”然后是“proc.h”。

如果一切正常，你的lazy allocation应该使`echo hi`正常运行。您应该至少有一个页面错误（因为延迟分配），也许有两个。

---

根据提示来做就好，另外6.S081对应的视频课程中对这部分代码做出了很大一部分的解答。

**(1)**. 修改`usertrap()`(***kernel/trap.c***)函数，使用`r_scause()`判断是否为页面错误，在页面错误处理的过程中，先判断发生错误的虚拟地址（`r_stval()`读取）是否位于栈空间之上，进程大小（虚拟地址从0开始，进程大小表征了进程的最高虚拟地址）之下，然后分配物理内存并添加映射

```c
  uint64 cause = r_scause();
  if(cause == 8) {
    ...
  } else if((which_dev = devintr()) != 0) {
    // ok
  } else if(cause == 13 || cause == 15) {
    // 处理页面错误
    uint64 fault_va = r_stval();  // 产生页面错误的虚拟地址
    char* pa;                     // 分配的物理地址
    if(PGROUNDUP(p->trapframe->sp) - 1 < fault_va && fault_va < p->sz &&
      (pa = kalloc()) != 0) {
        memset(pa, 0, PGSIZE);
        if(mappages(p->pagetable, PGROUNDDOWN(fault_va), PGSIZE, (uint64)pa, PTE_R | PTE_W | PTE_X | PTE_U) != 0) {
          kfree(pa);
          p->killed = 1;
        }
    } else {
      // printf("usertrap(): out of memory!\n");
      p->killed = 1;
    }
  } else {
    ...
  }
```

**(2)**. 修改`uvmunmap()`(***kernel/vm.c***)，之所以修改这部分代码是因为lazy allocation中首先并未实际分配内存，所以当解除映射关系的时候对于这部分内存要略过，而不是使系统崩溃，这部分在课程视频中已经解答。

```c
void
uvmunmap(pagetable_t pagetable, uint64 va, uint64 npages, int do_free)
{
  ...

  for(a = va; a < va + npages*PGSIZE; a += PGSIZE){
    if((pte = walk(pagetable, a, 0)) == 0)
      panic("uvmunmap: walk");
    if((*pte & PTE_V) == 0)
      continue;

    ...
  }
}
```



# Lazytests and Usertests (moderate)

我们为您提供了`lazytests`，这是一个xv6用户程序，它测试一些可能会给您的惰性内存分配器带来压力的特定情况。修改内核代码，使所有`lazytests`和`usertests`都通过。

- 处理`sbrk()`参数为负的情况。
- 如果某个进程在高于`sbrk()`分配的任何虚拟内存地址上出现页错误，则终止该进程。
- 在`fork()`中正确处理父到子内存拷贝。
- 处理这种情形：进程从`sbrk()`向系统调用（如`read`或`write`）传递有效地址，但尚未分配该地址的内存。
- 正确处理内存不足：如果在页面错误处理程序中执行`kalloc()`失败，则终止当前进程。
- 处理用户栈下面的无效页面上发生的错误。

如果内核通过`lazytests`和`usertests`，那么您的解决方案是可以接受的：

```bash
$ lazytests
lazytests starting
running test lazy alloc
test lazy alloc: OK
running test lazy unmap...
usertrap(): ...
test lazy unmap: OK
running test out of memory
usertrap(): ...
test out of memory: OK
ALL TESTS PASSED
$ usertests
...
ALL TESTS PASSED
$
```

---

**(1)**. 处理`sbrk()`参数为负数的情况，参考之前`sbrk()`调用的`growproc()`程序，如果为负数，就调用`uvmdealloc()`函数，但需要限制缩减后的内存空间不能小于0

```c
uint64
sys_sbrk(void)
{
  int addr;
  int n;

  if(argint(0, &n) < 0)
    return -1;

  struct proc* p = myproc();
  addr = p->sz;
  uint64 sz = p->sz;

  if(n > 0) {
    // lazy allocation
    p->sz += n;
  } else if(sz + n > 0) {
    sz = uvmdealloc(p->pagetable, sz, sz + n);
    p->sz = sz;
  } else {
    return -1;
  }
  return addr;
}
```

**(2)**. 正确处理`fork`的内存拷贝：`fork`调用了`uvmcopy`进行内存拷贝，所以修改`uvmcopy`如下

```c
int
uvmcopy(pagetable_t old, pagetable_t new, uint64 sz)
{
  ...
  for(i = 0; i < sz; i += PGSIZE){
    if((pte = walk(old, i, 0)) == 0)
      continue;
    if((*pte & PTE_V) == 0)
      continue;
    ...
  }
  ...
}
```

**(3)**. 还需要继续修改`uvmunmap`，否则会运行出错，关于为什么要使用两个`continue`，请看本文最下面

```c
void
uvmunmap(pagetable_t pagetable, uint64 va, uint64 npages, int do_free)
{
  ...

  for(a = va; a < va + npages*PGSIZE; a += PGSIZE){
    if((pte = walk(pagetable, a, 0)) == 0)
      continue;
    if((*pte & PTE_V) == 0)
      continue;

    ...
  }
}
```

**(4)**. 处理通过sbrk申请内存后还未实际分配就传给系统调用使用的情况，系统调用的处理会陷入内核，scause寄存器存储的值是8，如果此时传入的地址还未实际分配，就不能走到上文usertrap中判断scause是13或15后进行内存分配的代码，syscall执行就会失败

- 系统调用流程：

  - 陷入内核**==>**`usertrap`中`r_scause()==8`的分支**==>**`syscall()`**==>**回到用户空间

- 页面错误流程：

  - 陷入内核**==>**`usertrap`中`r_scause()==13||r_scause()==15`的分支**==>**分配内存**==>**回到用户空间

因此就需要找到在何时系统调用会使用这些地址，将地址传入系统调用后，会通过`argaddr`函数(***kernel/syscall.c***)从寄存器中读取，因此在这里添加物理内存分配的代码

可以运行 usertests 测试看看，就明白为啥这么改

```
test sbrkarg: sbrkarg: write sbrk failed
FAILED
```



```c
int
argaddr(int n, uint64 *ip)
{
  *ip = argraw(n);
  struct proc* p = myproc();

  // 处理向系统调用传入lazy allocation地址的情况
  if(walkaddr(p->pagetable, *ip) == 0) {
    if(PGROUNDUP(p->trapframe->sp) - 1 < *ip && *ip < p->sz) {
      char* pa = kalloc();
      if(pa == 0)
        return -1;
      memset(pa, 0, PGSIZE);

      if(mappages(p->pagetable, PGROUNDDOWN(*ip), PGSIZE, (uint64)pa, PTE_R | PTE_W | PTE_X | PTE_U) != 0) {
        kfree(pa);
        return -1;
      }
    } else {
      return -1;
    }
  }

  return 0;
}
```

## 为什么使用两个continue

这里需要解释一下为什么在两个判断中使用了`continue`语句，在课程视频中仅仅添加了第二个`continue`，利用`vmprint`打印出来初始时刻用户进程的页表如下

```
page table 0x0000000087f55000
..0: pte 0x0000000021fd3c01 pa 0x0000000087f4f000
.. ..0: pte 0x0000000021fd4001 pa 0x0000000087f50000
.. .. ..0: pte 0x0000000021fd445f pa 0x0000000087f51000
.. .. ..1: pte 0x0000000021fd4cdf pa 0x0000000087f53000
.. .. ..2: pte 0x0000000021fd900f pa 0x0000000087f64000
.. .. ..3: pte 0x0000000021fd5cdf pa 0x0000000087f57000
..255: pte 0x0000000021fd5001 pa 0x0000000087f54000
.. ..511: pte 0x0000000021fd4801 pa 0x0000000087f52000
.. .. ..510: pte 0x0000000021fd58c7 pa 0x0000000087f56000
.. .. ..511: pte 0x0000000020001c4b pa 0x0000000080007000
```

除去高地址的trapframe和trampoline页面，进程共计映射了4个有效页面，即添加了映射关系的虚拟地址范围是`0x0000~0x3fff`，假如使用`sbrk`又申请了一个页面，由于lazy allocation，页表暂时不会改变，而不经过读写操作后直接释放进程，进程将会调用`uvmunmap`函数，此时将会发生什么呢？

`uvmunmap`首先使用`walk`找到虚拟地址对应的PTE地址，虚拟地址的最后12位表征了偏移量，前面每9位索引一级页表，将`0x4000`的虚拟地址写为二进制（省略前面的无效位）：

```
{000 0000 00}[00 0000 000](0 0000 0100) 0000 0000 0000
```

- `{}`：页目录表索引(level==2)，为0
- `[]`：二级页表索引(level==1)，为0
- `()`：三级页表索引(level==0)，为4

我们来看一下`walk`函数，`walk`返回指定虚拟地址的PTE，但我认为这个程序存在一定的不足。walk函数的代码如下所示

```c
pte_t *
walk(pagetable_t pagetable, uint64 va, int alloc)
{
  if(va >= MAXVA)
    panic("walk");

  for(int level = 2; level > 0; level--) {
    pte_t *pte = &pagetable[PX(level, va)];
    if(*pte & PTE_V) {
      pagetable = (pagetable_t)PTE2PA(*pte);
    } else {
      if(!alloc || (pagetable = (pde_t*)kalloc()) == 0)
        return 0;
      memset(pagetable, 0, PGSIZE);
      *pte = PA2PTE(pagetable) | PTE_V;
    }
  }
  return &pagetable[PX(0, va)];
}
```

这段代码中`for`循环执行`level==2`和`level==1`的情况，而对照刚才打印的页表，`level==2`时索引为0的项是存在的，`level==1`时索引为0的项也是存在的，最后执行`return`语句，然而level==0时索引为4的项却是不存在的，此时`walk`不再检查`PTE_V`标志等信息，而是直接返回，因此即使虚拟地址对应的PTE实际不存在，`walk`函数的返回值也可能不为0！

那么返回的这个地址是什么呢？level为0时

有效索引为0~3，因此索引为4时返回的是最后一个有效PTE后面的一个地址。

因此我们不能仅靠PTE为0来判断虚拟地址无效，还需要再次检查返回的PTE中是否设置了`PTE_V`标志位。





# 可选的挑战练习

- 让延时分配协同上一个实验中简化版的`copyin`一起工作。