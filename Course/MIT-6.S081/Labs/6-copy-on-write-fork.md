# Lab6: Copy-on-Write Fork for xv6

虚拟内存提供了一定程度的间接寻址：内核可以通过将PTE标记为无效或只读来拦截内存引用，从而导致页面错误，还可以通过修改PTE来更改地址的含义。在计算机系统中有一种说法，任何系统问题都可以用某种程度的抽象方法来解决。Lazy allocation实验中提供了一个例子。这个实验探索了另一个例子：写时复制分支（copy-on write fork）。

在开始本实验前，将仓库切换到cow分支

```bash
$ git fetch
$ git checkout cow
$ make clean
```

## 问题

xv6中的`fork()`系统调用将父进程的所有用户空间内存复制到子进程中。如果父进程较大，则复制可能需要很长时间。更糟糕的是，这项工作经常造成大量浪费；例如，子进程中的`fork()`后跟`exec()`将导致子进程丢弃复制的内存，而其中的大部分可能都从未使用过。另一方面，如果父子进程都使用一个页面，并且其中一个或两个对该页面有写操作，则确实需要复制。

## 解决方案

copy-on-write (COW) fork()的目标是推迟到子进程实际需要物理内存拷贝时再进行分配和复制物理内存页面。

COW fork()只为子进程创建一个页表，用户内存的PTE指向父进程的物理页。COW fork()将父进程和子进程中的所有用户PTE标记为不可写。当任一进程试图写入其中一个COW页时，CPU将强制产生页面错误。内核页面错误处理程序检测到这种情况将为出错进程分配一页物理内存，将原始页复制到新页中，并修改出错进程中的相关PTE指向新的页面，将PTE标记为可写。当页面错误处理程序返回时，用户进程将能够写入其页面副本。

COW fork()将使得释放用户内存的物理页面变得更加棘手。给定的物理页可能会被多个进程的页表引用，并且只有在最后一个引用消失时才应该被释放。



# Implement copy-on write (hard)

> [!TIP|label:YOUR JOB]
> 您的任务是在xv6内核中实现copy-on-write fork。如果修改后的内核同时成功执行`cowtest`和`usertests`程序就完成了。

为了帮助测试你的实现方案，我们提供了一个名为`cowtest`的xv6程序（源代码位于***user/cowtest.c***）。`cowtest`运行各种测试，但在未修改的xv6上，即使是第一个测试也会失败。因此，最初您将看到：

```bash
$ cowtest
simple: fork() failed
$ 
```

“simple”测试分配超过一半的可用物理内存，然后执行一系列的`fork()`。`fork`失败的原因是没有足够的可用物理内存来为子进程提供父进程内存的完整副本。

完成本实验后，内核应该通过`cowtest`和`usertests`中的所有测试。即：

```bash
$ cowtest
simple: ok
simple: ok
three: zombie!
ok
three: zombie!
ok
three: zombie!
ok
file: ok
ALL COW TESTS PASSED
$ usertests
...
ALL TESTS PASSED
$
```

**这是一个合理的攻克计划：**

1. 修改`uvmcopy()`将父进程的物理页映射到子进程，而不是分配新页。在子进程和父进程的PTE中清除`PTE_W`标志。
2. 修改`usertrap()`以识别页面错误。当COW页面出现页面错误时，使用`kalloc()`分配一个新页面，并将旧页面复制到新页面，然后将新页面添加到PTE中并设置`PTE_W`。
3. 确保每个物理页在最后一个PTE对它的引用撤销时被释放——而不是在此之前。这样做的一个好方法是为每个物理页保留引用该页面的用户页表数的“引用计数”。当`kalloc()`分配页时，将页的引用计数设置为1。当`fork`导致子进程共享页面时，增加页的引用计数；每当任何进程从其页表中删除页面时，减少页的引用计数。`kfree()`只应在引用计数为零时将页面放回空闲列表。可以将这些计数保存在一个固定大小的整型数组中。你必须制定一个如何索引数组以及如何选择数组大小的方案。例如，您可以用页的物理地址除以4096对数组进行索引，并为数组提供等同于***kalloc.c***中`kinit()`在空闲列表中放置的所有页面的最高物理地址的元素数。
4. 修改`copyout()`在遇到COW页面时使用与页面错误相同的方案。

**提示：**

- lazy page allocation实验可能已经让您熟悉了许多与copy-on-write相关的xv6内核代码。但是，您不应该将这个实验室建立在您的lazy allocation解决方案的基础上；相反，请按照上面的说明从一个新的xv6开始。
- 有一种可能很有用的方法来记录每个PTE是否是COW映射。您可以使用RISC-V PTE中的RSW（reserved for software，即为软件保留的）位来实现此目的。
- `usertests`检查`cowtest`不测试的场景，所以别忘两个测试都需要完全通过。
- ***kernel/riscv.h***的末尾有一些有用的宏和页表标志位的定义。
- 如果出现COW页面错误并且没有可用内存，则应终止进程。

---

跟着提示一步一步来

**(1).** 在***kernel/riscv.h***中选取PTE中的保留位定义标记一个页面是否为COW Fork页面的标志位

```c
// 记录应用了COW策略后fork的页面
#define PTE_F (1L << 8)
```

**(2).** 在***kalloc.c***中进行如下修改

* 定义引用计数的全局变量`ref`，其中包含了一个自旋锁和一个引用计数数组，由于`ref`是全局变量，会被自动初始化为全0。

  这里使用自旋锁是考虑到这种情况：进程P1和P2共用内存M，M引用计数为2，此时CPU1要执行`fork`产生P1的子进程，CPU2要终止P2，那么假设两个CPU同时读取引用计数为2，执行完成后CPU1中保存的引用计数为3，CPU2保存的计数为1，那么后赋值的语句会覆盖掉先赋值的语句，从而产生错误

```c
struct ref_stru {
  struct spinlock lock;
  int cnt[PHYSTOP / PGSIZE];  // 引用计数
} ref;
```

- 在`kinit`中初始化`ref`的自旋锁

```c
void
kinit()
{
  initlock(&kmem.lock, "kmem");
  initlock(&ref.lock, "ref");
  freerange(end, (void*)PHYSTOP);
}
```

* 修改`kalloc`和`kfree`函数，在`kalloc`中初始化内存引用计数为1，在`kfree`函数中对内存引用计数减1，如果引用计数为0时才真正删除

```c
void
kfree(void *pa)
{ // 释放物理地址
  struct run *r;

  if(((uint64)pa % PGSIZE) != 0 || (char*)pa < end || (uint64)pa >= PHYSTOP)
    panic("kfree");

  // 引用计数减1，为0才将内存真正释放
  acquire(&ref.lock);
  int idx = (uint64)pa / PGSIZE;
  ref.cnt[idx] -= 1;
  
  if (ref.cnt[idx] == 0) { 
    release(&ref.lock); // 一定要锁到取值检查后，否则这个值可能会被其他进程改掉
    
    // Fill with junk to catch dangling refs.
    memset(pa, 1, PGSIZE);

    r = (struct run*)pa;

    acquire(&kmem.lock);
    r->next = kmem.freelist;
    kmem.freelist = r;
    release(&kmem.lock);
  } else {
    release(&ref.lock);
  }
}

void *
kalloc(void)
{ // 申请物理地址
  struct run *r;

  acquire(&kmem.lock);
  r = kmem.freelist;
  if(r) {
    kmem.freelist = r->next;
    acquire(&ref.lock);
    ref.cnt[(uint64)r / PGSIZE] = 1; // 将引用计数初始化为1
    release(&ref.lock);
  }
  release(&kmem.lock);

  if(r)
    memset((char*)r, 5, PGSIZE); // fill with junk
  return (void*)r;
}
```

- 添加如下四个函数，详细说明已在注释中，这些函数中用到了`walk`，记得在***defs.h***中添加声明，最后也需要将这些函数的声明添加到***defs.h***，在cowalloc中，读取内存引用计数，如果为1，说明只有当前进程引用了该物理内存（其他进程此前已经被分配到了其他物理页面），就只需要改变PTE使能`PTE_W`；否则就分配物理页面，并将原来的内存引用计数减1。该函数需要返回物理地址，这将在`copyout`中使用到。

```c
/**
 * @brief kaddrefcnt 增加内存的引用计数
 * @param pa 指定的内存地址
 * @return 0:成功 -1:失败
 */
int kaddrefcnt(void* pa) {
  if(((uint64)pa % PGSIZE) != 0 || (char*)pa < end || (uint64)pa >= PHYSTOP)
    return -1;
  acquire(&ref.lock);
  ++ref.cnt[(uint64)pa / PGSIZE];
  release(&ref.lock);
  return 0;
}

/**
 * @brief cowpage 判断一个页面是否为COW页面
 * @param pagetable 指定查询的页表
 * @param va 虚拟地址
 * @return 1:是 0:不是 -1:报错
 */
int cowpage(pagetable_t pagetable, uint64 va) {
  if(va >= MAXVA)
    return -1;
  pte_t* pte = walk(pagetable, va, 0);
  if(pte == 0)
    return -1;
  if((*pte & PTE_V) == 0)
    return 0;
  return (*pte & PTE_F ? 1 : 0);
}

/**
 * @brief cowalloc copy-on-write分配器
 * @param pagetable 指定页表
 * @param va 指定的虚拟地址,必须页面对齐
 * @return 分配后va对应的物理地址，如果返回0则分配失败
 */
void* cowalloc(pagetable_t pagetable, uint64 va) {
  if(va % PGSIZE != 0)
    return 0;

  uint64 pa = walkaddr(pagetable, va);  // 获取对应的物理地址
  if(pa == 0)
    return 0;

  pte_t* pte = walk(pagetable, va, 0);  // 获取对应的PTE

  if(krefcnt((char*)pa) == 1) {
    // 只剩一个进程对此物理地址存在引用
    // 则直接修改对应的PTE即可
    *pte |= PTE_W;  // 标记为可写
    *pte &= ~PTE_F; // 移去COW标记
    return (void*)pa;
  } else {
    // 多个进程对物理内存存在引用
    // 需要分配新的页面，并拷贝旧页面的内容，真正去申请物理地址
    char* mem = kalloc();
    if(mem == 0)
      return 0;

    // 复制旧页面内容到新页
    memmove(mem, (char*)pa, PGSIZE);

    // 清除PTE_V，否则在mappagges中会判定为remap
    *pte &= ~PTE_V;

    // 为新页面添加映射
    if(mappages(pagetable, va, PGSIZE, (uint64)mem, (PTE_FLAGS(*pte) | PTE_W) & ~PTE_F) != 0) {
      kfree(mem);
      *pte |= PTE_V;
      return 0;
    }

    // 将原来的物理内存引用计数减1
    kfree((char*)PGROUNDDOWN(pa));
    return mem;
  }
}

/**
 * @brief krefcnt 获取内存的引用计数
 * @param pa 指定的内存地址
 * @return 引用计数
 */
int krefcnt(void* pa) {
  return ref.cnt[(uint64)pa / PGSIZE];
}
```

- 修改`freerange`

```c
void
freerange(void *pa_start, void *pa_end)
{
  char *p;
  p = (char*)PGROUNDUP((uint64)pa_start);
  for (; p + PGSIZE <= (char*)pa_end; p += PGSIZE) {
    // 在kfree中将会对cnt[]减1，这里要先设为1，否则就会减成负数
    // 同时起到彻底释放的作用
    ref.cnt[(uint64)p / PGSIZE] = 1;
    kfree(p);
  }
}
```

**(3).** 修改`uvmcopy`，不为子进程分配内存，而是使父子进程共享内存，但禁用`PTE_W`，同时标记`PTE_F`，记得调用`kaddrefcnt`增加引用计数

```c
int
uvmcopy(pagetable_t old, pagetable_t new, uint64 sz)
{
  pte_t *pte;
  uint64 pa, i;
  uint flags;
  // char *mem;

  for(i = 0; i < sz; i += PGSIZE){
    if((pte = walk(old, i, 0)) == 0)
      panic("uvmcopy: pte should exist");
    if((*pte & PTE_V) == 0)
      panic("uvmcopy: page not present");
    // 此时 pte 为父进程中pagetable的有效pte
    pa = PTE2PA(*pte);
    flags = PTE_FLAGS(*pte);

    // 不要真的去申请物理内存
    // if((mem = kalloc()) == 0)
    //   goto err;
    // memmove(mem, (char*)pa, PGSIZE);

    // 仅对可写页面设置COW标记
    if(flags & PTE_W) {
      // 禁用写并设置COW Fork标记
      flags = (flags | PTE_F) & ~PTE_W;
      *pte = PA2PTE(pa) | flags;
    }

    // 直接将新的pagetable映射到物理地址上
    if(mappages(new, i, PGSIZE, pa, flags) != 0){
      // kfree(mem); // 如果映射错误，也不要真的释放内存
      uvmunmap(new, 0, i / PGSIZE, 1);
    }
    // 增加内存的引用计数
    kaddrefcnt((char*)pa);
  }
  return 0;
}
```

**(4).** 修改`usertrap`，处理页面错误

```c
uint64 cause = r_scause();
if(cause == 8) {
  ...
} else if((which_dev = devintr()) != 0){
  // ok
} else if(cause == 13 || cause == 15) {
    // 这个地方会在子进程中触发，p->pagetable 为子进程中映射在老物理地址上的pagetable
    // 使用老的pagetable 会报page fault
    // 进行一些判断后进行copy on write申请内存
    uint64 fault_va = r_stval();  // 获取出错的虚拟地址
    if (fault_va < p->sz && cowpage(p->pagetable, fault_va) == 1) {
      // 如果这个错误的虚地址是有效的，且这个虚地址对应的pte是COW页面
      // 进行copy on write申请内存
      if (cowalloc(p->pagetable, PGROUNDDOWN(fault_va)) == 0) {
        p->killed = 1;
      }
    } else {
      p->killed = 1;
    }
} else {
  ...
}
```

**(5).** 在`copyout`中处理相同的情况，如果是COW页面，需要更换`pa0`指向的物理地址

```c
while(len > 0){
  va0 = PGROUNDDOWN(dstva);
  pa0 = walkaddr(pagetable, va0);

  // 处理COW页面的情况
  if(cowpage(pagetable, va0) == 0) {
    // 更换目标物理地址
    pa0 = (uint64)cowalloc(pagetable, va0);
  }

  if(pa0 == 0)
    return -1;

  ...
}
```

https://github.com/dowalle/xv6-labs-2020/commit/d9c8cc8fb508c1ebdfa5eceb702246f219439e15

# 可选的挑战练习

- 修改xv6以同时支持lazy allocation和COW。
- 测量您的COW实现减少了多少xv6拷贝的字节数以及分配的物理页数。寻找并利用机会进一步减少这些数字。

