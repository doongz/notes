# ceph

来源：[如何通俗地解释ceph的工作机制？](https://www.zhihu.com/question/50803995/answer/468830791)

![img](https://pic3.zhimg.com/80/v2-c9c16ce81abfa19c89cd080e48d52168_720w.jpg?source=1940ef5c)

上面这张图很好地介绍了Ceph的架构和数据IO路径，并且也很好地诠释Ceph的设计哲理：

- 一切皆对象
- 一切均被crush

## 一切皆对象

众所周知，Ceph提供了一个统一存储平台，即结合了块存储（RBD）、对象存储（RGW）、文件存储（CephFS）与一体的分布式存储“航母”，而这艘航母的核心是RADOS。

![img](https://pica.zhimg.com/50/v2-0240cde36ecdea288a425eb016501f2b_720w.jpg?source=1940ef5c)

而RADOS这一层就是一个对象存储系统，所有进入Ceph中的数据最终都是由RADOS负责存储进OSD中。这一层提供了librados接口，供RBD、RGW、CephFS这些上层的调用，通过socket来达到与RADOS层交互，所有上层对象最终会被封装成一个个rados对象。

## 一切皆被crush

一个文件被封装成一个个rados对象后，如何均匀地分发到各个OSD节点上呢？这个时候就需要用到**ceph的核心算法：crush**

在介绍crush算法之前，还需要介绍两个概念：

1. **Pool:** Ceph对PG做的逻辑上的划分。每类存储都有其对应的默认存储池，比如RBD的默认存储池为rbd, RGW的对应存储池为default.rgw.buckets.data, CephFS的对应存储池为cephfs。也就是说，不同的RADOS上层来的数据，最终会落到不同的Pool中，由此来更好的管理数据。
2. **PG**(placement group): 是一些对象逻辑上的合集，也是Pool最基本组成单位，是实现冗余策略，数据迁移、灾难恢复等功能的基础。可以向上接受、处理客户端请求，转化为能被ObjectStore理解的事务，是一个对象落到OSD上的最后逻辑载体。

因此可以看到，一个文件从客户端写入，到最终落盘，以对象存储为例，会经历以下过程：

![[公式]](https://www.zhihu.com/equation?tex=rgw%5C+object%5C+-%3E%5C+rados+%5C+object%5C+-%3E%5C+pool%5C+-%3E%5C+pg%5C+-%3E%5C+osd%5C%5C)

而一个rgw对象被映射成一个rados对象，一个rados对象被映射到PG，一个PG映射到一个OSD中，都需要借助哈希算法，这三次哈希转变，也就是crush算法的核心。

> RGW: 提供对象存储服务的组件
>
> RBD：提供块存储服务的组件
>
> MDS：提供文件存储服务的组件
>
> OSD: Ceph管理硬盘的组件
>
> MON（Monitor）: 管理Ceph集群状态、各个组件的组件
