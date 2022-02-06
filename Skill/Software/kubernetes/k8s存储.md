**Kubernetes volume，拥有明确的生命周期**，与所在的Pod的生命周期相同。因此，Kubernetes volume独立与任何容器，与Pod相关，所以数据在重启的过程中还会保留，当然，如果这个Pod被删除了，那么这些数据也会被删除。更重要的是，**Kubernetes volume 支持多种类型，任何容器都可以使用多个****Kubernetes volume**。

它的核心，**一个 volume 就是一个目录，可能包含一些数据，这些数据对****pod****中的所有容器都是可用的，这个目录怎么使用，什么类型，由什么组成都是由特殊的****volume** **类型决定的。**

要使用Volume，pod需要指定Volume的类型和内容（**spec.volumes字段**），和映射到容器的位置（**spec.containers.volumeMounts字段**）。

 

 

PersistentVolume（**PV**）是集群中由管理员配置的**一段网络存储**。 它是集群中的资源，就像节点是集群资源一样。 PV是容量插件，如Volumes，但其生命周期独立于使用PV的任何单个pod。 此API对象捕获存储实现的详细信息，包括NFS，iSCSI或特定于云提供程序的存储系统。

PersistentVolumeClaim（**PVC**）是由**用户进行存储的请求**。 它类似于pod。 Pod消耗节点资源，PVC消耗PV资源。Pod可以请求特定级别的资源（CPU和内存）。声明可以请求特定的大小和访问模式（例如，可以一次读/写或多次只读）。

虽然PersistentVolumeClaims允许用户使用抽象存储资源，但是PersistentVolumes对于不同的问题，用户通常需要具有不同属性（例如性能）。群集管理员需要能够提供各种PersistentVolumes不同的方式，而不仅仅是大小和访问模式，而不会让用户了解这些卷的实现方式。对于这些需求，有**StorageClass** **资源。**

 

 

 

 

