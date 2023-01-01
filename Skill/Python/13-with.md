# Python 中 with 用法详解

来源：https://blog.csdn.net/freeking101/article/details/109615618

## 由来 

with…as 是 python 的控制流语句，像 if ，while一样。with…as 语句是简化版的 try except finally语句。

先理解一下 try…except…finally 语句是干啥的。实际上 try…except 语句和 try…finally 语句是两种语句，用于不同的场景。但是当二者结合在一起时，可以“实现稳定性和灵活性更好的设计”。

### 1. try…except 语句

用于处理程序执行过程中的异常情况，比如语法错误、从未定义变量上取值等等，也就是一些python程序本身引发的异常、报错。比如你在python下面输入 1 / 0：

```
>>> 1/0
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

系统会给你一个 ZeroDivisionError 的报错。说白了就是为了防止一些报错影响你的程序继续运行，就用try语句把它们抓出来(捕获)。

**try…except 的标准格式：**

```python
try:  
    ## normal block  
except A:  
    ## exc A block  
except:  
    ## exc other block  
else:  
    ## noError block  
```

**程序执行流程是：**

```python
–>执行normal block
–>发现有A错误，执行 exc A block(即处理异常)
–>结束
 
如果没有A错误呢？
–>执行normal block
–>发现B错误，开始寻找匹配B的异常处理方法，发现A，跳过，发现except others(即except:)，执行exc other block
–>结束
 
如果没有错误呢？
–>执行normal block
–>全程没有错误，跳入else 执行noError block
–>结束
```

Tips: 我们发现，一旦跳入了某条except语句，就会执行相应的异常处理方法(block)，执行完毕就会结束。不会再返回try的normal block继续执行了。

结果是，先打出了一个0，又打出了一个Error。就是把ZeroDivisionError错误捕获了。

先执行 try 后面这一堆语句，由上至下：

- step1: a 正常，打印a. 于是打印出0.5 (python3.x以后都输出浮点数)
- step2: b, 不正常了，0 不能做除数，所以这是一个错误。直接跳到except报错去。于是打印了Error。
- step3: 其实没有step3，因为程序结束了。c是在错误发生之后的b语句后才出现，根本轮不到执行它。也就看不到打印出的c了

但这还不是 try/except 的所有用法

except后面还能跟表达式的!

所谓的表达式，就是错误的定义。也就是说，我们可以捕捉一些我们想要捕捉的异常。而不是什么异常都报出来。

**异常分为两类：**

- python标准异常
- 自定义异常

我们先抛开自定义异常(因为涉及到类的概念)，看看 except 都能捕捉到哪些 python 标准异常。请查看[菜鸟笔记](http://www.runoob.com/python/python-exceptions.html)

https://www.runoob.com/python/python-exceptions.html

### 2. try…finallly 语句

用于无论执行过程中有没有异常，都要执行清场工作。

```python
try:  
    execution block  ##正常执行模块  
except A:  
    exc A block ##发生A错误时执行  
except B:  
    exc B block ##发生B错误时执行  
except:  
    other block ##发生除了A,B错误以外的其他错误时执行  
else:  
    if no exception, jump to here ##没有错误时执行  
finally:  
    final block  ##总是执行  
```

**tips:** 注意顺序不能乱，否则会有语法错误。如果用 else 就必须有 except，否则会有语法错误。

```c++
try:
    a = 1 / 2
    print(a)
    print(m)  # 抛出 NameError异常, 此后的语句都不在执行
    b = 1 / 0
    print(b)
    c = 2 / 1
    print(c)
except NameError:
    print("Ops!!")  # 捕获到异常
except ZeroDivisionError:
    print("Wrong math!!")
except:
    print("Error")
else:
    print("No error! yeah!")
finally:  # 是否异常都执行该代码块
    print("Successfully!")
```

## 1. with 语句的原理

- 上下文管理协议（Context Management Protocol）：包含方法 **__enter__()** 和 **__exit__()**，支持该协议的对象要实现这两个方法。
- 上下文管理器（Context Manager）：支持上下文管理协议的对象，这种对象实现了 __enter__() 和 __exit__() 方法。上下文管理器定义执行 with 语句时要建立的运行时上下文，负责执行 with 语句块上下文中的进入与退出操作。通常使用 with 语句调用上下文管理器，也可以通过直接调用其方法来使用。

说完上面两个概念，我们再从 with 语句的常用表达式入手，一段基本的 with 表达式，其结构是这样的：

```python
with context_expression [as target(s)]:
    ...
    with-body
    ...
```

其中 context_expression 可以是任意表达式；as target(s) 是可选的。

with 语句执行过程 。在语义上等价于:

```python
    context_manager = context_expression
    exit = type(context_manager).__exit__
    value = type(context_manager).__enter__(context_manager)
    exc = True   # True 表示正常执行，即便有异常也忽略；False 表示重新抛出异常，需要对异常进行处理
    try:
        try:
            target = value  # 如果使用了 as 子句
            with-body     # 执行 with-body
        except:
            # 执行过程中有异常发生
            exc = False
            # 如果 __exit__ 返回 True，则异常被忽略；如果返回 False，则重新抛出异常
            # 由外层代码对异常进行处理
            if not exit(context_manager, *sys.exc_info()):
                raise
    finally:
        # 正常退出，或者通过 statement-body 中的 break/continue/return 语句退出
        # 或者忽略异常退出
        if exc:
            exit(context_manager, None, None, None)
        # 缺省返回 None，None 在布尔上下文中看做是 False
```

可以看到，with 和 try finally 有下面的等价流程：

```python
try:  
    执行 __enter__的内容  
    执行 with_block.  
finally:  
    执行 __exit__内容  
```


执行 **context_expression** ，生成上下文管理器 **context_manager**

调用上下文管理器的 **__enter__()** 方法；如果使用了 as 子句，则将 **__enter__()** 方法的 **返回值** 赋值给 as 子句中的 target(s)

执行语句体 with-body

不管执行过程中是否发生了异常，执行上下文管理器的 **__exit__()** 方法，**__exit__()** 方法负责执行 "清理" 工作，如释放资源等。如果执行过程中没有出现异常，或者语句体中执行了语句 break/continue/return，则以 None 作为参数调用 **__exit__**(None, None, None) ；如果执行过程中出现异常，则使用 sys.exc*info 得到的异常信息为参数调用* **__exit__**(exc_type, exc_value, exc_traceback)

出现异常时，如果 **__exit__**(type, value, traceback) 返回 False，则会重新抛出异常，让 with 之外的语句逻辑来处理异常，这也是通用做法；如果返回 True，则忽略异常，不再对异常进行处理

那么`__enter__`和`__exit__`是怎么用的方法呢？我们直接来看一个栗子好了。

### 程序无错的例子

```python
class Sample(object):             # object类是所有类最终都会继承的类
    def __enter__(self):          # 类中函数第一个参数始终是self，表示创建的实例本身
        print("In __enter__()")
        return "Foo"
 
    def __exit__(self, type, value, trace):
        print("In __exit__()")
 
 
def get_sample():
    return Sample()
 
 
with get_sample() as sample:
    print("sample:", sample)
 
 
print(Sample)    # 这个表示类本身   <class '__main__.Sample'>
print(Sample())  # 这表示创建了一个匿名实例对象 <__main__.Sample object at 0x00000259369CF550>
 
'''
In __enter__()
sample: Foo
In __exit__()
<class '__main__.Sample'>
<__main__.Sample object at 0x00000226EC5AF550>
'''
```

**步骤分析:**

–> 调用`get_sample()`函数，返回`Sample`类的实例;
–> 执行`Sample`类中的`__enter__()`方法，打印`"In__enter_()"`字符串，并将字符串`“Foo”`赋值给as后面的sample变量;
–> 执行`with-block`码块，即打印`"sample: %s"`字符串，结果为`"sample: Foo"`
–> 执行`with-block`码块结束，返回`Sample`类，执行类方法`__exit__()`。因为在执行with-block码块时并没有错误返回，所以type,value,trace这三个arguments都没有值。直接打印`"In__exit__()"`

### 程序有错的例子

```python
class Sample:
    def __enter__(self):
        return self
 
    def __exit__(self, type, value, trace):
        print("type:", type)
        print("value:", value)
        print("trace:", trace)
 
    def do_something(self):
        bar = 1 / 0
        return bar + 10
 
 
with Sample() as sample:
    sample.do_something()
 
'''
type: <class 'ZeroDivisionError'>
value: division by zero
trace: <traceback object at 0x0000019B73153848>
Traceback (most recent call last):
  File "F:/机器学习/生物信息学/Code/first/hir.py", line 16, in <module>
    sample.do_something()
  File "F:/机器学习/生物信息学/Code/first/hir.py", line 11, in do_something
    bar = 1 / 0
ZeroDivisionError: division by zero
'''
```

**步骤分析:**

–> 实例化`Sample`类，执行类方法`__enter__()`，返回值`self`也就是实例自己赋值给`sample`。即`sample`是`Sample`的一个实例(对象);
–>执行`with-block`码块: 实例`sample`调用方法`do_something()`;
–>执行`do_something()`第一行 `bar = 1 / 0`，发现`ZeroDivisionError`，直接结束`with-block`代码块运行
–>执行类方法`__exit__()`，带入`ZeroDivisionError`的错误信息值，也就是`type`,`value`, `trace`，并打印它们。



如果有多个项目，则会视作存在多个 [`with`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#with) 语句嵌套来处理多个上下文管理器: （ https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-with-statement ）

```python
with A() as a, B() as b:
    SUITE
在语义上等价于:
with A() as a:
    with B() as b:
        SUITE
```

在 3.1 版更改: 支持多个上下文表达式。

参见：[**PEP 343**](https://www.python.org/dev/peps/pep-0343) - "with" 语句。Python [`with`](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#with) 语句的规范描述、背景和示例。

## 2. 自定义上下文管理器

开发人员可以自定义支持上下文管理协议的类。自定义的上下文管理器要实现上下文管理协议所需要的 **enter**() 和 **exit**() 两个方法：

- `contextmanager.__enter__()` ：进入上下文管理器的运行时上下文，在语句体执行前调用。with 语句将该方法的返回值赋值给 as 子句中的 target，如果指定了 as 子句的话
- `**contextmanager.__exit__(exc_type, exc_value, exc_traceback`：退出与上下文管理器相关的运行时上下文，返回一个布尔值表示是否对发生的异常进行处理。参数表示引起退出操作的异常，如果退出时没有发生异常，则3个参数都为None。如果发生异常时，返回True 表示不处理异常，否则会在退出该方法后重新抛出异常以由 with 语句之外的代码逻辑进行处理。如果该方法内部产生异常，则会取代由 statement-body 中语句产生的异常。要处理异常时，不要显示重新抛出异常，即不能重新抛出通过参数传递进来的异常，只需要将返回值设置为 False 就可以了。之后，上下文管理代码会检测是否 `__exit__()` 失败来处理异常

下面通过一个简单的示例来演示如何构建自定义的上下文管理器。

注意，上下文管理器必须同时提供 `__enter__()` 和 `__exit__()` 方法的定义，缺少任何一个都会导致 AttributeError；with 语句会先检查是否提供了 `__exit__()` 方法，然后检查是否定义了 `__enter__()` 方法。

```python
# coding = utf-8
 
 
class DBManager(object):
    def __init__(self):
        pass
 
    def __enter__(self):
        print('__enter__')
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__')
        return True
 
def getInstance():
        return DBManager()
 
with getInstance() as dbManagerIns:
    print('with demo')
 
 
'''
运行结果:
__enter__
with demo
__exit__
'''
```

**with 后面必须跟一个上下文管理器，如果使用了 as，则是把上下文管理器的 `__enter__()` 方法的返回值赋值给 target，target 可以是单个变量，或者由 "()" 括起来的元组（不能是仅仅由 "," 分隔的变量列表，必须加 "()"）**

结果分析：当我们使用 with 的时候，`__enter__` 方法被调用，并且将返回值赋值给 as 后面的变量，并且在退出 with 的时候自动执行 `__exit__` 方法

```python
class With_work(object):
    def __enter__(self):
        """进入with语句的时候被调用"""
        print('enter called')
        return "xxt"
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开with的时候被with调用"""
        print('exit called')
 
 
with With_work() as as_f:
    print(f'as_f : {as_f}')
    print('hello with')
 
 
'''
enter called
as_f : xxt
hello with
exit called
'''
```

示例 2：

自定义支持 with 语句的对象 

```python
class DummyResource:
    def __init__(self, tag):
        self.tag = tag
        print(f'Resource [{tag}]')
 
    def __enter__(self):
        print(f'[Enter {self.tag}]: Allocate resource.')
        return self  # 可以返回不同的对象
 
    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        :param exc_type: 错误的类型
        :param exc_value: 错误类型对应的值 
        :param exc_tb: 代码中错误发生的位置 
        :return:
        """
        print(f'[Exit {self.tag}]: Free resource.')
        if exc_tb is None:
            print(f'[Exit {self.tag}]: Exited without exception.')
        else:
            print(f'[Exit {self.tag}]: Exited with exception raised.')
            return False  # 可以省略，缺省的None也是被看做是False
 
 
# 第一个 with 语句
num = 50
print('*' * num)
with DummyResource('First'):
    print('[with-body] Run without exceptions.')
print('*' * num)
 
# 第二个 with 语句
print('*' * num)
with DummyResource('second'):
    print('[with-body] Run with exception.')
    raise Exception
    print('[with-body] Run with exception. Failed to finish statement-body!')
print('*' * num)
 
# 嵌套 with 语句
print('*' * num)
with DummyResource('Normal'):
    print('[with-body] Run without exceptions.')
 
    with DummyResource('With-Exception'):
        print('[with-body] Run with exception.')
        raise Exception
        print('[with-body] Run with exception. Failed to finish statement-body!')
print('*' * num)
```

DummyResource 中的 `__enter__()` 返回的是自身的引用，这个引用可以赋值给 as 子句中的 target 变量；返回值的类型可以根据实际需要设置为不同的类型，不必是上下文管理器对象本身。

`__exit__()` 方法中对变量 exctb 进行检测，如果不为 None，表示发生了异常，返回 False 表示需要由外部代码逻辑对异常进行处理；注意到如果没有发生异常，缺省的返回值为 None，在布尔环境中也是被看做 False，但是由于没有异常发生，`__exit__()` 的三个参数都为 None，上下文管理代码可以检测这种情况，做正常处理。

执行结果：

```
**************************************************
Resource [First]
[Enter First]: Allocate resource.
[with-body] Run without exceptions.
[Exit First]: Free resource.
[Exit First]: Exited without exception.
**************************************************
**************************************************
Resource [second]
[Enter second]: Allocate resource.
[with-body] Run with exception.
[Exit second]: Free resource.
[Exit second]: Exited with exception raised.
Traceback (most recent call last):
  File "temp.py", line 30, in <module>
    raise Exception
Exception
```

第1个 with 语句执行结果：可以看到，正常执行时会先执行完语句体 with-body，然后执行 **__exit__**() 方法释放资源。

第2个 with 语句的执行结果：可以看到，with-body 中发生异常时with-body 并没有执行完，但资源会保证被释放掉，同时产生的异常由 with 语句之外的代码逻辑来捕获处理。

因为第2个with语句发生异常，所以 嵌套 with 语句没有执行。。。

## 3. 自动关闭文件 

我们都知道打开文件有两种方法:

- f = open()
- with open() as f:

这两种方法的区别就是第一种方法需要我们自己关闭文件；f.close()，而第二种方法不需要我们自己关闭文件，无论是否出现异常，with都会自动帮助我们关闭文件，这是为什么呢？

我们先自定义一个类，用with来打开它：

```python
class Foo(object):
    def __enter__(self):
        print("enter called")
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit called")
        print("exc_type :%s" % exc_type)
        print("exc_val :%s" % exc_val)
        print("exc_tb :%s" % exc_tb)
 
 
with Foo() as foo:
    print("hello python")
    a = 1 / 0
    print("hello end")
 
 
'''
enter called
Traceback (most recent call last):
hello python
exit called
exc_type :<class 'ZeroDivisionError'>
exc_val :division by zero
 File "F:/workspaces/python_workspaces/flask_study/with.py", line 25, in <module>
  a = 1/0
exc_tb :<traceback object at 0x0000023C4EDBB9C8>
ZeroDivisionError: division by zero
 
Process finished with exit code 1
'''
```

执行结果的输入顺序，分析如下：

当我们 with Foo() as foo: 时，此时会执行 __enter__方法，然后进入执行体，也就是：

```python
print("hello python")
a = 1/0
print("hello end")
```

语句，但是在 a=1/0 出现了异常，with将会中止，此时就执行__exit__方法，就算不出现异常，当执行体被执行完毕之后，__exit__方法仍然被执行一次。

我们回到 with open("file")as f: 不用关闭文件的原因就是在 __exit__ 方法中，存在关闭文件的操作，所以不用我们手工关闭文件，with已将为我们做好了这个操作，这就可以理解了。

## 4. contextlib 模块

contextlib --- 为 with语句上下文提供的工具：https://docs.python.org/zh-cn/3/library/contextlib.html#contextlib.asynccontextmanager

contextlib 模块提供了3个对象，使用这些对象，可以对已有的生成器函数或者对象进行包装，加入对上下文管理协议的支持，避免了专门编写上下文管理器来支持 with 语句。

- 装饰器 contextmanager
- 函数 nested 
- 上下文管理器 closing

### 装饰器 contextmanager

contextmanager 用于对生成器函数进行装饰，生成器函数被装饰以后，返回的是一个上下文管理器，其 `__enter__()` 和 `__exit__()` 方法由 contextmanager 负责提供，而不再是之前的迭代子。被装饰的生成器函数只能产生一个值，否则会导致异常 RuntimeError；产生的值会赋值给 as 子句中的 target，如果使用了 as 子句的话。下面看一个简单的例子。

```python
from contextlib import contextmanager
 
 
@contextmanager
def demo():
    print('[Allocate resources]')
    print('Code before yield-statement executes in __enter__')
    yield '*** contextmanager demo ***'
    print('Code after yield-statement executes in __exit__')
    print('[Free resources]')
 
 
with demo() as value:
    print(f'Assigned Value: {value}')
 
'''
[Allocate resources]
Code before yield-statement executes in __enter__
Assigned Value: *** contextmanager demo ***
Code after yield-statement executes in __exit__
[Free resources]
'''
```

可以看到，生成器函数中 yield 之前的语句在 **enter**() 方法中执行，yield 之后的语句在 **exit**() 中执行，而 yield 产生的值赋给了 as 子句中的 value 变量。

需要注意的是，contextmanager 只是省略了 **enter**() / **exit**() 的编写，但并不负责实现资源的”获取”和”清理”工作；”获取”操作需要定义在 yield 语句之前，”清理”操作需要定义 yield 语句之后，这样 with 语句在执行 **enter**() / **exit**() 方法时会执行这些语句以获取/释放资源，即生成器函数中需要实现必要的逻辑控制，包括资源访问出现错误时抛出适当的异常。

### 函数 nested

nested 可以将多个上下文管理器组织在一起，避免使用嵌套 with 语句。

```python
nested 语法
 
with nested(A(), B(), C()) as (X, Y, Z):
    # with-body code here
类似于：
with A() as X:
    with B() as Y:
        with C() as Z:
            # with-body code here
需要注意的是，发生异常后，如果某个上下文管理器的 exit() 方法对异常处理返回 False，
则更外层的上下文管理器不会监测到异常。
```

### 上下文管理器 closing

closing 的实现如下

```python
class closing(object):
    # help doc here
    def __init__(self, thing):
        self.thing = thing
 
    def __enter__(self):
        return self.thing
 
    def __exit__(self, *exc_info):
        self.thing.close()
```

上下文管理器会将包装的对象赋值给 as 子句的 target 变量，同时保证打开的对象在 with-body 执行完后会关闭掉。closing 上下文管理器包装起来的对象必须提供 close() 方法的定义，否则执行时会报 AttributeError 错误。

自定义支持 closing 的对象

```python
from contextlib import closing
 
 
class ClosingDemo(object):
    def __init__(self):
        self.acquire()
 
    def acquire(self):
        print('Acquire resources.')
 
    def free(self):
        print('Clean up any resources acquired.')
 
    def close(self):
        self.free()
 
 
with closing(ClosingDemo()):
    print('Using resources')
 
'''
Acquire resources.
Using resources
Clean up any resources acquired.
'''
```

closing 适用于提供了 close() 实现的对象，比如网络连接、数据库连接等，也可以在自定义类时通过接口 close() 来执行所需要的资源”清理”工作。

## 5. 总结

with 是对 try…expect…finally 语法的一种简化，并且提供了对于异常非常好的处理方式。在Python有2种方式来实现 with 语法：class-based 和 decorator-based，2种方式在原理上是等价的，可以根据具体场景自己选择。

with 最初起源于一种block…as…的语法，但是这种语法被很多人所唾弃，最后诞生了with，关于这段历史依然可以去参考PEP-343和PEP-340

with 主要用在：自定义上下文管理器来对软件系统中的资源进行管理，比如数据库连接、共享资源的访问控制等。文件操作。进程线程之间互斥对象。支持上下文其他对象