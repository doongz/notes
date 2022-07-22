# 系统调用和 UNIX Shell

## Overview

复习

- 状态机模型 (程序、多线程程序、操作系统)
- 操作系统是状态机的管理者

------

本次课回答的问题

- **Q**: 我们是操作系统的用户；但操作系统提供的 API 并不是 “我们” 作为人类用户能直接使用的。那 “我们” 到底怎么用操作系统？

------

本次课主要内容

- UNIX Shell 的设计和实现

## 一、Shell

### 1、半学期小结：我们都学了什么？

整个计算机系统世界的 “构建”

- 硬件 (NEMU)：从 CPU Reset 开始执行指令 (计算和 I/O)
- Firmware: 加载操作系统
- 操作系统：状态机的管理者
  - 初始化第一个进程 (状态机)
  - 执行系统调用

例子：[linux-minimal.zip](https://box.nju.edu.cn/f/3f67e092e1ba441187d9/?dl=1)

- 整个系统里只需要 “一个程序”
  - busybox/toybox/...
- 这个程序可以再执行各种应用程序
  - vim; dosbox; xeyes; ...

### 2、为用户封装操作系统 API

> 我们需要一个 “用户能直接操作” 的程序管理操作系统对象。

这就是 Shell (内核 Kernel 提供系统调用；Shell 提供用户接口)

- “与**人类直接交互**的第一个程序”
- 帮助人类创建/管理进程 (应用程序)、数据文件……

![img](http://jyywiki.cn/pages/OS/img/win11.jpg)

### 3、The UNIX Shell

“终端” 时代的伟大设计

- “Command-line interface” (CLI) 的巅峰

**Shell 是一门 “把用户指令翻译成系统调用” 的编程语言**

- man sh (推荐阅读！), bash, ...
- 原来我们一直在编程
  - 直到有了 Graphical Shell (GUI)
  - Windows, Gnome, Symbian, Android

## 二、复刻经典

### 1、脾气有点小古怪的 UNIX 世界

“Unix is user-friendly; it's just choosy about who its friends are.”

- 但如果把 shell 理解成编程语言，“不好用” 好像也没什么毛病了
  - ~~你见过哪个编程语言 “好用” 的？~~

![img](http://jyywiki.cn/pages/OS/img/xkcd-tar.png)

(UNIX 世界有很多历史遗留约定)

### 2、A Zero-dependency UNIX Shell (from xv6)

[sh-xv6.c](http://jyywiki.cn/pages/OS/2022/demos/sh-xv6.c)

- 零库函数依赖 (-ffreestanding 编译、ld 链接)
- 可以作为最小 Linux 的 init 程序
- 用到**文件描述符**：一个打开文件的 “指针”

```c
// Linux port of xv6-riscv shell (no libc)
// Compile with "-ffreestanding"!

#include <fcntl.h>
#include <stdarg.h>
#include <stddef.h>
#include <sys/syscall.h>

// Parsed command representation
enum { EXEC = 1, REDIR, PIPE, LIST, BACK };

#define MAXARGS 10
#define NULL ((void *)0)

struct cmd {
  int type;
};

struct execcmd {
  int type;
  char *argv[MAXARGS], *eargv[MAXARGS];
};

struct redircmd {
  int type, fd, mode;
  char *file, *efile;
  struct cmd* cmd;
};

struct pipecmd {
  int type;
  struct cmd *left, *right;
};

struct listcmd {
  int type;
  struct cmd *left, *right;
};

struct backcmd {
  int type;
  struct cmd* cmd;
};

struct cmd* parsecmd(char*);

// Minimum runtime library
long syscall(int num, ...) {
  va_list ap;
  va_start(ap, num);
  register long a0 asm ("rax") = num;
  register long a1 asm ("rdi") = va_arg(ap, long);
  register long a2 asm ("rsi") = va_arg(ap, long);
  register long a3 asm ("rdx") = va_arg(ap, long);
  register long a4 asm ("r10") = va_arg(ap, long);
  va_end(ap);
  asm volatile("syscall"
    : "+r"(a0) : "r"(a1), "r"(a2), "r"(a3), "r"(a4)
    : "memory", "rcx", "r8", "r9", "r11");
  return a0;
}

size_t strlen(const char *s) {
  size_t len = 0;
  for (; *s; s++) len++;
  return len;
}

char *strchr(const char *s, int c) {
  for (; *s; s++) {
    if (*s == c) return (char *)s;
  }
  return NULL;
}

void print(const char *s, ...) {
  va_list ap;
  va_start(ap, s);
  while (s) {
    syscall(SYS_write, 2, s, strlen(s));
    s = va_arg(ap, const char *);
  }
  va_end(ap);
}

#define assert(cond) \
  do { if (!(cond)) { \
    print("Panicked.\n", NULL); \
    syscall(SYS_exit, 1); } \
  } while (0)

static char mem[4096], *freem = mem;

void *zalloc(size_t sz) {
  assert(freem + sz < mem + sizeof(mem));
  void *ret = freem;
  freem += sz;
  return ret;
}

// Execute cmd.  Never returns.
void runcmd(struct cmd* cmd) {
  int p[2];
  struct backcmd* bcmd;
  struct execcmd* ecmd;
  struct listcmd* lcmd;
  struct pipecmd* pcmd;
  struct redircmd* rcmd;

  if (cmd == 0) syscall(SYS_exit, 1);

  switch (cmd->type) {
    case EXEC:
      ecmd = (struct execcmd*)cmd;
      if (ecmd->argv[0] == 0) syscall(SYS_exit, 1);
      syscall(SYS_execve, ecmd->argv[0], ecmd->argv, NULL);
      print("fail to exec ", ecmd->argv[0], "\n", NULL);
      break;

    case REDIR:
      rcmd = (struct redircmd*)cmd;
      syscall(SYS_close, rcmd->fd);
      if (syscall(SYS_open, rcmd->file, rcmd->mode, 0644) < 0) {
        print("fail to open ", rcmd->file, "\n", NULL);
        syscall(SYS_exit, 1);
      }
      runcmd(rcmd->cmd);
      break;

    case LIST:
      lcmd = (struct listcmd*)cmd;
      if (syscall(SYS_fork) == 0) runcmd(lcmd->left);
      syscall(SYS_wait4, -1, 0, 0, 0);
      runcmd(lcmd->right);
      break;

    case PIPE:
      pcmd = (struct pipecmd*)cmd;
      assert(syscall(SYS_pipe, p) >= 0);
      if (syscall(SYS_fork) == 0) {
        syscall(SYS_close, 1);
        syscall(SYS_dup, p[1]);
        syscall(SYS_close, p[0]);
        syscall(SYS_close, p[1]);
        runcmd(pcmd->left);
      }
      if (syscall(SYS_fork) == 0) {
        syscall(SYS_close, 0);
        syscall(SYS_dup, p[0]);
        syscall(SYS_close, p[0]);
        syscall(SYS_close, p[1]);
        runcmd(pcmd->right);
      }
      syscall(SYS_close, p[0]);
      syscall(SYS_close, p[1]);
      syscall(SYS_wait4, -1, 0, 0, 0);
      syscall(SYS_wait4, -1, 0, 0, 0);
      break;

    case BACK:
      bcmd = (struct backcmd*)cmd;
      if (syscall(SYS_fork) == 0) runcmd(bcmd->cmd);
      break;

    default:
      assert(0);
  }
  syscall(SYS_exit, 0);
}

int getcmd(char* buf, int nbuf) {
  print("> ", NULL);
  for (int i = 0; i < nbuf; i++) buf[i] = '\0';

  while (nbuf-- > 1) {
    int nread = syscall(SYS_read, 0, buf, 1);
    if (nread <= 0) return -1;
    if (*(buf++) == '\n') break;
  }
  return 0;
}

void _start() {
  static char buf[100];

  // Read and run input commands.
  while (getcmd(buf, sizeof(buf)) >= 0) {
    if (buf[0] == 'c' && buf[1] == 'd' && buf[2] == ' ') {
      // Chdir must be called by the parent, not the child.
      buf[strlen(buf) - 1] = 0;  // chop \n
      if (syscall(SYS_chdir, buf + 3) < 0) print("cannot cd ", buf + 3, "\n", NULL);
      continue;
    }
    if (syscall(SYS_fork) == 0) runcmd(parsecmd(buf));
    syscall(SYS_wait4, -1, 0, 0, 0);
  }
  syscall(SYS_exit, 0);
}

// Constructors

struct cmd* execcmd(void) {
  struct execcmd* cmd;

  cmd = zalloc(sizeof(*cmd));
  cmd->type = EXEC;
  return (struct cmd*)cmd;
}

struct cmd* redircmd(struct cmd* subcmd, char* file, char* efile, int mode,
                     int fd) {
  struct redircmd* cmd;

  cmd = zalloc(sizeof(*cmd));
  cmd->type = REDIR;
  cmd->cmd = subcmd;
  cmd->file = file;
  cmd->efile = efile;
  cmd->mode = mode;
  cmd->fd = fd;
  return (struct cmd*)cmd;
}

struct cmd* pipecmd(struct cmd* left, struct cmd* right) {
  struct pipecmd* cmd;

  cmd = zalloc(sizeof(*cmd));
  cmd->type = PIPE;
  cmd->left = left;
  cmd->right = right;
  return (struct cmd*)cmd;
}

struct cmd* listcmd(struct cmd* left, struct cmd* right) {
  struct listcmd* cmd;

  cmd = zalloc(sizeof(*cmd));
  cmd->type = LIST;
  cmd->left = left;
  cmd->right = right;
  return (struct cmd*)cmd;
}

struct cmd* backcmd(struct cmd* subcmd) {
  struct backcmd* cmd;

  cmd = zalloc(sizeof(*cmd));
  cmd->type = BACK;
  cmd->cmd = subcmd;
  return (struct cmd*)cmd;
}

// Parsing

char whitespace[] = " \t\r\n\v";
char symbols[] = "<|>&;()";

int gettoken(char** ps, char* es, char** q, char** eq) {
  char* s;
  int ret;

  s = *ps;
  while (s < es && strchr(whitespace, *s)) s++;
  if (q) *q = s;
  ret = *s;
  switch (*s) {
    case 0:
      break;
    case '|': case '(': case ')': case ';': case '&': case '<':
      s++;
      break;
    case '>':
      s++;
      if (*s == '>') {
        ret = '+'; s++;
      }
      break;
    default:
      ret = 'a';
      while (s < es && !strchr(whitespace, *s) && !strchr(symbols, *s)) s++;
      break;
  }
  if (eq) *eq = s;

  while (s < es && strchr(whitespace, *s)) s++;
  *ps = s;
  return ret;
}

int peek(char** ps, char* es, char* toks) {
  char* s;

  s = *ps;
  while (s < es && strchr(whitespace, *s)) s++;
  *ps = s;
  return *s && strchr(toks, *s);
}

struct cmd* parseline(char**, char*);
struct cmd* parsepipe(char**, char*);
struct cmd* parseexec(char**, char*);
struct cmd* nulterminate(struct cmd*);

struct cmd* parsecmd(char* s) {
  char* es;
  struct cmd* cmd;

  es = s + strlen(s);
  cmd = parseline(&s, es);
  peek(&s, es, "");
  assert(s == es);
  nulterminate(cmd);
  return cmd;
}

struct cmd* parseline(char** ps, char* es) {
  struct cmd* cmd;

  cmd = parsepipe(ps, es);
  while (peek(ps, es, "&")) {
    gettoken(ps, es, 0, 0);
    cmd = backcmd(cmd);
  }
  if (peek(ps, es, ";")) {
    gettoken(ps, es, 0, 0);
    cmd = listcmd(cmd, parseline(ps, es));
  }
  return cmd;
}

struct cmd* parsepipe(char** ps, char* es) {
  struct cmd* cmd;

  cmd = parseexec(ps, es);
  if (peek(ps, es, "|")) {
    gettoken(ps, es, 0, 0);
    cmd = pipecmd(cmd, parsepipe(ps, es));
  }
  return cmd;
}

struct cmd* parseredirs(struct cmd* cmd, char** ps, char* es) {
  int tok;
  char *q, *eq;

  while (peek(ps, es, "<>")) {
    tok = gettoken(ps, es, 0, 0);
    assert(gettoken(ps, es, &q, &eq) == 'a');
    switch (tok) {
      case '<':
        cmd = redircmd(cmd, q, eq, O_RDONLY, 0);
        break;
      case '>':
        cmd = redircmd(cmd, q, eq, O_WRONLY | O_CREAT | O_TRUNC, 1);
        break;
      case '+':  // >>
        cmd = redircmd(cmd, q, eq, O_WRONLY | O_CREAT, 1);
        break;
    }
  }
  return cmd;
}

struct cmd* parseblock(char** ps, char* es) {
  struct cmd* cmd;

  assert(peek(ps, es, "("));
  gettoken(ps, es, 0, 0);
  cmd = parseline(ps, es);
  assert(peek(ps, es, ")"));
  gettoken(ps, es, 0, 0);
  cmd = parseredirs(cmd, ps, es);
  return cmd;
}

struct cmd* parseexec(char** ps, char* es) {
  char *q, *eq;
  int tok, argc;
  struct execcmd* cmd;
  struct cmd* ret;

  if (peek(ps, es, "(")) return parseblock(ps, es);

  ret = execcmd();
  cmd = (struct execcmd*)ret;

  argc = 0;
  ret = parseredirs(ret, ps, es);
  while (!peek(ps, es, "|)&;")) {
    if ((tok = gettoken(ps, es, &q, &eq)) == 0) break;
    assert(tok == 'a');
    cmd->argv[argc] = q;
    cmd->eargv[argc] = eq;
    assert(++argc < MAXARGS);
    ret = parseredirs(ret, ps, es);
  }
  cmd->argv[argc] = 0;
  cmd->eargv[argc] = 0;
  return ret;
}

// NUL-terminate all the counted strings.
struct cmd* nulterminate(struct cmd* cmd) {
  int i;
  struct backcmd* bcmd;
  struct execcmd* ecmd;
  struct listcmd* lcmd;
  struct pipecmd* pcmd;
  struct redircmd* rcmd;

  if (cmd == 0) return 0;

  switch (cmd->type) {
    case EXEC:
      ecmd = (struct execcmd*)cmd;
      for (i = 0; ecmd->argv[i]; i++) *ecmd->eargv[i] = 0;
      break;

    case REDIR:
      rcmd = (struct redircmd*)cmd;
      nulterminate(rcmd->cmd);
      *rcmd->efile = 0;
      break;

    case PIPE:
      pcmd = (struct pipecmd*)cmd;
      nulterminate(pcmd->left);
      nulterminate(pcmd->right);
      break;

    case LIST:
      lcmd = (struct listcmd*)cmd;
      nulterminate(lcmd->left);
      nulterminate(lcmd->right);
      break;

    case BACK:
      bcmd = (struct backcmd*)cmd;
      nulterminate(bcmd->cmd);
      break;
  }
  return cmd;
}
```



```bash
$ gcc -c -ffreestanding a.c -g -O2
$ ld a.o -o sh
```

------

支持的功能

- 命令执行 `ls`
- 重定向 `ls > a.txt`
- 管道 `ls | wc -l`
- 后台 `ls &`
- 命令组合 `(echo a ; echo b) | wc -l`

### 3、A Zero-dependency UNIX Shell (from xv6)

我们应该如何阅读 [sh-xv6.c](http://jyywiki.cn/pages/OS/2022/demos/sh-xv6.c) 的代码？

- strace + gdb!
  - set follow-fork-mode, set follow-exec-mode

![img](http://jyywiki.cn/pages/OS/img/pipe.gif)

关键点

- 命令的执行、重定向、管道和对应的系统调用
- 这里用到 [minimal.S](http://jyywiki.cn/pages/OS/2022/demos/minimal.S) 会简化输出

```
echo './a.out > /tmp/a.txt' | strace -f ./sh
```

- 还可以用管道过滤不想要的系统调用



```bash
$ strace -f -o /tmp/strace.log ./sh
> ./a.out

// 另一个窗口
$ tail -f /tmp/strace.log
```

### 4、The Shell Programming Language

**基于文本替换的快速工作流搭建**

- 重定向: `cmd > file < file 2> /dev/null`
- 顺序结构: `cmd1; cmd2`, `cmd1 && cmd2`, `cmd1 || cmd2`
- 管道: `cmd1 | cmd2`
- 预处理: `$()`, `<()`
- 变量/环境变量、控制流……

------

Job control

- 类比窗口管理器里的 “叉”、“最小化”
  - jobs, fg, bg, wait
  - (今天的 GUI 并没有比 CLI 多做太多事)

### 5、UNIX Shell: Traps and Pitfalls

在 “自然语言”、“机器语言” 和 “1970s 的算力” 之间达到优雅的平衡

- 平衡意味着并不总是完美

------

- 操作的 “优先级”？
  - `ls > a.txt | cat` (bash/zsh)
- 文本数据 “责任自负”
  - 有空格？后果自负！(PowerShell: 我有 object stream pipe 啊喂)
- 行为并不总是 intuitive

```bash
$ echo hello > /etc/a.txt
bash: /etc/a.txt: Permission denied
$ sudo echo hello > /etc/a.txt
bash: /etc/a.txt: Permission denied
```

### 6、展望未来

> Open question: 我们能否从根本上改变命令行的交互模式？

Shell 连接了用户和操作系统

- 是 “自然语言”、“机器语言” 之间的边缘地带！
- 非常适合 BERT 这样的语言模型

------

已经看到的一些方向

- fish, zsh, ...
- Stackoverflow, tldr, [thef**k](https://github.com/nvbn/thefuck) (自动修复)
- Command palette of vscode (Ctrl-Shift-P)
- [Executable formal semantics for the POSIX shell](https://dl.acm.org/doi/10.1145/3371111) (POPL'20)

## 三、终端和 Job Control

### 1、Shell 还有一些未解之谜

为什么 Ctrl-C 可以退出程序？

为什么有些程序又不能退出？

- 没有人 read 这个按键，为什么进程能退出？
- Ctrl-C 到底是杀掉一个，还是杀掉全部？
    - 如果我 fork 了一份计算任务呢？
    - 如果我 fork-execve 了一个 shell 呢？
        - Hmmm……

------

为什么 [fork-printf.c](http://jyywiki.cn/pages/OS/2022/demos/fork-printf.c) 会在管道时有不同表现？

- libc 到底是根据什么调整了缓冲区的行为？

------

为什么 Tmux 可以管理多个窗口？

### 2、答案：终端

终端是 UNIX 操作系统中一类非常特别的设备！

- RTFM: tty, stty, ...

### 3、观察 Tmux 的实现

![img](./doc/tmux-cheatsheet.png)

首先，我们可以 “使用” tmux

- 在多个窗口中执行 tty，会看到它们是不同的终端设备！

------

然后，我们也可以把 tmux “打开”

- strace (`-o`) 可以看到一些关键的系统调用 (以及 man 7 pty)

### 4、终端相关的 API

为什么 `fork-printf` 能识别 tty 和管道？

- 当然是观察 strace 了！
    - 找到是哪个系统调用 “识别” 出了终端？

------

```c
#include <stdio.h>

int main() {
  printf("Hello, World\n");
}
```



```bash
$ strace ./a.out
...
fstat(1, {st_mode=S_IFCHR|0600, st_rdev=makedev(0x88, 0), ...}) = 0
...

$ strace ./a.out > /dev/null
...
fstat(1, {st_mode=S_IFCHR|0666, st_rdev=makedev(0x1, 0x3), ...}) = 0
ioctl(1, TCGETS, 0x7fff583c6910)        = -1 ENOTTY (Inappropriate ioctl for device)
...
```

### 5、Session, Process Group 和信号

![img](./doc/process-groups-sessions.png)

参考 [signal-handler.c](http://jyywiki.cn/pages/OS/2022/demos/signal-handler.c)

```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void handler(int signum) {
  switch (signum) {
    case SIGINT:
      printf("Received SIGINT!\n");
      break;
    case SIGQUIT:
      printf("Received SIGQUIT!\n");
      exit(0);
      break;
  }
}

void cleanup() {
  printf("atexit() cleanup\n");
}

int main() {
  // fork(); 观察下行为
  signal(SIGINT,  handler);
  signal(SIGQUIT, handler);
  atexit(cleanup);

  while (1) {
    char buf[4096];
    int nread = read(STDIN_FILENO, buf, sizeof(buf));
    buf[nread - 1] = '\0';
    printf("[%d] Got: %s\n", getpid(), buf);
    if (nread < 0) {
      perror("read");
      exit(1);
    }
    sleep(1);
  }
}
```

```bash
$ gcc a.c && ./a.out 
asdf
[654336] Got: asdf
^CReceived SIGINT!
```

### 6、SIGSEGV 和 SIGFPE

大家熟悉的 Segmentation Fault/Floating point exception (core dumped)

- \#GP, #PF 或 #DIV
    - UNIX 系统会给进程发送一个信号
    - 此时可以生成一个 “core” 文件 (ELF 格式)，能用 gdb 调试

------

UNIX (System V) 信号其实是有一些 dark corners 的

- 如果 `SIGSEGV` 里再次 `SIGSEGV`?
    - POSIX.1 solved the portability mess by specifying `sigaction(2)`, which provides explicit control of the semantics when a signal handler is invoked; use that interface instead of `signal()`.
        - 支持多线程 (早期的 UNIX 还没有多线程)、信号屏蔽...

### 7、Job Control 背后的机制

> RTFM: setpgid/getpgid(2)，它解释了 process group, session, controlling terminal 之间的关系
>
> ——你神奇地发现，读手册不再是障碍了！

- The PGID (process-group ID) is preserved across an execve(2) and inherited in fork(2)...
- Each process group is a member of a *session*

![img](./doc/tty-session.png)

- A session can have a controlling terminal.
    - At any time, one (and only one) of the process groups in the session can be the foreground process group for the terminal; the remaining process groups are in the background.
        - `./a.out &` 创建新的进程组 (使用 setpgid)
    - If a signal is generated from the terminal (e.g., typing the interrupt key to generate`SIGINT`), that signal is sent to the foreground process group.
        - Ctrl-C 是终端 (设备) 发的信号，发给 foreground 进程组
        - 所有 fork 出的进程 (默认同一个 PGID) 都会收到信号
        - 可以修改 [signal-handler.c](http://jyywiki.cn/pages/OS/2022/demos/signal-handler.c) 观察到这个行为

- Only the foreground process group may read(2) from the terminal; if a background process group tries to read(2) from the terminal, then the group is sent a `SIGTTIN` signal, which suspends it.
    - 这解释了 `cat &` 时你看到的 “suspended (tty input)”
    - 同一个进程组的进程 read tty 会竞争
    - [signal-handler.c](http://jyywiki.cn/pages/OS/2022/demos/signal-handler.c) 同样可以观察到这个行为

------

- The `setpgid()` and `getpgrp()` calls are used by programs such as bash(1) to create process groups in order to implement shell job control.
    - 如果希望从进程组里 detach, 使用 setpgid
    - `ps -eo pid,pgid,cmd` 可以查看进程的 pgid

## 总结

本次课回答的问题

- **Q**: 我们作为用户，到底怎么 “使用” 操作系统？

------

Take-away messages

- 一个功能完整的 Shell 使用的操作系统对象和 API
    - session, process group, controlling terminal
    - 文件描述符：open, close, pipe, dup, read, write
    - 状态机管理：fork, execve, exit, wait, signal, kill, setpgid, getpgid, ...
- 随着 “零依赖” 的 [sh-xv6.c](http://jyywiki.cn/pages/OS/2022/demos/sh-xv6.c)，操作系统的神秘感逐渐消失
    - (下次课拆开库函数)