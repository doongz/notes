# socket

https://www.zhihu.com/question/29637351

## 简述

就是两个进程，跨计算机，他俩需要通讯的话，需要通过网络对接起来。

这就是 socket 的作用。打个比方吧，两个进程在两个计算机上，需要有一个进程做被动方，叫做服务器。另一个做主动方，叫做客户端。他们位于某个计算机上，叫做主机 host ，在网络上有自己的 ip 地址。**一个计算机上可以有多个进程作为服务器，但是 ip 每个机器只有一个，所以通过不同的 port 数字加以区分**。

因此，**服务器程序需要绑定在本机的某个端口号上。客户端需要声明自己连接哪个地址的那个端口。两个进程通过网络建立起通讯渠道，然后就可以通过 recv send 来收发一些信息，完成通讯**。

所以 **socket 就是指代承载这种通讯的系统资源的标识**。

---

不要把 socket 想得太复杂，它其实和一般的文件读写没有太大区别。

只不过一个是用 fopen 打开，读写模式作为参数传进去；一个是用 socket 打开，服务器还是客户通过 connect / listen 设置。

一个是 fread / fwrite 读写，一个是 recv 和 send 读写（在Linux 下用 read 和 write 的话，文件和 socket 两者都能读写，只是无法直接设置一些特殊的 flag)

**一般的文件以及 socket 客户端读写的都是数据，而 socket 服务端 accept 读出来的是可以读写的客户端文件**

socket 是进程间数据传输的媒介

新手知道这些就可以大胆地去做 socket 编程了。

## 文章一

### 1、层级结构

![](https://pic2.zhimg.com/80/v2-226e5169b8c0da05cb3605d00269356f_1440w.jpg?source=1940ef5c)

**socket 其实就是操作系统提供给程序员操作「网络协议栈」的接口，说人话就是，你能通过socket 的接口，来控制协议找工作，从而实现网络通信，达到跨主机通信**。

协议栈的上半部分有两块，分别是负责收发数据的 TCP 和 UDP 协议，它们两会接受应用层的委托执行收发数据的操作。（传输层）

协议栈的下面一半是用 IP 协议控制网络包收发操作，在互联网上传数据时，数据会被切分成一块块的网络包，而将网络包发送给对方的操作就是由 IP 负责的。（IP层）

此外 IP 中还包括 `ICMP` 协议和 `ARP` 协议。

- `ICMP` 用于告知网络包传送过程中产生的错误以及各种控制信息。
- `ARP` 用于根据 IP 地址查询相应的以太网 MAC 地址。

IP 下面的网卡驱动程序负责控制网卡硬件，而最下面的网卡则负责完成实际的收发操作，也就是对网线中的信号执行发送和接收操作。（数据链路层）

那具体 socket 有哪些接口呢？

socket 一般分为 **TCP 网络编程**和 **UDP 网络编程**

### 2、TCP 网络编程

先来看看 TCP 网络编程，一幅图就很好理解。

![](https://pic3.zhimg.com/80/v2-7105d213a9207bf0d497455c652df7e2_1440w.jpg?source=1940ef5c)

基于 TCP 协议的客户端和服务器工作

- 服务端和客户端初始化 `socket`，得到文件描述符；
- 服务端调用 `bind`，将绑定在 IP 地址和端口;
- 服务端调用 `listen`，进行监听；
- 服务端调用 `accept`，等待客户端连接；
- 客户端调用 `connect`，向服务器端的地址和端口发起连接请求；
- 服务端 `accept` 返回用于传输的 `socket` 的文件描述符；
- 客户端调用 `write` 写入数据；服务端调用 `read` 读取数据；
- 客户端断开连接时，会调用 `close`，那么服务端 `read` 读取数据的时候，就会读取到了 `EOF`，待处理完数据后，服务端调用 `close`，表示连接关闭。

这里需要注意的是，服务端调用 `accept` 时，连接成功了会返回一个已完成连接的 socket，后续用来传输数据。

所以，监听的 socket 和真正用来传送数据的 socket，是「两个」 socket，一个叫作**监听 socket**，一个叫作**已完成连接 socket**。

成功连接建立之后，双方开始通过 read 和 write 函数来读写数据，就像往一个文件流里面写东西一样。

### 3、结合三次握手连接的 TCP socket

![](https://pic1.zhimg.com/80/v2-527311b944dd6de447c2f2d15f615e11_1440w.jpg?source=1940ef5c)

客户端连接服务端

- 客户端的协议栈向服务器端发送了 SYN 包，并告诉服务器端当前发送序列号 client_isn，客户端进入 SYN_SENT 状态；
- 服务器端的协议栈收到这个包之后，和客户端进行 ACK 应答，应答的值为 client_isn+1，表示对 SYN 包 client_isn 的确认，同时服务器也发送一个 SYN 包，告诉客户端当前我的发送序列号为 server_isn，服务器端进入 SYN_RCVD 状态；
- 客户端协议栈收到 ACK 之后，使得应用程序从 `connect` 调用返回，表示客户端到服务器端的单向连接建立成功，客户端的状态为 ESTABLISHED，同时客户端协议栈也会对服务器端的 SYN 包进行应答，应答数据为 server_isn+1；
- 应答包到达服务器端后，服务器端协议栈使得 `accept` 阻塞调用返回，这个时候服务器端到客户端的单向连接也建立成功，服务器端也进入 ESTABLISHED 状态。

### 4、结合四次挥手的 TCP socket

![](https://pica.zhimg.com/80/v2-41ee0ce58d9cbada7edd9fa8ded1f07e_1440w.jpg?source=1940ef5c)

客户端调用 close 过程

- 客户端调用 `close`，表明客户端没有数据需要发送了，则此时会向服务端发送 FIN 报文，进入 FIN_WAIT_1 状态；
- 服务端接收到了 FIN 报文，TCP 协议栈会为 FIN 包插入一个文件结束符 `EOF` 到接收缓冲区中，应用程序可以通过 `read` 调用来感知这个 FIN 包。这个 `EOF` 会被**放在已排队等候的其他已接收的数据之后**，这就意味着服务端需要处理这种异常情况，因为 EOF 表示在该连接上再无额外数据到达。此时，服务端进入 CLOSE_WAIT 状态；
- 接着，当处理完数据后，自然就会读到 `EOF`，于是也调用 `close` 关闭它的套接字，这会使得服务端会发出一个 FIN 包，之后处于 LAST_ACK 状态；
- 客户端接收到服务端的 FIN 包，并发送 ACK 确认包给服务端，此时客户端将进入 TIME_WAIT 状态；
- 服务端收到 ACK 确认包后，就进入了最后的 CLOSE 状态；
- 客户端经过 `2MSL` 时间之后，也进入 CLOSE 状态；

## 文章二

作者：张彦飞
链接：https://www.zhihu.com/question/29637351/answer/2177529520

---

现在业界感觉从协议到[socket](https://www.zhihu.com/search?q=socket&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2177529520})中间这环是欠缺的，导致很多同学并不能融会贯通。计算机学生在学校学习网络的时候，讲的的分层协议，arp ip tcp 三次握手 四次挥手 流量控制 等等基础概念。但是等到了网络编程的时候，突然就跳跃到socket了。这个跳跃幅度着实有点大，导致很多人无法理解。

其实我觉得在计算机课程教学中缺少了一环，那就是介绍一下socket编程是如何和网络中的各种概念联系起来的，只有这样这样才能融会贯通。

比如，**socket中的listen到底是干了啥**？很多人只知道大家都是这么用，却不明白它的底层原理。**实际上服务器在准备接受客户端的握手请求之前，需要准备半连接队列和全连接队列，准备好之后才能接收握手请求**。

[为什么服务端程序都需要先 listen 一下？](https://zhuanlan.zhihu.com/p/397740688)

再比如**connect是干了啥**？同样没人讲过。**实际上connect是客户端选择了一个可用端口，然后向服务器发起握手请求了**。同时自己还开了个定时器，如果逾期收不到反馈会重试。

客户端发起连接请求之后，三次握手的工作就由双方的内核完成了。三次握手成功之后，服务器端会创建一个sock对象，在它上面保存好tcp连接的[四元组](https://www.zhihu.com/search?q=四元组&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A2177529520})信息，然后放在接收队列中。

你调用accept的时候就是从这个接收队列中获取一个握手就绪连接来用。

[能将三次握手理解到这个深度，面试官拍案叫绝！](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/vlrzGc5bFrPIr9a7HIr2eA)

再后面就是在这个连接之上的读和写了。用户流程只需要发起读写请求就好了，放到接收缓存或者发送缓存中。真正的读写，重试都由内核从缓存中取数据，或者写入。

[图解 Linux 网络包发送过程](https://zhuanlan.zhihu.com/p/373060740)

[图解Linux网络包接收过程](https://zhuanlan.zhihu.com/p/256428917)

当然了，用户进程在发送或者接收数据的时候如果发送缓存区不够用，或者接收的数据并未到达，那该有可能会被阻塞。会导致一次进程上下文切换的开销。放内核ready的时候，再把该进程切换回来，又来一次切换开销。

[深入理解高性能网络开发路上的绊脚石 - 同步阻塞网络 IO](https://zhuanlan.zhihu.com/p/353850099)

如果嫌弃阻塞带来的各种额外的cpu开销，也不想创建那么多进程，那就来试试epoll

[图解 | 深入揭秘 epoll 是如何实现 IO 多路复用的！](https://link.zhihu.com/?target=https%3A//mp.weixin.qq.com/s/OmRdUgO1guMX76EdZn11UQ)

如果你想用多进程的方式来使用epoll，哪个进程来处理事件等待，哪个进程真正发送，由于分工的不同，又涉及到Reactor，Proactor等模式。

如果你嫌弃手写epoll以及各种复杂的进程协作模式太麻烦，那就选一些成熟的网络库来用就行了。它们都替你封装好了，例如java里的netty，golang里的net包，C++里的[Sogou Workflow](https://link.zhihu.com/?target=https%3A//github.com/sogou/workflow)。

## golang 代码

server

```go
package main

import (
	"bufio"
	"fmt"
	"net"
)

func main() {
	// 1. 监听端口
	listener, err := net.Listen("tcp", "127.0.0.1:8080")
	if err != nil {
		fmt.Println("listen fail err", err)
		return
	}

	defer listener.Close()

	for {
		// 2. 接收客户端请求建立链接
		conn, err := listener.Accept()
		if err != nil {
			fmt.Println("accept fail err", err)
			continue
		}

		// 3. 创建goroutine处理链接
		go handler(conn)

	}
}

func handler(conn net.Conn) {
	defer fmt.Println("conn链接关闭了")
	defer conn.Close() // 关闭链接

	reader := bufio.NewReader(conn)
	for {
		var buf [4096]byte
		n, err := reader.Read(buf[:]) // 读取数据
		if err != nil {
			break
		}
		recvStr := string(buf[:n])
		fmt.Println("收到Client发来的数据: ", recvStr)
		recvStr = "server-" + recvStr
		conn.Write([]byte(recvStr))
	}

}
```

client

```go
package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

func main() {
	// 建立与服务器的链接
	conn, err := net.Dial("tcp", "127.0.0.1:8080")
	if err != nil {
		fmt.Println("Dial fail err", err)
		return
	}

	// 关闭链接
	defer conn.Close()

	inputReader := bufio.NewReader(os.Stdin)
	// 进行数据的收发
	for {
		input, _ := inputReader.ReadString('\n')
		inputInfo := strings.Trim(input, "\r\n")
		if strings.ToUpper(inputInfo) == "Q" { // 如果用户输入的是q/Q就退出
			return
		}

		// 发送数据
		_, err := conn.Write([]byte(inputInfo))
		if err != nil {
			fmt.Println("Write fail err", err)
			return
		}

		// 接收数据
		buf := [4096]byte{}
		n, err := conn.Read(buf[:])
		if err != nil {
			fmt.Println("Read fail err", err)
			return
		}
		fmt.Println("收到server发来的数据: ", string(buf[:n]))
	}
}
```

