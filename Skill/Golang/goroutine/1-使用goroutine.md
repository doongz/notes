# goroutine

参考1：[Go语言并发](http://c.biancheng.net/golang/concurrent/)

goroutine 是 Go语言中的轻量级线程实现，由 Go 运行时（runtime）管理。Go 程序会智能地将 goroutine 中的任务合理地分配给每个 CPU。

Go 程序从 main 包的 main() 函数开始，在程序启动时，Go 程序就会为 main() 函数创建一个默认的 goroutine。

## 一、基础使用

### 1、使用普通函数创建 goroutine

Go 程序中使用 **go** 关键字为一个函数创建一个 goroutine。一个函数可以被创建多个 goroutine，一个 goroutine 必定对应一个函数。

```go
go 函数名( 参数列表 )
```

使用 go 关键字创建 goroutine 时，被调用函数的返回值会被忽略。

如果需要在 goroutine 中返回数据，请使用后面介绍的通道（channel）特性，通过通道把数据从 goroutine 中作为返回值传出。

```go
package main

import (
	"fmt"
	"time"
)

func running() {
	var times int
	for { // 构建一个无限循环
		times++ // 延时1秒
		fmt.Println("tick", times)
		time.Sleep(time.Second)
	}
}
func main() {
	// 并发执行程序
	go running()
	// 接受命令行输入, 不做任何事情
	var input string
	fmt.Scanln(&input)
}
```

### 2、使用匿名函数创建goroutine

go 关键字后也可以为匿名函数或闭包启动 goroutine

使用匿名函数或闭包创建 goroutine 时，除了将函数定义部分写在 go 的后面之外，还需要加上匿名函数的调用参数，格式如下：

```go
go func( 参数列表 ){
    函数体
}( 调用参数列表 )
```

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	go func() {
		var times int
		for {
			times++
			fmt.Println("tick", times)
			time.Sleep(time.Second)
		}
	}()
	var input string
	fmt.Scanln(&input)
}
```

### 3、GOMAXPROCS

在 Go语言程序运行时（runtime）实现了一个小型的任务调度器。这套调度器的工作原理类似于操作系统调度线程，Go 程序调度器可以高效地将 CPU 资源分配给每一个任务。传统逻辑中，开发者需要维护线程池中线程与 CPU 核心数量的对应关系。同样的，Go 地中也可以通过 runtime.GOMAXPROCS() 函数做到，格式为：

```go
runtime.GOMAXPROCS(逻辑CPU数量)
```

这里的逻辑CPU数量可以有如下几种数值：

- <1：不修改任何数值
- =1：单核心执行
- \>1：多核并发执行

一般情况下，可以使用 runtime.NumCPU() 查询 CPU 数量，并使用 runtime.GOMAXPROCS() 函数进行设置，例如：

```go
runtime.GOMAXPROCS(runtime.NumCPU())
```

GOMAXPROCS 同时也是一个环境变量，在应用程序启动前设置环境变量也可以起到相同的作用。

## 二、go语言通道 chan

如果说 goroutine 是 Go语言程序的并发体的话，那么 channels 就是它们之间的通信机制。一个 channels 是一个通信机制，它可以让一个 goroutine 通过它给另一个 goroutine 发送值信息。每个 channel 都有一个特殊的类型，也就是 channels 可发送数据的类型。一个可以发送 int 类型数据的 channel 一般写为 chan int。

Go语言提倡使用通信的方法代替共享内存，当一个资源需要在 goroutine 之间共享时，通道在 goroutine 之间架起了一个管道，并提供了确保同步交换数据的机制。声明通道时，需要指定将要被共享的数据的类型。可以通过通道共享内置类型、命名类型、结构类型和引用类型的值或者指针。

- Go语言中的通道（channel）是一种特殊的类型。在任何时候，同时只能有一个 goroutine 访问通道进行发送和获取数据。goroutine 间通过通道就可以通信。
- 通道像一个传送带或者队列，总是遵循先入先出（First In First Out）的规则，保证收发数据的顺序。

### 1、声明通道类型

通道本身需要一个类型进行修饰，就像切片类型需要标识元素类型。通道的元素类型就是在其内部传输的数据类型，声明如下：

```go
var 通道变量 chan 通道类型
```

- 通道类型：通道内的数据类型。
- 通道变量：保存通道的变量。

chan 类型的空值是 nil，声明后需要配合 make 后才能使用。

### 2、创建通道（常用）

通道是引用类型，需要使用 make 进行创建，格式如下：

```go
通道实例 := make(chan 数据类型)
```

- 数据类型：通道内传输的元素类型。
- 通道实例：通过make创建的通道句柄。

```go
ch1 := make(chan int)                 // 创建一个整型类型的通道
ch2 := make(chan interface{})         // 创建一个空接口类型的通道, 可以存放任意格式
type Equip struct{ /* 一些字段 */ }
ch2 := make(chan *Equip)             // 创建Equip指针类型的通道, 可以存放*Equip
```

### 3、使用通道发送数据

通道发送数据的格式

```go
通道变量 <- 值
```

- 通道变量：通过make创建好的通道实例。
- 值：可以是变量、常量、表达式或者函数返回值等。值的类型必须与ch通道的元素类型一致。

```go
// 创建一个空接口通道
ch := make(chan interface{})
// 将0放入通道中
ch <- 0
// 将hello字符串放入通道中
ch <- "hello"
```

把数据往通道中发送时，如果接收方一直都没有接收，那么发送操作将持续阻塞。Go 程序运行时能智能地发现一些永远无法发送成功的语句并做出提示

### 4、使用通道接收数据

通道接收同样使用`<-`操作符，通道接收有如下特性：

- **通道的收发操作在不同的两个 goroutine 间进行**，由于通道的数据在没有接收方处理时，数据发送方会持续阻塞，因此通道的接收必定在另外一个 goroutine 中进行
- **接收将持续阻塞直到发送方发送数据**，如果接收方接收时，通道中没有发送方发送数据，接收方也会发生阻塞，直到发送方发送数据为止。
- **每次接收一个元素**，通道一次只能接收一个数据元素。

通道的数据接收一共有以下 4 种写法：

#### 1) 阻塞接收数据

阻塞模式接收数据时，将接收变量作为`<-`操作符的左值，格式如下：

```go
data := <-ch
```

执行该语句时将会阻塞，直到接收到数据并赋值给 data 变量。

#### 2) 非阻塞接收数据

使用非阻塞方式从通道接收数据时，语句不会发生阻塞，格式如下：

```go
data, ok := <-ch
```

- data：表示接收到的数据。未接收到数据时，data 为通道类型的零值。
- ok：表示是否接收到数据。


非阻塞的通道接收方法可能造成高的 CPU 占用，因此使用非常少。如果需要实现接收超时检测，可以配合 select 和计时器 channel 进行，可以参见后面的内容。

#### 3) 接收任意数据，忽略接收的数据

阻塞接收数据后，忽略从通道返回的数据，格式如下：

```go
<-ch
```

执行该语句时将会发生阻塞，直到接收到数据，但接收到的数据会被忽略。这个方式实际上只是通过通道在 goroutine 间阻塞收发实现并发同步。

```go
package main

import (
	"fmt"
)

func main() {

	ch := make(chan int) // 构建一个通道

	go func() { // 开启一个并发匿名函数
		fmt.Println("start goroutine")

		ch <- 0 // 通过通道通知main的goroutine
		fmt.Println("exit goroutine")
	}()

	fmt.Println("wait goroutine")
	<-ch // 等待匿名goroutine

	fmt.Println("all done")
}

// wait goroutine
// start goroutine
// exit goroutine
// all done
```

#### 4) 循环接收

通道的数据接收可以借用 for range 语句进行多个元素的接收操作，格式如下：

```go
for data := range ch {
}
```

通道 ch 是可以进行遍历的，遍历的结果就是接收到的数据。数据类型就是通道的数据类型。通过 for 遍历获得的变量只有一个，即上面例子中的 data。

```go
package main

import (
	"fmt"
	"time"
)

func main() {

	ch := make(chan int) // 构建一个通道

	go func() { // 开启一个并发匿名函数
		for i := 3; i >= 0; i-- { // 从3循环到0
			ch <- i                 // 发送3到0之间的数值
			time.Sleep(time.Second) // 每次发送完时等待
		}
	}()

	for data := range ch { // 遍历接收通道数据
		fmt.Println(data) // 打印通道数据
		if data == 0 {    // 当遇到数据0时, 退出接收循环
			break
		}
	}
}

// 3
// 2
// 1
// 0
```