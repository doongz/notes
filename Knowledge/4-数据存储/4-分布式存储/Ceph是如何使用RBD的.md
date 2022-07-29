# Ceph 是如何使用 RBD 的

参考1：[通过iscsi协议使用ceph rbd](https://blog.csdn.net/wytdahu/article/details/46545235)

参考2：[iscsi是什么](https://baijiahao.baidu.com/s?id=1726815999411295441&wfr=spider&for=pc)

参考3：[iSCSI 百度百科](https://baike.baidu.com/item/iSCSI/2169135?fr=aladdin)

ceph 很早就已经支持通过iscsi协议来使用rbd

iSCS:连接到一个TCP/IP网络的直接寻址的存储库,通过块I/O SCSI指令对其进行访问。

iSCSI 就是用广域网仿真了一个常用的高性能本地存储总线，从而创建了一个存储局域网（SAN）

## 一、iSCSI

**iSCSI**（Internet Small Computer System Interface，发音为/ˈаɪskʌzi/），[Internet小型计算机系统接口](https://baike.baidu.com/item/Internet小型计算机系统接口/3023938)，又称为IP-SAN，是一种基于[因特网](https://baike.baidu.com/item/因特网)及[SCSI-3](https://baike.baidu.com/item/SCSI-3)协议下的存储技术，由[IETF](https://baike.baidu.com/item/IETF)提出，并于2003年2月11日成为正式的标准。

### 1、简介

**SCSI**（Internet Small Computer System Interface，发音为/ˈаɪskʌzi/），[Internet小型计算机系统接口](https://baike.baidu.com/item/Internet小型计算机系统接口/3023938)，又称为IP-[SAN](https://baike.baidu.com/item/SAN)，是一种基于[因特网](https://baike.baidu.com/item/因特网)及[SCSI-3](https://baike.baidu.com/item/SCSI-3)协议下的存储技术，由[IETF](https://baike.baidu.com/item/IETF)提出，并于2003年2月11日成为正式的标准。与传统的[SCSI](https://baike.baidu.com/item/SCSI)技术比较起来，iSCSI技术有以下三个革命性的变化：

1. 把原来只用于本机的SCSI协议透过[TCP/IP](https://baike.baidu.com/item/TCP%2FIP)网络发送，使连接距离可作无限的地域延伸；
2. 连接的[服务器](https://baike.baidu.com/item/服务器)数量无限（原来的SCSI-3的上限是15）；
3. 由于是服务器架构，因此也可以实现在线扩容以至动态部署。 

### 2、功能

iSCSI利用了TCP/IP的port 860 和 3260 作为沟通的渠道。透过两部计算机之间利用iSCSI的协议来交换[SCSI](https://baike.baidu.com/item/SCSI)命令，让计算机可以透过高速的局域网集线来把SAN模拟成为本地的储存装置。

**iSCSI使用 TCP/IP 协议（一般使用[TCP端口](https://baike.baidu.com/item/TCP端口/9603009)860和3260）。 本质上，iSCSI 让两个主机通过 IP 网络相互协商然后交换[SCSI](https://baike.baidu.com/item/SCSI)命令。这样一来，iSCSI 就是用广域网仿真了一个常用的高性能本地存储总线，从而创建了一个存储局域网（SAN）。不像某些 SAN 协议，iSCSI 不需要专用的电缆；它可以在已有的交换和 IP 基础架构上运行。**然而，如果不使用专用的网络或者子网（ LAN 或者 VLAN ），iSCSI SAN 的部署性能可能会严重下降。于是，iSCSI 常常被认为是光纤通道（Fiber Channel）的一个低成本替代方法，而光纤通道是需要专用的基础架构的。但是，基于以太网的光纤通道（[FCoE](https://baike.baidu.com/item/FCoE)）则不需要专用的基础架构。

虽然 iSCSI 可以与任意类型的 SCSI 设备进行通信，系统管理员几乎总是使用它来连接服务器计算机 （例如，数据库服务器） 和磁盘卷上存储阵列。 使用iSCSI SAN 的目的通常有以下两个：

**存储集成**公司希望将不同的存储资源从分散在网络上的服务器移动到统一的位置（常常是数据中心）； 这可以让存储的分配变得更为有效。 SAN 环境中的服务器无需任何更改硬件或电缆连接就可以得到新分配的磁盘卷。

**灾难恢复**公司希望把存储资源从一个数据中心镜像到另一个远程的数据中心上，后者在出现长时间停电的情况下可以用作热备份。 特别是，iSCSI SAN 使我们只需要用最小的配置更改就可以在 WAN 上面迁移整个磁盘阵列，实质上就是，把存储变成了“可路由的”，就像普通的网络通信一样。

### 3、网络引导/启动

从数据存储的角度，对于一个已经处于运行状态的计算机，任意类型的通用网络接口都可用于访问 iSCSI 设备。 然而，通用消费级网络接口却不能够从远程的 iSCSI 数据源引导无盘计算机。 相反，对于服务器而言，通常情况是，它是从一个小的本地 RAID 镜像或闪存驱动器引导设备来加载操作系统，并从本地设备启动完毕后，然后使用 iSCSI 来进行对数据存储的访问。

对于配有支持网络引导的网络接口设备（网卡）的计算机，可以另外配置一台 DHCP 服务器来协助“iSCSI 启动”。 这种情况下，网卡会寻找一个提供[PXE](https://baike.baidu.com/item/PXE)或[BOOTP](https://baike.baidu.com/item/BOOTP)引导映像的 DHCP 服务器。该 DHCP 服务器会根据启动网卡的[MAC地址](https://baike.baidu.com/item/MAC地址)提供对应的 iSCSI 启动目标设备/卷信息，然后计算机便可以开始从 iSCSI 远程启动的进程了。

定制的 iSCSI 接口卡提供内置的 BIOS 功能，可以为该接口事先指定一个 iSCSI 目标设备，然后就可以直接从一个启动服务器进行启动，（而不需要另设一个DHCP 服务器）， 从而减少网络配置的复杂度。