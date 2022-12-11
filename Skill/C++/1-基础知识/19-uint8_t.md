# uint8_t / uint16_t / uint32_t /uint64_t

来源：https://blog.csdn.net/Mary19920410/article/details/71518130

来源：https://blog.csdn.net/weixin_44942126/article/details/115014754

一、C语言基本数据类型回顾

在C语言中有6种基本数据类型：short、int、long、float、double、char

1、数值类型

1）整型：short、int、long

2）浮点型：float、double

2、字符类型：char

二、typedef回顾

typedef用来定义关键字或标识符的别名，例如：

```c
typedef double wages;
typedef wages salary;
```

三、uint[]_t

uint8_t / uint16_t / uint32_t /uint64_t

1、这些类型的来源：这些数据类型中都带有_t, _t 表示这些数据类型是通过typedef定义的，而不是新的数据类型。也就是说，它们其实是我们已知的类型的别名。

2、使用这些类型的原因：方便代码的维护。比如，在C中没有bool型，于是在一个软件中，一个程序员使用int，一个程序员使用short，会比较混乱。最好用一个typedef来定义一个统一的bool：

```
typedef char bool;
```

在涉及到跨平台时，不同的平台会有不同的字长，所以利用预编译和typedef可以方便的维护代码。

3、这些类型的定义：

在C99标准中定义了这些数据类型，具体定义在：/usr/include/stdint.h      ISO C99: 7.18 Integer types

```c
#ifndef __int8_t_defined  
# define __int8_t_defined  
typedef signed char             int8_t;   
typedef short int               int16_t;  
typedef int                     int32_t;  
# if __WORDSIZE == 64  
typedef long int                int64_t;  
# else  
__extension__  
typedef long long int           int64_t;  
# endif  
#endif  
  
  
typedef unsigned char           uint8_t;  
typedef unsigned short int      uint16_t;  
#ifndef __uint32_t_defined  
typedef unsigned int            uint32_t;  
# define __uint32_t_defined  
#endif  
#if __WORDSIZE == 64  
typedef unsigned long int       uint64_t;  
#else  
__extension__  
typedef unsigned long long int  uint64_t;  
#endif  
```

4、格式化输出：

```cpp
uint16_t %hu
uint32_t %u
uint64_t %llu
```

5 、uint8_t类型的输出：

注意uint8_t的定义为

```c
typedef unsigned char           uint8_t;
```

uint8_t实际上是一个char。所以输出uint8_t类型的变量实际上输出其对应的字符，而不是数值。例：

```c
uint8_t num = 67;
cout << num << endl;
```

输出结果：C

# FP32、FP16和INT8

1、定义

FP32（Full Precise Float 32，单精度）占用4个字节，共32位，其中1位为符号位，8为指数位，23为尾数位。

FP16（float，半精度）占用2个字节，共16位，其中1位为符号位，5位指数位，十位有效数字位。与FP32相比，FP16的访存消耗仅为1/2，也因此FP16是更适合在移动终端侧进行AI计算的数据格式。

INT8，八位整型占用1个字节，INT8是一种定点计算方式，代表整数运算，一般是由浮点运算量化而来。在二进制中一个“0”或者“1”为一bit，INT8则意味着用8bit来表示一个数字。因此，虽然INT8比FP16精度低，但是数据量小、能耗低，计算速度相对更快，更符合端侧运算的特点。

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210426181444527.png)

|      | Dynamic Range               | Minimum Positive Value |
| ---- | --------------------------- | ---------------------- |
| FP32 | -3.4 x 10^38 ~ +3.4 x 10^38 | 1.4 x 10^(-45)         |
| FP16 | -65504 ~ +65504             | 5.96 x 10^(-8)         |
| INT8 | -128 ~ +127                 | 1                      |

2、比较

低精度技术 (high speed reduced precision)。在training阶段，梯度的更新往往是很微小的，需要相对较高的精度，一般要用到FP32以上。在inference的时候，精度要求没有那么高，一般F16（半精度）就可以，甚至可以用INT8（8位整型），精度影响不会很大。同时低精度的模型占用空间更小了，有利于部署在嵌入式模型里面。

利用fp16 代替 fp32

优点：

1）TensorRT的FP16与FP32相比能有接近一倍的速度提升，前提是GPU支持FP16（如最新的2070,2080,2080ti等）

2）减少显存。

缺点：

1） 会造成溢出

3、测试

我用Jetson Xavier NX测试了基于TensorRT加速的yolo算法在FP32、FP16、INT8三种精度下的数据:

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210426210222511.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NDk0MjEyNg==,size_16,color_FFFFFF,t_70)