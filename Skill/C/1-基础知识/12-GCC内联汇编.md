# GCC内联汇编

[GCC内联汇编](https://www.jianshu.com/p/1782e14a0766)

[GCC-Inline-Assembly-HOWTO (ibiblio.org)](http://www.ibiblio.org/gferg/ldp/GCC-Inline-Assembly-HOWTO.html)

中文翻译：[最牛X的GCC 内联汇编 | 《Linux就该这么学》 (linuxprobe.com)](https://www.linuxprobe.com/gcc-how-to.html)

[C 语言内联汇编介绍](https://blog.csdn.net/longintchar/article/details/107594725)

## 一、概要

在讨论GCC内联汇编之前，我们先来搞搞清楚，到底什么是内联汇编？

先看在C语言中，我们可以指定编译器将一个函数代码直接**复制**到调用其代码的地方执行。这种函数调用方式和默认压栈调用方式不同，我们称这种函数为内联函数。内联函数看起来很像宏？两者确实有许多共同之处。

那么，内联函数有哪些优点呢？

很明显，**内联函数**降低了函数的调用开销：如果多次被调用的某个函数实参相同，那么它的返回值一定是相同的，这就给编译器留下了优化空间。此时编译器完全可以直接用这个返回值替代这个函数，而不必把该函数的代码插入到调用者的代码中再去计算结果了。如此一来，不但减少了代码量，还节省了计算资源。指定编译器将一个函数处理为内联函数，我们只要在函数申明前加上inline关键字即可。

基于对上述内联函数的认知，我们大概可以想象出**内联汇编**到底是怎么一回事了。内联汇编相当于用汇编语句写成的内联函数。它方便，快速，对系统编程有着举足轻重的作用。本文主要就**GCC**内联函数的格式和使用方法展开讨论。在GCC中声明一个内联汇编函数，我们要用asm这个关键字。

之所以内联汇编如此有用，主要是因为它可以操作C语言变量，比如可以输出值到C语言变量。这个特性使内联汇编成为汇编代码和调用其C程序之间的桥梁。

## 二、GCC汇编格式

GCC (GNU Compiler for Linux) 使用AT&T/UNIX汇编语法。所以这篇文章将会用AT&T汇编格式来写汇编代码。如果你不熟悉AT&T汇编语法也没有关系，下面会有些简单的介绍。AT&T和Intel汇编语法差别比较大，二者主要不同之处如下：

### 源操作数和目的操作数的方向

AT&T和Intel汇编语法源操作数和目的操作数的方向正好相反。Intel中第一个操作数作为目的操作数，第二个操作数作为源操作数。而**在AT&T中，第一个操作数是源操作数，第二个是目的操作数**：

```
OP-code dst src //Intel语法
Op-code src dst //AT&T语法
```

### 寄存器命名

在AT&T汇编中, 寄存器名前有 `%` 前缀。例如，如果要使用 `eax`，得写作: `%eax`

### 立即数 (Immediate Operand)

在AT&T语法中，立即数(Immediate Operand)都有 `$` 前缀。引用的C语言静态变量 (static C variables) 也必须放上 `$` 前缀；

此外，在Intel语法中, 16进制的常数是以 `h` 作为后缀的，但是在AT&T语法中, 是以 `0x` 作为前缀的。因此，在AT&T语法中，一个16进制常数的写法是：首先以 `$` 开头接着是 `0x`，最后是常数本身。

### 操作数大小

在AT&T语法中，操作符的最后一个字符决定着操作数访问内存的长度：以 `b`, `w` 和 `l` 为后缀指明内存访问长度是 byte(8-bit), word(16-bit)还是long(32-bit)。而Intel语法在操作数前加上 `byte ptr`, `word ptr` 和 `dword ptr` 的内存操作符来达到相同目的。

因此 Intel汇编写法：

```
mov al, byte ptr foo
```

用AT&T语法写就是：

```
movb foo, %al
```

### 内存操作数

在Intel语法中，基址寄存器是放在方括号 `[]` 中的，但AT&T是放在小括弧 `()` 内的。

因此，在Intel语法中，一个间接内存寻址是这么写的：

```
section:[base + index * scale + disp]
```

而在AT&T中则应该写成这样：

```
section:disp(base, index, scale)
```

此外对于AT&T汇编，当一个常数被用作disp或者scale时，不需要 `$` 前缀。这点需要记住

以上就是AT&T和Intel汇编语法的一些主要不同点。这只是一小部分，具体内容需要参考GNU汇编文档。为了更好理解这些不同，这里给出一些实例作为对照：

| Intel Code               | AT&T Code                      |
| ------------------------ | ------------------------------ |
| mov eax,1                | movl $1,%eax                   |
| mov ebx,0ffh             | movl $0xff,%ebx                |
| int 80h                  | int $0x80                      |
| mov ebx, eax             | movl %eax, %ebx                |
| mov eax,[ecx]            | movl (%ecx),%eax               |
| mov eax,[ebx+3]          | movl 3(%ebx),%eax              |
| mov eax,[ebx+20h]        | movl 0x20(%ebx),%eax           |
| add eax,[ebx+ecx*2h]     | addl (%ebx,%ecx,0x2),%eax      |
| lea eax,[ebx+ecx]        | leal (%ebx,%ecx),%eax          |
| sub eax,[ebx+ecx*4h-20h] | subl -0x20(%ebx,%ecx,0x4),%eax |

## 三、基本内联汇编 (Basic Inline)

基本内联汇编格式比较直观，可以直接这样写：

```c
asm("assembly code");
```

例如:

```c
asm("movl %ecx, %eax");       	// 把 ecx 内容移动到 eax
__asm__("movb %bh , (%eax)");  	// 把bh中一个字节的内容移动到eax指向的内存
```

你可能注意到了这里使用了两个不同的关键字 `asm` 和 `__asm__`。这两个关键字都可以使用。不过当遇到 `asm` 关键字与程序其他变量有冲突的时候就必须用 `__asm__` 了。如果内联汇编有多条指令，则每行要加上双引号，并且该行要以 `\n\t` 结尾。这是因为GCC会将每行指令作为一个字符串传给as(GAS)，使用换行和TAB可以将正确且格式良好的代码行传递给汇编器。

举个例子:

```c
__asm__("movl %eax, %ebx\n\t"
        "movl $56, %esi\n\t"
        "movl %ecx, $label(%edx,%ebx,$4)\n\t"
        "movb %ah, (%ebx)");
```

如果在内联代码中操作了一些寄存器，比如你修改了寄存器内容（而之后也没有进行还原操作），程序很可能会产生一些难以预料的情况。

因为此时GCC并不知道你已经将寄存器内容修改了。这点尤其是在编译器对代码进行了一些优化的情况下而导致问题。因为编译器注意不到寄存器内容已经被改掉，程序将当作它没有被修改过而继续执行。所以此时我们尽量不要使用这些会产生附加影响的操作，或者当我们退出的时候还原这些操作。否则很可能会造成程序崩溃。

再一个例子

```c
#include <stdio.h>

int sum(int a, int b) {
    // asm("addl %edi, %esi");
    // asm("movl %esi, %eax");
    asm("addl %edi, %esi\n\t"
        "movl %esi, %eax\n\t");
}

int main() {
    printf("%d\n", sum(2, 3));
    return 0;
}
```

可是如果我们必须要这样操作该怎么办呢？我们可以通过下面的讨论的扩展内联汇编进行。

## 四、扩展内联汇编 (Extended Asm)

前面讨论的基本内联汇编只涉及到嵌入汇编指令，而**在扩展形式中，我们还可以指定操作数，并且可以选择输入输出寄存器，以及指明要修改的寄存器列表**。对于要访问的寄存器，并不一定要要显式指明，也可以留给GCC自己去选择，这可能让GCC更好去优化代码。

扩展内联汇编格式如下:

```c
asm (assembler template
     : output operands               /* optional */
     : input operands                /* optional */
     : list of clobbered registers   /* optional */
);
```

- 其中assembler template为汇编指令部分。
- 括号内的操作数都是C语言表达式中常量字符串。
- 不同部分之间使用冒号分隔。
- 相同部分语句中的每个小部分用逗号分隔。
- 最多可以指定10个操作数，不过可能有的计算机平台有额外的文档说明可以使用超过10个操作数。

此外，如果没有输出部分但是有输入部分，我们还得保留输出部分前面的冒号。就像下面这样：

```c
asm ( "cld\n\t"
      "rep\n\t"
      "stosl"
      : /* no output registers */
      : "c" (count), "a" (fill_value), "D" (dest)
      : "%ecx", "%edi"
);
```

上述代码做了些什么呢？

它主要是循环 `count` 次把 `fill_value` 的值到填充到 `edi` 寄存器指定的内存位置。并且告诉GCC，寄存器 `ecx` 和 `edi` 中的内容可能已经被改变了。 

为了有一个更清晰的理解，我们再来看一个例子：

```c
#include <stdio.h>

int main() {
    int a = 10, b;
    printf("a:%d, b:%d\n", a, b);

    asm("movl %1, %%eax; movl %%eax, %0;"
        : "=r"(b) /* output */
        : "r"(a)  /* input */
        : "%eax"  /* clobbered register */
    );

    printf("a:%d, b:%d\n", a, b);

    return 0;
}
// a:10, b:0
// a:10, b:10
```

上面代码实现的功能就是用汇编代码把a的值赋给b。值得注意的几点有:

- `b` 是输出操作数，用 `%0` 来访问，`a` 是输入操作数，用 `%1` 来访问。

- `r` 是一个**constraint**, 关于constraint后面有详细的介绍。这里我们只要记住这里 `r` 的意思就是让GCC自己去选择一个寄存器去存储变量 `a`。输出部分constraint前必须要有个 `=` 修饰，用来说明是一个这是一个输出操作数，并且是只写(write only)的。

- 你可能已经注意到，有的寄存器名字前面用了 `％%` ，这是用来让GCC区分操作数和寄存器的：操作数已经用了一个 `%` 作为前缀，寄存器只能用 `%%` 做前缀了。

- 第三个冒号后面的clobbered register部分有个 `%eax`，意思是内联汇编代码中会改变寄存器 `eax` 的内容，如此一来GCC在调用内联汇编前就不会依赖保存在寄存器 `eax` 中的内容了。

当这段代码执行结束后，变量 `b` 的值将会被改写，因为它是被指定作为输出操作数的。这里可以看出在 `asm` 内部对 `b` 的改动将影响到 `asm` 外了，正如之前所说的内联汇编起到桥梁作用。

下面我们将对扩展内联汇编各个部分分别进行详细的讨论。

### 汇编模板

汇编模板部分就是嵌入在C程序中的汇编指令，格式如下：

- 每条指令放在一个双引号内，或者将所有的指令都放着一个双引号内。
- 每条指令都要包含一个分隔符。合法的分隔符是换行符 `\n` 或者分号 `;`。用换行符的时候通常后面放一个制表符 `\t`。对此前文已经有所说明。
- 访问C语言变量用 `%0,%1…` 等等。

### 操作数

`asm` 内部使用C语言字符串作为操作数。

- 操作数都要放在双引号 `" "` 中。
- 对于输出操作数，还要用 `=` 修饰
- constraint和修饰都放在双引号 `" "` 内。
- 之后是C表达式了。就像下面这样:

```c
"constraint" (C expression) // "=r"(result)
```

对于输出操作数一定要用 `=` 修饰。

constraint主要用来指定操作数的寻址类型 (内存寻址或寄存器寻址)，也用来指明使用哪个寄存器。

如果有多个操作数，使用逗号 `,` 隔开。

在汇编模板部分，我们按顺序用数字去引用操作数，引用规则如下：

如果总共有 n 个操作数(包括输入输出操作数)，那么第一个输出操作引用数字为 `0`，依次递增，然后最后一个操作数是 `n-1`。关于操作数数量限制参见前面的章节。

输出操作数表达式必须是左值，输入操作数没有这个限制。注意这里可以使表达式，不仅仅指一个变量。当编译器不知道有这个机器指令的时候（比如新CPU指令出来的时候，编译器还没有支持该指令），扩展汇编形式就能发挥其用武之地了。如果输出表达式不能直接寻址(比如是[bit-field]), constraint就必须指定一个寄存器。这种情况下，GCC将使用寄存器作为asm的输出。然后保存这个寄存器的值到输出表达式中。

如前文所描述，一般输出操作数必须是只写 (write only)的；GCC将认为在这条指令之前，保存在这种操作数中的值已经过期和不再需要了。当然也支持输入输出类型或者可读可写类型的操作数。

现在我们来看一些例子:

要求把一个数字乘以5，我们可以使用汇编指令lea来实现，具体方法如下：

```c
#include <stdio.h>

int main() {
    int x = 10, five_times_x;
    printf("x:%d, five_times_x:%d\n", x, five_times_x);

    asm("leal (%1,%1,4), %0"
        : "=r"(five_times_x)
        : "r"(x));

    printf("x:%d, five_times_x:%d\n", x, five_times_x);

    return 0;
}
// x:10, five_times_x:0
// x:10, five_times_x:50
```

这里输入操作数是 `x`，因为没有指定具体要使用那个寄存器，GCC会自己选择合适的输入输出寄存器。我们也可以修改constraint部分内容，让GCC固定使用同一个寄存器，具体方法如下:

```c
#include <stdio.h>

int main() {
    int x = 10, five_times_x;
    printf("x:%d, five_times_x:%d\n", x, five_times_x);

    asm("lea (%0, %0, 4), %0"
        : "=r"(five_times_x)
        : "0"(x));

    printf("x:%d, five_times_x:%d\n", x, five_times_x);

    return 0;
}
// x:10, five_times_x:0
// x:10, five_times_x:50
```

上面例子中指定GCC始终使用在相同的寄存器来处理输入输出操作数。当然这时我们也不知道GCC具体使那个寄存器，如果需要的话我们也可以像这样指定一个:

```c
#include <stdio.h>

int main() {
    int x = 10;
    printf("x:%d\n", x);

    asm("leal (%%ecx,%%ecx,4), %%ecx"
        : "=c"(x)
        : "c"(x));

    printf("x:%d\n", x);

    return 0;
}
// x:10
// x:50
```

上面的三个例子中，我都没有在clobber list部分指定何寄存器。为什么？

前两个例子中，因为指定GCC自己选择合适的寄存器，并且GCC知道会改写什么。第三个例子中我们也没有必要把 `ecx` 放在clobber list中是因为GCC知道 `x` 将存入其中，GCC完全知道 `ecx` 的值。所以我们也不用写在clobber list中。

### Clobber List

**如果某个指令clobber(狠击，极大地打击) 了某个寄存器的值，我们就必须在 `asm` 中第三个冒号后的Clobber List中标示出该寄存器**。为的是通知GCC我们将使用和修改这些寄存器，所以 gcc 不会假设它加载到这些寄存器中的值是有效的。**输入、输出寄存器不用放Clobber List中**（看上面就是个例子），因为GCC能知道 `asm` 将使用这些寄存器。(因为它们已经显式被指定输入输出标出在输入输出部分) 。其他使用到的寄存器，无论是显示还是隐式的使用，必须在clobbered list中标明。

如果指令中以无法预料的形式修改了内存值，需要在clobbered list中加上 `”memory”`。从而使得GCC不去缓存在这些内存值。此外，如果要改变没有被列在输入和出部分的内存内容时，需要加上 `volatile` 关键字说明。clobbered list中列出的寄存器可以被多次读写。

来看一个内联汇编实现乘法的例子，这里内联汇编调用函数 `_foo`，并且接受存在 `eax` 和 `ecx` 值作为参数：

```c
asm( "movl %0,%%eax; movl %1,%%ecx; call _foo"
        : /*no outputs*/
        : "g" (from), "g" (to)
        : "eax", "ecx"
    );
```

### Volatile

如果你熟悉内核代码或者一些类似优秀的代码，你一定见过很多在 `asm` 或者 `__asm__` 后的函数声明前加了 `volatile` 或者 `__volatile__`。前面已经讨论了 `asm` 和 `__asm__` 的用途，那 `volatile` 有什么用途呢?

如果我们**要求汇编代码必须在被放置的位置执行**(例如不能被循环优化而移出循环)，我们就要在 `asm` 之后的 `()` 前，放一个 `volatile` 关键字。 这样**可以禁止这些代码被移动或删除**，像这样声明:

```c
asm volatile ( ... : ... : ... : ...);
```

同样，如果担心 `volatile` 有变量冲突，可以使用 `__volatile__` 关键字。

如果汇编代码只是做一些运算而没有什么附加影响的时候最好不要使用 `volatile` 修饰。不用 `volatile` 能给GCC留下优化代码的空间。

在“常用技巧”章节中的代码示例里有更多的关于 `volatile` 的使用详情。

## 五、constraints详解

你可能已经感到我们之前经常提到的constraint是个很重要的内容了。不过之前我们并没有过多的讨论。

constraint中可以指明一个操作数**是否在寄存器中**，**在哪个寄存器中**；可以**指明操作数是否是内存引用**，**如何寻址**；可以说明操作数是否是立即数常量，和其可能是的值（或值范围）。

### 常用constraints

虽然constraints有很多，但常用的并不多。下面我们就来看看这些常用的constraints。

#### 寄存器操作数constraints: `r`

如果操作数指定了这个constraints，操作数将被存储在通用寄存器中。看下面的例子:

```c
asm ("movl %%eax, %0\n" :"=r"(myval));
```

上面变量myval会被被保存在一个由GCC自己选择的寄存器中，eax中的值被拷贝到这个寄存器中去，并且在内存中的myval的值也会按这个寄存器值被更新。**当constraints `r` 被指定时，GCC可能会在任何一个可用的通用寄存器中保存这个值**。当然，你也可以指定具体使用那个寄存器，用下表所列出的constraints:

| r    | Register(s)     |
| ---- | --------------- |
| a    | %eax, %ax, %al  |
| b    | %ebx, %bx, %bl  |
| c    | %ecx, %cx, %cl  |
| d    | %edx, %dx, %adl |
| S    | %esi, %si       |
| D    | %edi, %di       |

#### 内存操作数constraint: `m`

当操作数在内存中时，任何对其操作会直接在内存中进行。与寄存器constraint不同的是：

- 指定寄存器constraint时，内存操作时先把值存在一个寄存器中，修改后再将该值写回到该内存中去。寄存器constraint通常只用于必要的汇编指令，或者用于能明显加快操作速度的情况
- 因为内存constraint能提升C语言变量更新效率，完全没必要通过一个寄存器来中转。

下面这个例子中，sidt的值会被直接存储到loc所指向的内存:

```c
asm("sidt %0\n" : :"m"(loc));
```

#### 匹配constraint

在某些情况下，一个变量可能被用来传递输入也用来保存输出。这种情况下我们需要用到匹配constraint。

```c
asm ("incl %0" :"=a"(var):"0"(var));
```

在之前章节中我们已经看过类似的例子。上面的例子中，`%eax` 被用来传递输入也用来保存输出。输入变量先被读入 `eax` 中，`incl` 执行之后，`%eax` 被更新并且保存到变量 `var` 中。这里的constraint `0` 就是指定使用和第一个输出相同的寄存器，即输入变量指定放在 `eax` 中。这种constraint可以使用在如下场景:

- 输入值从一个变量读入, 这个变量将被修改并且修改过的值要写回同一个变量；
- 没有必要把输入和输出操作数分开。

使用匹配constraint最重要的好处是可以**更高效地使用变量寄存器**。

### Some other constraints used are:

1. "m" : A memory operand is allowed, with any kind of address that the machine supports in general.
2. "o" : A memory operand is allowed, but only if the address is offsettable. ie, adding a small offset to the address gives a valid address.
3. "V" : A memory operand that is not offsettable. In other words, anything that would fit the `m’ constraint but not the `o’constraint.
4. "i" : An immediate integer operand (one with constant value) is allowed. This includes symbolic constants whose values will be known only at assembly time.
5. "n" : An immediate integer operand with a known numeric value is allowed. Many systems cannot support assembly-time constants for operands less than a word wide. Constraints for these operands should use ’n’ rather than ’i’.
6. "g" : Any register, memory or immediate integer operand is allowed, except for registers that are not general registers.

### Following constraints are x86 specific.

1. "r" : Register operand constraint, look table given above.
2. "q" : Registers a, b, c or d.
3. "I" : Constant in range 0 to 31 (for 32-bit shifts).
4. "J" : Constant in range 0 to 63 (for 64-bit shifts).
5. "K" : 0xff.
6. "L" : 0xffff.
7. "M" : 0, 1, 2, or 3 (shifts for lea instruction).
8. "N" : Constant in range 0 to 255 (for out instruction).
9. "f" : Floating point register
10. "t" : First (top of stack) floating point register
11. "u" : Second floating point register
12. "A" : Specifies the `a’ or `d’ registers. This is primarily useful for 64-bit integer values intended to be returned with the `d’ register holding the most significant bits and the `a’ register holding the least significant bits.

### constraint修饰符（Constraint Modifiers）

在使用constraint的时候，为了更精确的控制约束，GCC提供了一些修饰符，常用的修饰符有：

- “=” 指明这个操作数是只写的；之前保存在其中的值将被废弃而被输出值所代替
- “&” 指明这个操作事数是一个会在使用之前被修改的操作数，这个操作数将在输入指令用过输入操作数之前被修改。因此，该操作数不能被放在一个被用作输入操作数的寄存器或者内存处。只有在该操作数被写入之前完成输入指令的情况下，可以被绑定在该操作数上。

## 六、常用代码示例

到目前为止，GCC内联汇编基础知识就已经讲完了。接下来让我们通过一些简单的例子来巩固我们所学到到知识。内联汇编函数可以很方便的用宏的形式来编写，linux内核代码中有很多这样的实例(在`/usr/src/linux/asm/*.h`)。

### 1、两个数字相加

我们从一个简单的例子看起。我们来写一个把两个数字加起来的一个程序。

```c
#include <stdio.h>

int main(void) {
    int foo = 10, bar = 15;
    __asm__ __volatile__("addl %%ebx, %%eax"
                         : "=a"(foo)
                         : "a"(foo), "b"(bar));
    printf("foo+bar=%d\n", foo); // 25
    return 0;
}
```

在这里，我们坚持 GCC 将 `foo` 存储在 `%eax` 中，将 `bar` 存储在 `%ebx` 中，并且我们还希望将结果存储在 `%eax` 中。`=` 符号表示它是一个输出寄存器。现在我们可以用其他方法将整数添加到变量中。

```c
#include <stdio.h>

int main(void) {
    int my_var = 10, my_int = 15;
    __asm__ __volatile__("lock; addl %1,%0;"
                         : "=m"(my_var)
                         : "ir"(my_int), "m"(my_var)
                         : /* no clobber-list */
    );
    printf("my_var: %d\n", my_var);  // 25
    printf("my_int: %d\n", my_int);  // 15
    return 0;
}
```

这是原子性的 addition。我们可以移除指令“锁”来移除原子性。在 output 字段中，` =m` 表示 `my_var` 是一个输出，它在内存中。类似地，`ir` 表示，`my_int` 是一个整数，应该驻留在某个寄存器中(回想一下我们上面看到的表)。清单上没有记录。

### 2、加减

在我们将对一些寄存器/变量执行一些操作并比较值。

```c
#include <stdio.h>
#include <stdbool.h>

int main(void) {
    int my_var = 10;
    bool cond;
    __asm__ __volatile__("decl %0; sete %1;"
                         : "=m"(my_var), "=q"(cond)
                         : "m"(my_var)
                         : "memory");
    printf("my_var: %d\n", my_var);  // 9
    printf("cond: %d\n", cond);      // 0
    return 0;
}
```

这里，`my_var` 的值减1，如果结果值为0，则设置变量 cond。我们可以通过在汇编程序模板中添加指令 `lock;\n\t` 作为第一条指令来添加原子性。

类似地，我们可以使用 `incl% 0` 代替 `decl% 0`，以便增加 `my_var`。

需要注意的是:

1. `my_val` 是驻留在内存中的变量
2. `cond` 位于任何寄存器 `eax`、`ebx`、`ecx` 和 `edx` 中，约束 `= q` 保证了这一点。
3. 我们可以看到 memory 存在于清除列表中。也就是说，代码正在改变内存的内容。

### 3、设置/清除一个寄存器位

如何设置/清除一个寄存器位? 来看看下面这个技巧

```c
__asm__ __volatile__("btsl %1,%0"
                     : "=m"(ADDR)
                     : "Ir"(pos)
                     : "cc");
```

上面例子中变量 `ADDR`（一个内存变量）的 `pos` 位置值被设置成了1。我们可以使用 `btrl` 指令来清除由 `btsl` 设置的位。`pos` 变量的限定符constraint为 `Ir` 说明pos放在寄存器中，并且取值范围是0-31（I是一个x86相关constraint）。因此我们可以设置或者清除ADDR变量中从第0到第31位的值。因为这个操作涉会改变相关寄存器的内容，因此我们加上 `cc` 在clobberlist中。

### 4、字符串拷贝函数

现在我再来看一些更加复杂但是有用的函数。字符串拷贝函数：

```c
static inline char *strcpy(char *dest, const char *src) {
    int d0, d1, d2;
    __asm__ __volatile__(
        "1:\tlodsb\n\t"
        "stosb\n\t"
        "testb %%al,%%al\n\t"
        "jne 1b"
        : "=&S"(d0), "=&D"(d1), "=&a"(d2)
        : "0"(src), "1"(dest)
        : "memory");
    return dest;
}
```

上面代码的源地址存在 `esi` 寄存器中，目的地址存在 `EDI` 中。接着开始复制操作，直到遇到0结束。约束符constraint 为 `&S`,`&D`,`&a`，指定了使用的寄存器为 `esi`，`edi`和`eax`。很明显这些寄存器是clobber寄存器，因为它们的内容会在函数执行后被改变。此外我们也能看出为什么 `memory` 被放在clobber list中，因为`d0`, `d1`, `d2` 被更新了。

我们再来看一个类似的函数。该函数用来移动一块双字（double word）。注意这个函数是用宏来定义的。

```c
#define mov_blk(src, dest, numwords)         \
    __asm__ __volatile__(                    \
        "cld\n\t"                            \
        "rep\n\t"                            \
        "movsl"                              \
        :                                    \
        : "S"(src), "D"(dest), "c"(numwords) \
        : "%ecx", "%esi", "%edi")
```

该函数没有输出，但是块移动过程导致ecx, esi, edi内容被改变，所以我们必须把它们放在clobber list中。

### 5、系统调用实现

在Linux中，系统调用是用GCC内联汇编的形式实现的。让我们来看看一个系统调用是如何实现的。所有的系统调用都是用宏来写的 (在linux/unistd.h)。例如，一个带三个参数的系统调用的定义如下:

```c
#define _syscall3(type, name, type1, arg1, type2, arg2, type3, arg3)               \
    type name(type1 arg1, type2 arg2, type3 arg3) {                                \
        long __res;                                                                \
        __asm__ volatile("int $0x80"                                               \
                         : "=a"(__res)                                             \
                         : "0"(__NR_##name), "b"((long)(arg1)), "c"((long)(arg2)), \
                           "d"((long)(arg3)));                                     \
        __syscall_return(type, __res);                                             \
    }
```

所有带三个参数的系统调用都会用上面这个宏来执行。这段代码中，系统调用号放在eax中，参数分别放在ebx，ecx，edx中，最后用”int 0x80”执行系统调用。返回值放在eax中。

Linux中所有的系统调用都是用上面类似的方式实现的。比如Exit系统调用，它是带单个参数的系统调用。实现的代码如下:

```c
{
        asm("movl $1,%%eax;         /* SYS_exit is 1 */
             xorl %%ebx,%%ebx;      /* Argument is in ebx, it is 0 */
             int  $0x80"            /* Enter kernel mode */
             );
}
```

Exit的系统调用号是1，参数为0，所以我们把1放到eax中并且把0放到ebx中，最后通过调用int $0x80，exit(0)就被执行了。这就是exit函数的全部。

## 结束语

这篇文章讲述了GCC内联汇编的基础知识。一旦你理解了这些基础内容，自己再一步步的看下去就没有什么困难了。通过这些例子可以更好的帮助我们理解内联汇编的常用特性。

GCC内联汇编是一个很大的主题，这片文章的讨论还远远不够。本篇文章我们提到的大多数语法都可以在官方文档GNU Assembler中看到。完整的constraint也可以在GCC官方文档中找到。

Linux内核大范围内使用了GCC内联汇编，我们可以从中找到各种各样的例子来学习。这对我们也很有帮助。
