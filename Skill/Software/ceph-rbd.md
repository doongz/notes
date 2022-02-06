# Ceph RBD

apt install ceph-common

ceph.conf 放到 /etc/ceph

## 一、ceph 相关命令

| 命令                                                | 描述           |
| --------------------------------------------------- | -------------- |
| ceph -s                                             | 看ceph状态     |
| ceph df                                             | 看存储使用状态 |
| ceph osd tree                                       | 查看有多少osd  |
| ceph osd lspools                                    | 看存储池       |
| ceph osd pool create <pool_name> <pg_num> <pgp_num> | 创建存储池     |
| ceph osd pool set <pool_name> size <备份数>         | 设置备份数     |
| ceph osd pool set <pool_name> size <备份数>         | 设置备份数     |
| ceph osd pool get <pool_name> size                  | 查看备份数     |

创建存储池命令详解：

pgp_num跟pg_num保持一致, pg_num = ((osd_num * 100) / 备份数) -> 再向上取2的幂次方，例如，计算以后=1000，则取值1024

## 二、rbd 相关命令

### 1、查看

| 命令                             | 描述                                    |
| :------------------------------- | :-------------------------------------- |
| rbd ls user_pool                 | 查看资源池里面的镜像                    |
| rbd info user_pool/zd_image      | 查看镜像的具体信息                      |
| rbd du <pool_name>/<volume_name> | 查看卷实际使用大小                      |
| rbd snap ls user_pool/zd_image   | 查看该镜像下的快照                      |
| rbd showmapped                   | 查看本机上挂载的rbd设备，配合grep可以查 |

### 2、创建

| 命令                                                         | 描述                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| rbd create user_pool/zd_image --size 100                     | 建个100M的镜像（卷）                                         |
| rbd map user_pool/zd_image<br/>mkfs -t ext4 /dev/rbd0<br/>mount /dev/rbd0 /mnt | 输出：/dev/rbd0<br/>挂载到本地使用                           |
| rbd snap create user_pool/zd_image@zd_snap                   | 创建快照                                                     |
| rbd snap protect user_pool/zd_image@zd_snap                  | 保护快照后                                                   |
| rbd clone user_pool/zd_image@zd_snap user_pool/zd_image_snap_clone | 才能制作克隆卷                                               |
| rbd flatten rbd/zd_image_snap_clone                          | 将一个克隆卷flatter后，该克隆卷与父镜像解除关系，成为独立镜像 |
| rbd copy user_pool/zd_image user_pool/zd_copy_image          | 拷贝一个镜像，拷贝的镜像不继承父子关系                       |
| rbd deep copy user_pool/zd_image user_pool/zd_deep_copy_image | 拷贝一个镜像，拷贝的镜像继承父子关系                         |

### 3、删除

| 命令                                                         | 描述                                  |
| :----------------------------------------------------------- | :------------------------------------ |
| rbd unmap /dev/rbd10                                         | 在本机上卸载块设备，-o force 强制删除 |
| rbd rm user_pool/zd_image                                    | 删除镜像                              |
| rbd snap rm user_pool/zd_image@zd_snap                       | 删除快照                              |
| rbd snap unprotect user_pool/zd_image@zd_snap                | 快照去保护                            |
| ceph osd pool delete user_pool user_pool --yes-i-really-really-mean-it | 删除存储池                            |

