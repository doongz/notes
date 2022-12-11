# GNU make

官方文档：https://www.gnu.org/software/make/manual/make.html

中文文档：https://seisman.github.io/how-to-write-makefile/overview.html

参考：https://zhuanlan.zhihu.com/p/376493209

## 1. 简介

`make`(GNU make) 是一个项目构建工具，即方便地编译、链接多个源代码文件，自动决定哪些源文件需要重新编译，从而高效地构建自己地项目。本教程使用最广泛使用`make`的`.c`文件为例，但实际上`make`的使用并不限于 C 语言。

目标：

1. 根据多个源文件（示例为`.c`、`.h`文件），编译成多个中间文件（示例为`.o`文件）避免每次都重新编译，然后链接生成可执行文件;
2. 利用变量、通配符和函数处理源文件在不同文件夹下的情况，使得最终项目的构建依然十分方便、`Makefile`易于修改；
3. 适用于同时生成多个可执行文件的情况，避免每次要编译其他文件都得修改`Makefile`。

在官方文档 [GUN Make Manual](https://link.zhihu.com/?target=https%3A//www.gnu.org/software/make/manual/make.html) 中，没有满足 2、3 点的示例`Makefile`，因此本教程对于不想花太多时间看文档、只想快速根据示例`Makefile`构建自己项目的人来说很有必要。实际上，你也可以跳过此教程，直接使用示例项目中的 `Makefile` 作为自己项目的模板。

## 2. 示例项目

https://github.com/literaryno4/Makefile_tutorial

```
.
    ├── include                  # 本文件下包含构建目标文件所需的头文件
    │   ├── become_daemon.h
    │   ├── error_functions.h
    │   ├── get_num.h
    │   ├── inet_sockets.h
    │   └── tlpi_hdr.h
    ├── lib                      # 本文件夹下包含构建目标文件所需的库文件和依赖文件
    │   ├── become_daemon.c
    │   ├── ename.c.inc
    │   ├── error_functions.c
    │   ├── get_num.c
    │   └── inet_sockets.c
    └── src                      # 本文件夹包含项目的源文件、Makefile、目标文件以及可执行文件
        ├── obj
        │   ├── become_daemon.o
        │   ├── client.o
        │   ├── error_functions.o
        │   ├── get_num.o
        │   ├── inet_sockets.o
        │   └── server.o
        ├── Makefile
        ├── client
        ├── client.c
        ├── server
        └── server.c
```

## 3. 为什么使用 make

### 使用 gcc 原生命令

构建`client`或者`server`目标文件的思路是：

1、生成库文件和源文件的目标文件:

```shell
# 先运行 mkdir obj
gcc -c -o obj/error_functions.o ../lib/error_functions.c 
gcc -c -o obj/get_num.o ../lib/get_num.c 
gcc -c -o obj/inet_sockets.o ../lib/inet_sockets.c 
gcc -c -o obj/become_daemon.o ../lib/become_daemon.c 
gcc -c -o obj/client.o client.c 
gcc -c -o obj/server.o server.c
```

2、链接目标文件生成可执行文件：

```shell
gcc -o client obj/client.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 
gcc -o server obj/server.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o
```

可以看到，即使是这样一个很小的项目，每次构建都需要在命令行执行六次指令，即使使用键盘 ⬆️ ⬇️ 也要按️很多次，十分麻烦。这时候就需要`make`了。

### 使用 make

`make`执行`Makefile`指定的规则，`Makefile`一个规则的基本构成如下：

```makefile
target … : prerequisites …
	recipe
    …
    …
```

`:`前面指定要生成的文件(`target`)，后面是需要的依赖(`prerequisites`)，`recipe`指定行为规则，一般为编译或者链接，也可以是命令。`prerequisites` 和 `recipe`其中一个可以省略。

**`recipe` 前一定是 `tab`，不能是空格**

根据这样的规则，示例项目的`Makefile`最简单版本就呼之欲出了：

```makefile
# compile
obj/error_functions.o: ../lib/error_functions.c
	gcc -c -o obj/error_functions.o ../lib/error_functions.c 

obj/get_num.o: ../lib/get_num.c
	gcc -c -o obj/get_num.o ../lib/get_num.c 

obj/inet_sockets.o: ../lib/inet_sockets.c
	gcc -c -o obj/inet_sockets.o ../lib/inet_sockets.c 

obj/become_daemon.o: ../lib/become_daemon.c
	gcc -c -o obj/become_daemon.o ../lib/become_daemon.c 

obj/client.o: client.c
	gcc -c -o obj/client.o client.c 

obj/server.o: server.c
	gcc -c -o obj/server.o server.c 

# link
client: obj/client.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 
	gcc -o client obj/client.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 

server: obj/server.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 
	gcc -o server obj/server.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o

.PHONY: clean
clean:
	rm obj/*.o client server
```

以上共有 9 个规则，用空行分开，1-8 实际上就是生成的目标文件和可执行文件，第 9 条规则是清理所有生成文件的命令，`Makefile`需要根据`targets`指定需要执行哪些规则，默认先寻找内建的`all`规则执行，如果没有`all`就执行第一个规则。

最终要生成`client`和`server`文件，所以命令行输入：

```shell
mkdir obj
make client server
```

终端输出如下：

```shell
gcc -c -o obj/client.o client.c 
gcc -c -o obj/error_functions.o ../lib/error_functions.c 
gcc -c -o obj/get_num.o ../lib/get_num.c 
gcc -c -o obj/inet_sockets.o ../lib/inet_sockets.c 
gcc -c -o obj/become_daemon.o ../lib/become_daemon.c 
gcc -o client obj/client.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 
gcc -c -o obj/server.o server.c 
gcc -o server obj/server.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o
```

和上面手动输入`gcc`命令如出一辙，但是注意，我们并没有指定生成目标文件，`make`却也执行了生成目标文件的规则，这是因为`make`会根据规则的`prerequesites`自动搜索相应目录，如果没有依赖文件，就根据`Makefile`里面的规则生成。所以我们只需要指定最终的可执行文件。

清理所有生成的文件：

```shell
make clean
```

`.PHONY`表示`clean`不是一个文件而是一个命令的名字。

更方便的，也可以在`Makefile`内建的`all`规则中指定要执行的规则：

```makefile
all: client server

# compile
obj/error_functions.o: ../lib/error_functions.c
    gcc -c -o obj/error_functions.o ../lib/error_functions.c 

obj/get_num.o: ../lib/get_num.c
    gcc -c -o obj/get_num.o ../lib/get_num.c 

obj/inet_sockets.o: ../lib/inet_sockets.c
    gcc -c -o obj/inet_sockets.o ../lib/inet_sockets.c 

obj/become_daemon.o: ../lib/become_daemon.c
    gcc -c -o obj/become_daemon.o ../lib/become_daemon.c 

obj/client.o: client.c
    gcc -c -o obj/client.o client.c 

obj/server.o: server.c
    gcc -c -o obj/server.o server.c 

# link
client: obj/client.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 
    gcc -o client obj/client.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 

server: obj/server.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o 
    gcc -o server obj/server.o  obj/error_functions.o  obj/get_num.o  obj/inet_sockets.o  obj/become_daemon.o

.PHONY: clean
clean：
    rm obj/*.o client server
```

这样每次修改代码后重新构建项目只需终端执行：

```shell
make
```

这样就比每次手动输入编译命令方便多了。

## 4. 使用变量

上面的`Makefile`虽然已经够用了，但是还是过于冗余了，如果想生成新的目标文件或者可执行文件，必须手动添加规则，显得比较麻烦，且容易出错。同时可以发现，上面版本的规则比较重复。因此可以使用变量来使得`Makefile`更加简洁易于修改。

`Makefile`的变量类似于`shell`，所以把重复的字段换成变量就行了：

同时使用自动变量也可以大大简化`Makefile`，类似于下面这样：

```makefile
CC=gcc
ODIR=obj
IDIR=../include
LDIR=../lib
PROGRAM=client server

_DEPS = error_functions.o get_num.o inet_sockets.o become_daemon.o
DEPS = $(patsubst %, $(ODIR)/%,$(_DEPS))       # 这里使用了函数，具体之后会介绍

all: $(PROGRAM)

# compile
$(ODIR)/error_functions.o: $(LDIR)/error_functions.c
    $(CC) -c -o $@ $<

$(ODIR)/get_num.o: $(LDIR)/get_num.c
    $(CC) -c -o $@ $<

$(ODIR)/inet_sockets.o: $(LDIR)/inet_sockets.c
    $(CC) -c -o $@ $<

$(ODIR)/become_daemon.o: $(LDIR)/become_daemon.c
    $(CC) -c -o $@ $<

$(ODIR)/client.o: client.c
    $(CC) -c -o $@ $<

$(ODIR)/server.o: server.c
    $(CC) -c -o $@ $<

# link
client: $(ODIR)/client.o $(DEPS) 
    $(CC) -o $@ $^

server: $(ODIR)/server.o $(DEPS) 
    $(CC) -o $@ $^

.PHONY: clean
clean: 
    rm $(ODIR)/*.o $(PROGRAM)
```

这样使用变量过后，可以方便的更改所有规则，而不用逐条修改规则。上面的`recipe`中还使用了自动变量，他们的含义分别为：

- `$@`: 一般指规则的`target`部分，即`:`前面的部分。注意如果`target`有多个文件，那么`$@`指能让`recipe`运行的那些，逐个区分对待，这种情况后面会具体讲；
- `$<`: 第一个`prerequisite`;
- `$^`: 所有`prerequisite`

其他自动变量参见 GNU make 手册 [Automatic Variables](https://link.zhihu.com/?target=https%3A//www.gnu.org/software/make/manual/html_node/Automatic-Variables.html%23Automatic-Variables)。

## 5. 模式规则

使用变量过后的`Makefile` 看起来仍然有些重复冗余，特别是编译生成目标文件，每个规则都十分相似，有没有办法简化呢，使得就算之后要添加生成其他目标文件也不用直接添加规则？。答案是使用模式规则。

先看前四个规则：

```makefile
$(ODIR)/error_functions.o: $(LDIR)/error_functions.c
	$(CC) -c -o $@ $<

$(ODIR)/get_num.o: $(LDIR)/get_num.c
	$(CC) -c -o $@ $<

$(ODIR)/inet_sockets.o: $(LDIR)/inet_sockets.c
	$(CC) -c -o $@ $<

$(ODIR)/become_daemon.o: $(LDIR)/become_daemon.c
	$(CC) -c -o $@ $<
```

使用模式规则后为：

```makefile
$(ODIR)/%.o: $(LDIR)/%.c
	$(CC) -c -o $@ $<
```

也就是说`make`会根据链接所有需要的目标文件的名字，找到相应的`.c`源文件，从而进行编译。本项目为例，由于后面链接生成`client`和`server`都需要`$(ODIR)/`下的`error_functions.o、get_num.o、inet_sockets.o、become_daemon.o`目标文件，于是`make`就会在`$(LDIR)/`下找对应的`error_functions.c、get_num.c、inet_sockets.c、become_daemon.c`并根据`recipe`(`$(CC) -c -o $@ $<`)分别进行编译。

考虑到`client.c`、`server.c`两个源文件不在`$(LDIR)`下，所以分开写，即:

```makefile
$(ODIR)/client.o: client.c
	$(CC) -c -o $@ $<

$(ODIR)/server.o: server.c
	$(CC) -c -o $@ $<
```

改为：

```makefile
$(ODIR)/%.o: %.c
	$(CC) -c -o $@ $<
```

于是使用了模式规则的`Makefile`就可以简写为：

```makefile
CC=gcc
CFLAGS=-Wall -Wformat=0
ODIR=obj
IDIR=../include
LDIR=../lib
PROGRAM=client server

_DEPS = error_functions.o get_num.o inet_sockets.o become_daemon.o
DEPS = $(patsubst %, $(ODIR)/%,$(_DEPS))

all: $(PROGRAM)

# compile
$(ODIR)/%.o: $(LDIR)/%.c
	$(CC) -c -o $@ $<

$(ODIR)/%.o: %.c
	$(CC) -c -o $@ $<

# link
client: $(ODIR)/client.o $(DEPS) 
	$(CC) -o $@ $^

server: $(ODIR)/server.o $(DEPS) 
	$(CC) -o $@ $^

.PHONY: clean
clean: 
	rm $(ODIR)/*.o $(PROGRAM)
```

是不是一下就简洁了不少，而且最重要的是以后如果在`$(LDIR)`下添加了新的库文件，只需要在`_DEPS`变量后面添加相应的目标文件就可以了，而不需要再添加新的规则，这也是使用模式规则最大的优势了。

## 6. 使用函数

使用了模式规则的`Makefile`已经十分简化了，但在链接生成`client`和`server`两个可执行文件时为什么不也使用模式规则呢？像是这样：

```makefile
%: $(ODIR)%.o $(DEPS)
	%(CC) -o $@ $^
```

这是因为`make`无法直接从上面的规则中推断出要链接哪些文件。因此我们没办法像编译生成目标文件那样直接使用模式规则来简化链接过程了，这意味着如果之后每次想链接生成新的可执行文件，都要手动添加新的规则，十分不方便。

解决此问题的方法是使用`make`内建函数。

实际上，上面的`Makefile`中的`DEPS`变量就使用了`make`内建函数`patsubst`，它的作用是给`_DEPS`变量的每个元素（空格分开）添加`$(ODIR)/`前缀。`make`内建函数的语法为：

```makefile
$(function arguments)
```

参数之间用逗号隔开，所以`patsubst`函数的声明就是：

```makefile
$(patsubst pattern,replacement,text)
```

表示在`text`根据`pattern`并用`replacement`替换之。

而想要简化链接规则使不管要生成多少个可执行文件，都仅需要一个规则，且不需要每次都修改，可以使用`patsubst`和`addsuffix`函数实现，即：

```makefile
client: $(ODIR)/client.o $(DEPS) 
	$(CC) -o $@ $^

server: $(ODIR)/server.o $(DEPS) 
	$(CC) -o $@ $^
```

简化为：

```makefile
$(PROGRAM): $(patsubst %, $(ODIR)/%,$(addsuffix .o,$(PROGRAM))) $(DEPS)
	$(CC) -o $@ $(ODIR)/$@.o $(DEPS)
```

`addsuffix`函数表示给`$(PROGRAM)`每个元素添加`.o`后缀。这里还用到了前面讲的`$@`变量，当`$(PROGRAM)`含义多个元素时，它表示每个能让`recipe`执行的元素。这里`client`、`server`都能使`recipe`链接，于是分别执行链接两次。

也就是说以后如果还想链接生成其他可执行文件，比如`client2`，不需要添加任何新的规则，只需要在`Makefile`头部`$(PROGRAM)`变量定义处添加`client2`（即`PROGRAM=client server clien2`）就 OK 了。

于是我们的`Makefile`就进一步简化成了如下形式：

```makefile
CC=gcc
CFLAGS=-Wall -Wformat=0
ODIR=obj
IDIR=../include
LDIR=../lib
PROGRAM=client server

_DEPS = error_functions.o get_num.o inet_sockets.o become_daemon.o
DEPS = $(patsubst %, $(ODIR)/%,$(_DEPS))

all: $(PROGRAM)

# compile
$(ODIR)/%.o: $(LDIR)/%.c
	$(CC) -c -o $@ $<

$(ODIR)/%.o: %.c
	$(CC) -c -o $@ $<

# link
$(PROGRAM): $(patsubst %, $(ODIR)/%,$(addsuffix .o,$(PROGRAM))) $(DEPS)
	$(CC) -o $@ $(ODIR)/$@.o $(DEPS) 

.PHONY: clean
clean: 
	rm $(ODIR)/*.o $(PROGRAM)
```

## 7. 总结

可以看到，使用`make`之后可以极大的简化我们编译构建含有多个源文件的项目，从而让我们更加地专注编写代码本身。关于`make`还有很多没讲到的地方，但是于我而言已经十分简单方便了，如果还有其他功能的需要，可以继续参考官方手册 [GNU Make Manual](https://link.zhihu.com/?target=https%3A//www.gnu.org/software/make/manual/make.html)。

同时再推荐一个`make`更简单的教程：[A Simple Makefile Tutorial](https://link.zhihu.com/?target=https%3A//www.cs.colby.edu/maxwell/courses/tutorials/maketutor/)。

## 8. 常见报错

Makefile:3: * missing separator. Stop.

这个是由于空格和TAB捣鬼的，Makefile文件规定命令都是以TAB开头的，但是有的地方复制过来的内容中的TAB被替换成了空格，所以会导致这个问题，解决办法就是把所有命令前的空格改成TAB

.... -> tab