# GDB

文档：[http://sourceware.org/gdb/documentation/](http://sourceware.org/gdb/documentation/)

gdb命令包含在GNU的gcc开发套件中，是功能强大的程序调试器。GDB中的命令固然很多，但我们只需掌握其中十个左右的命令，就大致可以完成日常的基本的程序调试工作。

```shell
gdb <选项> <二进制文件>

-cd：设置工作目录； 
-q：安静模式，不打印介绍信息和版本信息； 
-d：添加文件查找路径； 
-x：从指定文件中执行GDB指令； 
-s：设置读取的符号表文件。
```

## 一、常用命令

### 1、加载

```
(gdb) file gdb-sample
```

加载被调试的可执行程序文件。 因为一般都在被调试程序所在目录下执行GDB，因而文本名不需要带路径。

### 2、运行至断点

```
(gdb) r
```

Run的简写，运行被调试的程序。 如果此前没有下过断点，则执行完整个程序；如果有断点，则程序暂停在第一个可用断点处。

```
(gdb) c
```

Continue的简写，继续执行被调试程序，直至下一个断点或程序结束。

### 3、设置断点

```
b <行号> 
b <函数名称> 
b *<函数名称> 
b *<代码地址> 
d [编号]

(gdb) b 8 
(gdb) b main 
(gdb) b *main 
(gdb) b *0x804835c 
(gdb) d
```

b: Breakpoint的简写，设置断点。两可以使用“行号”“函数名称”“执行地址”等方式指定断点位置。

其中在函数名称前面加“*”符号表示将断点设置在“由编译器生成的prolog代码处”。如果不了解汇编，可以不予理会此用法。

### 4、删除断点

d: Delete breakpoint的简写，删除指定编号的某个断点，或删除所有断点。断点编号从1开始递增。

### 5、执行

```
(gdb) s 
(gdb) n
```

s: 执行一行源程序代码，如果此行代码中有函数调用，则进入该函数；**执行进入**

n: 执行一行源程序代码，此行代码中的函数调用也一并执行。 s 相当于其它调试器中的“Step Into (单步跟踪进入)”；**执行跳过**

n 相当于其它调试器中的“Step Over (单步跟踪)” 

这两个命令必须在有源代码调试信息的情况下才可以使用（GCC编译时使用“-g”参数）

```
(gdb) si
(gdb) ni
```

si命令类似于s命令，ni命令类似于n命令。

所不同的是，这两个命令（si/ni）所针对的是汇编指令，而s/n针对的是源代码。

### 6、打印变量

```
p <变量名称>

(gdb) p i 
(gdb) p nGlobalVar
```

Print的简写，显示指定变量（临时变量或全局变量）的值。

### 7、设置中断后显示

```
display ... 
undisplay <编号>

(gdb) display /i $pc 
(gdb) undisplay 1
```

display，设置程序中断后欲显示的数据及其格式。 

例如，如果希望每次程序中断后可以看到即将被执行的下一条汇编指令，可以使用命令 “display /i $pc” 其中 $pc 代表当前汇编指令，/i 表示以十六进行显示。

当需要关心汇编代码时，此命令相当有用。

undispaly，取消先前的display设置，编号从1开始递增。

### 8、退出

```
(gdb) q
```

Quit的简写，退出GDB调试环境。

### 9、信息查看

```
i
(gdb) i r
```

Info的简写，用于显示各类信息，详情请查阅“help i”。

```
help [命令名称]

(gdb) help
```

GDB帮助命令，提供对GDB名种命令的解释说明。 如果指定了“命令名称”参数，则显示该命令的详细说明；如果没有指定参数，则分类显示所有GDB命令，供用户进一步浏览和查询。

## 二、layout

ayout：用于分割窗口，可以一边查看代码，一边测试。主要有以下几种用法：

layout src：显示源代码窗口

layout asm：显示汇编窗口

layout regs：显示源代码/汇编和寄存器窗口

layout split：显示源代码和汇编窗口

layout next：显示下一个layout

layout prev：显示上一个layout

Ctrl + L：刷新窗口

Ctrl + x，再按1：单窗口模式，显示一个窗口

Ctrl + x，再按2：双窗口模式，显示两个窗口

Ctrl + x，再按a：回到传统模式，即退出layout，回到执行layout之前的调试窗口



**示例**：

gdb中输入tui enable可以打开源代码展示窗口。

在gdb中输入layout asm，可以在tui窗口看到所有的汇编指令。再输入layout reg可以看到所有的寄存器信息。

你可以在gdb中输入info breakpoints，你可以看到所有设置了的断点。你甚至可以看到这个断点已经被命中了几次。

现在我们在dummymain函数中。如果我们在gdb中输入info frame，可以看到有关当前Stack Frame许多有用的信息。

输入backtrace（简写bt）可以看到从当前调用栈开始的所有Stack Frame。

如果对某一个Stack Frame感兴趣，可以先定位到那个frame（frame 3）再输入info frame，假设对syscall的Stack Frame感兴趣。
