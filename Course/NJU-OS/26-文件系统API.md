# 文件系统 API

## Overview

复习

- 对 I/O 设备的抽象
    - 物理层 1-bit 的存储
    - 设备层 I/O 设备 (寄存器)
    - 驱动层 (可读/写/控制的对象)
    - 块设备层 (block read/write)

------

本次课回答的问题

- **Q**: 如何使应用程序能共享存储设备？

------

本次课主要内容

- 文件系统需求分析
- 文件系统 API

## 一、为什么需要文件系统？

### 1、设备在应用程序之间的共享

终端

- 多个进程并行打印，如何保证不混乱？([printf-race.c](http://jyywiki.cn/pages/OS/2022/demos/printf-race.c))
    - Unicode 字符和 Escape Code 被隔断可不是闹着玩的
- 多个进程并行读，就会发生争抢
    - 谁抢到谁赢 (还算可以接受)
    - 后台进程会在读终端时收到 SIGTTIN (RTFM)

```c
#include <stdio.h>
#include "thread.h"

void use_printf(const char *s) {
  printf("%s", s);
}

void use_putchar(const char *s) {
  for (; *s; s++) {
    putchar(*s);
  }
}

void (*print)(const char *) = use_printf;

void Tworker() {
  char buf[128];
  int c = gettid() % 4 + 1;
  sprintf(buf, "\033[3%dm%d\033[0m", c, c);
  while (1) {
    print(buf);
  }
}

int main(int argc, char *argv[]) {
  if (argc > 1) {
    print = use_putchar;
  }

  setbuf(stdout, NULL);
  for (int i = 0; i < 4; i++) {
    create(Tworker);
  }
}

```

------

GPU (CUDA)

- 每个 CUDA 应用程序都是一系列 CUDA API 的调用
    - cudaMemcpy, kernel call
- 全部由设备驱动负责调度 (和隔离)
    - Kernel 要等空闲 thread warp 才可以上，执行完后归还

---

磁盘需要支持数据的持久化

- 程序数据
    - 可执行文件和动态链接库
    - 应用数据 (高清图片、过场动画、3D 模型……)
- 用户数据
    - 文档、下载、截图、replay……
- 系统数据
    - Manpages
    - 系统配置

------

**字节序列并不是磁盘的好抽象**

- 让所有应用共享磁盘？一个程序 bug 操作系统就没了

### 2、文件系统：虚拟磁盘

文件系统：设计目标

1. 提供合理的 API 使多个应用程序能共享数据
2. 提供一定的隔离，使恶意/出错程序的伤害不能任意扩大

------

“存储设备 (字节序列) 的虚拟化”

- 磁盘 (I/O 设备) = 一个可以读/写的字节序列
- **虚拟磁盘**(文件) = 一个可以读/写的动态字节序列
    - 命名管理
        - 虚拟磁盘的名称、检索和遍历
    - 数据管理
        - `std::vector<char>` (随机读写/resize)

## 二、虚拟磁盘：命名管理

### 1、怎么找到想要的虚拟磁盘？

信息的局部性：将虚拟磁盘 (文件) 组织成层次结构

![img](./doc/nju-lib.jpg)

### 2、利用信息的局部性组织虚拟磁盘

目录树

- 逻辑相关的数据存放在相近的目录

```
.
└── 学习资料
    ├── .学习资料(隐藏)
    ├── 问题求解1
    ├── 问题求解2
    ├── 问题求解3
    ├── 问题求解4
    └── 操作系统
```

### 3、文件系统的 “根”

树总得有个根结点

- Windows: 每个设备(驱动器) 是一棵树
    - `C:\`“C 盘根目录”
        - `C:\Program Files\`, `C:\Windows`, `C:\Users`, ...
    - 优盘分配给新的盘符
        - 为什么没有 `A:\`, `B:\`?
        - 简单、粗暴、方便，但 `game.iso` 一度非常麻烦……

- UNIX/Linux
    - 只有一个根`/`
        - 第二个设备呢？
        - 优盘呢？？？

### 4、目录树的拼接

UNIX: 允许任意目录 “挂载 (mount)” 一个**设备**代表的目录树

- 非常灵活的设计
    - 可以把设备挂载到任何想要的位置
    - Linux 安装时的 “mount point”
        - `/`, `/home`, `/var` 可以是独立的磁盘设备

------

mount 系统调用

```c
int mount(const char *source, const char *target,
          const char *filesystemtype, unsigned long mountflags,
          const void *data);
```

- `mount /dev/sdb /mnt`(RTFM)
    - Linux mount 工具能自动检测文件系统 (busybox 不

### 5、真正的 Linux 启动流程

Linux-minimal 运行在 “initramfs” 模式

- Initial RAM file system
- 完整的文件系统
    - 可以包含设备驱动等任何文件 ([launcher.c](http://jyywiki.cn/pages/OS/2022/demos/launcher.c))
    - 但不具有 “持久化” 的能力

------

最小 “真正” Linux 的启动流程

```
export PATH=/bin
busybox mknod /dev/sda b 8 0
busybox mkdir -p /newroot
busybox mount -t ext2 /dev/sda /newroot
exec busybox switch_root /newroot/ /etc/init
```

通过 `pivot_root` (2) 实现根文件系统的切换