# GDB

官网：[http://sourceware.org/gdb/documentation/](http://sourceware.org/gdb/documentation/)

文档：https://sourceware.org/gdb/current/onlinedocs/gdb/

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

### 1. 加载

加载被调试的可执行程序文件。 因为一般都在被调试程序所在目录下执行GDB，因而文本名不需要带路径。

```
(gdb) file gdb-sample
```

start，运行被调试的程序，达到c源码的第一行停下来，一般是main

starti，运行被调试的程序，达到汇编的第一行停下来，一般是 _start

```
(gdb) start
(gdb) starti
```

Run的简写，运行被调试的程序。 如果此前没有下过断点，则执行完整个程序；如果有断点，则程序暂停在第一个可用断点处。

```
(gdb) run
(gdb) r
```

### 2. 设置断点

#### breakpoints

b: Breakpoint的简写，设置断点。两可以使用“行号”“函数名称”“执行地址”等方式指定断点位置。

其中在函数名称前面加“*”符号表示将断点设置在“由编译器生成的prolog代码处”。如果不了解汇编，可以不予理会此用法。

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

#### watchpoints

A *watchpoint* is a special breakpoint that stops your program when the value of an expression changes. The expression may be a value of a variable, or it could involve values of one or more variables combined by operators, such as ‘a + b’. This is sometimes called *data breakpoints*. You must use a different command to set watchpoints (see [Setting Watchpoints](https://sourceware.org/gdb/current/onlinedocs/gdb/Set-Watchpoints.html#Set-Watchpoints)), but aside from that, you can manage a watchpoint like any other breakpoint: you enable, disable, and delete both breakpoints and watchpoints using the same commands.

```
(gdb) watch a           
Hardware watchpoint 2: a
(gdb) c                  
Continuing.              
                         
Hardware watchpoint 2: a 
                         
Old value = 32767        
New value = 0            
main () at a.c:5    
(gdb) c                 
Continuing.             
                        
Hardware watchpoint 2: a
                        
Old value = 0           
New value = 3           
main () at a.c:7        
```

#### Catchpoints

You can use *catchpoints* to cause the debugger to stop for certain kinds of program events, such as C`++` exceptions or the loading of a shared library. Use the `catch` command to set a catchpoint.

[Set Catchpoints (Debugging with GDB) (sourceware.org)](https://sourceware.org/gdb/current/onlinedocs/gdb/Set-Catchpoints.html#Set-Catchpoints)

### 3. 运行至断点

```
(gdb) c
```

Continue的简写，继续执行被调试程序，直至下一个断点（断点行不执行）或程序结束。

### 4. 删除\禁用断点

d: Delete breakpoint的简写，删除指定编号的某个断点，或删除所有断点。断点编号从1开始递增。

```
(gdb) i b
(gdb) d 1
```

Rather than deleting a breakpoint, watchpoint, or catchpoint, you might prefer to *disable* it. This makes the breakpoint inoperative as if it had been deleted, but remembers the information on the breakpoint so that you can *enable* it again later.

```
disable [breakpoints] [list…]
enable [breakpoints] [list…]
```

### 5. 执行

```
(gdb) s 
(gdb) n
(gdb) s <count>
(gdb) n <count>
```

s/step: 执行一行源程序代码，如果此行代码中有函数调用，则进入该函数；**执行进入**

n/next: 执行一行源程序代码，此行代码中的函数调用也一并执行。 s 相当于其它调试器中的“Step Into (单步跟踪进入)”；**执行跳过**

n 相当于其它调试器中的“Step Over (单步跟踪)” 

这两个命令必须在有源代码调试信息的情况下才可以使用（GCC编译时使用“-g”参数）

```
(gdb) si
(gdb) ni
```

si命令类似于s命令，ni命令类似于n命令。

所不同的是，这两个命令（si/ni）所针对的是汇编指令，而s/n针对的是源代码。

### 6. 打印变量

Print的简写，显示指定变量（临时变量或全局变量）的值。

```
p <变量名称>

(gdb) p i 
(gdb) p nGlobalVar
```

以 `all_thread` 数组为例

打印 16 进制信息

```
p/x *all_thread
```

打印前4个元素，打印下标从m开始的n个元素：

```
p/x *all_thread@4
p/x *all_thread[m]@n
```



### 7. 设置中断后显示

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

### 8. 退出

```
(gdb) q
```

Quit的简写，退出GDB调试环境。

### 9. 信息查看

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

layout：用于分割窗口，可以一边查看代码，一边测试。主要有以下几种用法：

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

### 示例

- gdb中输入 `tui enable` 可以打开源代码展示窗口。
- 在gdb中输入 `layout asm`，可以在tui窗口看到所有的汇编指令。再输入 `layout reg` 可以看到所有的寄存器信息。
- 你可以在gdb中输入 `info breakpoints` ，你可以看到所有设置了的断点。你甚至可以看到这个断点已经被命中了几次。
- 现在我们在 dummymain 函数中。如果我们在gdb中输入 `info frame` ，可以看到有关当前Stack Frame许多有用的信息。
- 输入 `backtrace`（简写 `bt` ）可以看到从当前调用栈开始的所有Stack Frame。
- 如果对某一个Stack Frame感兴趣，可以先定位到那个frame（ `frame 3` ）再输入`info frame` ，假设对syscall的Stack Frame感兴趣。
## 三、Examining the Stack

### 1. Stack Frames

When your program has stopped, the first thing you need to know is where it stopped and how it got there.

Each time your program performs a function call, information about the call is generated. That information includes the location of the call in your program, the arguments of the call, and the local variables of the function being called. The information is saved in a block of data called a *stack frame*. The stack frames are allocated in a region of memory called the *call stack*.

Inside your program, stack frames are identified by their addresses. A stack frame consists of many bytes, each of which has its own address; each kind of computer has a convention for choosing one byte whose address serves as the address of the frame. Usually this address is kept in a register called the *frame pointer register* (see [$fp](https://sourceware.org/gdb/current/onlinedocs/gdb/Registers.html#Registers)) while execution is going on in that frame.

```
(gdb) p $fp
$1 = (void *) 0x7fffffffe210
```

### 2. Backtraces

A backtrace is a summary of how your program got where it is. It shows one line per frame, for many frames, starting with the currently executing frame (frame zero), followed by its caller (frame one), and on up the stack.

To print a backtrace of the entire stack, use the `backtrace` command, or its alias `bt`. This command will print one line per frame for frames in the stack. By default, all stack frames are printed. You can stop the backtrace at any time by typing the system interrupt character, normally Ctrl-c.

```
(gdb) bt                                   
#0  foo (t=10) at a.c:4                    
#1  0x000055555555468a in main () at a.c:14
(gdb) bt 1                   
#0  foo (t=10) at a.c:4      
(More stack frames follow...)
```

### 3. Selecting a Frame

Most commands for examining the stack and other data in your program work on whichever stack frame is selected at the moment. Here are the commands for selecting a stack frame; all of them finish by printing a brief description of the stack frame just selected.

- `frame [ frame-selection-spec ]`
- `f [ frame-selection-spec ]`

```
(gdb) frame 3
(gdb) frame address stack-address
```

Select the frame with stack address stack-address. The stack-address for a frame can be seen in the output of `info frame`, for example:

```
(gdb) info frame
Stack level 1, frame at 0x7fffffffda30:
 rip = 0x40066d in b (amd64-entry-value.cc:59); saved rip 0x4004c5
 tail call frame, caller of frame at 0x7fffffffda30
 source language c++.
 Arglist at unknown address.
 Locals at unknown address, Previous frame's sp is 0x7fffffffda30
```

The stack-address for this frame is `0x7fffffffda30` as indicated by the line:

```
Stack level 1, frame at 0x7fffffffda30:
```

### 4. Information About a Frame

There are several other commands to print information about the selected stack frame.

```
(gdb) frame
(gdb) f
```

When used without any argument, this command does not change which frame is selected, but prints a brief description of the currently selected stack frame. It can be abbreviated `f`. With an argument, this command is used to select a stack frame. See [Selecting a Frame](https://sourceware.org/gdb/current/onlinedocs/gdb/Selection.html#Selection).

```
(gdb) info frame
(gdb) info f
```

This command prints a verbose description of the selected stack frame, including:the address of the framethe address of the next frame down (called by this frame)the address of the next frame up (caller of this frame)the language in which the source code corresponding to this frame is writtenthe address of the frame’s argumentsthe address of the frame’s local variablesthe program counter saved in it (the address of execution in the caller frame)which registers were saved in the frameThe verbose description is useful when something has gone wrong that has made the stack format fail to fit the usual conventions.

```
(gdb) info frame [ frame-selection-spec ]
(gdb) info f [ frame-selection-spec ]
```

Print a verbose description of the frame selected by frame-selection-spec. The frame-selection-spec is the same as for the `frame` command (see [Selecting a Frame](https://sourceware.org/gdb/current/onlinedocs/gdb/Selection.html#Selection)). The selected frame remains unchanged by this command.

## 四、Examining Data

[Data (Debugging with GDB) (sourceware.org)](https://sourceware.org/gdb/current/onlinedocs/gdb/Data.html#Data)

| • [Expressions](https://sourceware.org/gdb/current/onlinedocs/gdb/Expressions.html#Expressions): |      | Expressions                                                  |
| ------------------------------------------------------------ | ---- | ------------------------------------------------------------ |
| • [Ambiguous Expressions](https://sourceware.org/gdb/current/onlinedocs/gdb/Ambiguous-Expressions.html#Ambiguous-Expressions): |      | Ambiguous Expressions                                        |
| • [Variables](https://sourceware.org/gdb/current/onlinedocs/gdb/Variables.html#Variables): |      | Program variables                                            |
| • [Arrays](https://sourceware.org/gdb/current/onlinedocs/gdb/Arrays.html#Arrays): |      | Artificial arrays                                            |
| • [Output Formats](https://sourceware.org/gdb/current/onlinedocs/gdb/Output-Formats.html#Output-Formats): |      | Output formats                                               |
| • [Memory](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory.html#Memory): |      | Examining memory                                             |
| • [Memory Tagging](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory-Tagging.html#Memory-Tagging): |      | Memory Tagging                                               |
| • [Auto Display](https://sourceware.org/gdb/current/onlinedocs/gdb/Auto-Display.html#Auto-Display): |      | Automatic display                                            |
| • [Print Settings](https://sourceware.org/gdb/current/onlinedocs/gdb/Print-Settings.html#Print-Settings): |      | Print settings                                               |
| • [Pretty Printing](https://sourceware.org/gdb/current/onlinedocs/gdb/Pretty-Printing.html#Pretty-Printing): |      | Python pretty printing                                       |
| • [Value History](https://sourceware.org/gdb/current/onlinedocs/gdb/Value-History.html#Value-History): |      | Value history                                                |
| • [Convenience Vars](https://sourceware.org/gdb/current/onlinedocs/gdb/Convenience-Vars.html#Convenience-Vars): |      | Convenience variables                                        |
| • [Convenience Funs](https://sourceware.org/gdb/current/onlinedocs/gdb/Convenience-Funs.html#Convenience-Funs): |      | Convenience functions                                        |
| • [Registers](https://sourceware.org/gdb/current/onlinedocs/gdb/Registers.html#Registers): |      | Registers                                                    |
| • [Floating Point Hardware](https://sourceware.org/gdb/current/onlinedocs/gdb/Floating-Point-Hardware.html#Floating-Point-Hardware): |      | Floating point hardware                                      |
| • [Vector Unit](https://sourceware.org/gdb/current/onlinedocs/gdb/Vector-Unit.html#Vector-Unit): |      | Vector Unit                                                  |
| • [OS Information](https://sourceware.org/gdb/current/onlinedocs/gdb/OS-Information.html#OS-Information): |      | Auxiliary data provided by operating system                  |
| • [Memory Region Attributes](https://sourceware.org/gdb/current/onlinedocs/gdb/Memory-Region-Attributes.html#Memory-Region-Attributes): |      | Memory region attributes                                     |
| • [Dump/Restore Files](https://sourceware.org/gdb/current/onlinedocs/gdb/Dump_002fRestore-Files.html#Dump_002fRestore-Files): |      | Copy between memory and a file                               |
| • [Core File Generation](https://sourceware.org/gdb/current/onlinedocs/gdb/Core-File-Generation.html#Core-File-Generation): |      | Cause a program dump its core                                |
| • [Character Sets](https://sourceware.org/gdb/current/onlinedocs/gdb/Character-Sets.html#Character-Sets): |      | Debugging programs that use a different character set than GDB does |
| • [Caching Target Data](https://sourceware.org/gdb/current/onlinedocs/gdb/Caching-Target-Data.html#Caching-Target-Data): |      | Data caching for targets                                     |
| • [Searching Memory](https://sourceware.org/gdb/current/onlinedocs/gdb/Searching-Memory.html#Searching-Memory): |      | Searching memory for a sequence of bytes                     |
| • [Value Sizes](https://sourceware.org/gdb/current/onlinedocs/gdb/Value-Sizes.html#Value-Sizes): |      | Managing memory allocated for values                         |

