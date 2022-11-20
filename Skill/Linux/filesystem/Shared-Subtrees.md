# Shared Subtrees

https://docs.kernel.org/filesystems/sharedsubtree.html

### Prepare

```shell
ceph osd pool create test-pool 256 256
rbd create test-pool/code-1 --size 100
rbd create test-pool/code-2 --size 100

mkdir -p /node/container-code-1
mkdir /node/container-code-2
mkdir /node/container-workspace
mkdir /node/mnt-code-1
mkdir /node/mnt-code-2
mkdir /node/mnt-workspace
```



### Code Container

1、make mount point

```shell
mount --bind /node/mnt-code-1/ /node/mnt-code-1/
```

2、mark a subtree as shared

```shell
mount --make-rshared /node/mnt-code-1/
```

3、mount a subtree somewhere else

```shell
mount --bind /node/mnt-code-1/ /node/container-code-1/
```

4、mount block device and mkfs

```shell
rbd map test-pool/code-1
mkfs -t xfs /dev/rbd0
```

5、mount a device in container

```shell
mkdir /node/container-code-1/data-1
mount /dev/rbd0 /node/container-code-1/data-1
```

```
.
|-- container-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- container-code-2
|-- container-workspace
|-- mnt-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- mnt-code-2
`-- mnt-workspace
```

如果 `mount /dev/rbd0 /node/mnt-code-1/data-1/` 效果也是一样的

6、container-code-2 same operation

```shell
mount --bind /node/mnt-code-2/ /node/mnt-code-2/
mount --make-rshared /node/mnt-code-2/
mount --bind /node/mnt-code-2/ /node/container-code-2/
rbd map test-pool/code-2
mkdir /node/container-code-2/data-2
mount /dev/rbd1 /node/container-code-2/data-2
```

```
.
|-- container-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- container-code-2
|   `-- data-2
|       `-- data-from-code-2
|-- container-workspace
|   `-- workspace-code-1
|       `-- data-from-code-1
|-- mnt-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- mnt-code-2
|   `-- data-2
|       `-- data-from-code-2
`-- mnt-workspace
    `-- workspace-code-1
        `-- data-from-code-1
```



### Workspace Container

1、make mount point

```shell
mount --bind /node/mnt-workspace/ /node/mnt-workspace/
```

2、mark a subtree as shared

```shell
mount --make-shared /node/mnt-workspace/
```

3、mount a subtree somewhere else

```shell
mount --bind /node/mnt-workspace/ /node/container-workspace/
```

4、mark a subtree as slave

```shell
mount --make-slave /node/container-workspace/
```



### Mount Propagation

1、create workspace-code-1

```shell
mkdir /node/mnt-workspace/workspace-code-1
```

2、bind workspace-code-1

```shell
mount --bind /node/mnt-code-1/data-1/ /node/mnt-workspace/workspace-code-1/
```

```
.
|-- container-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- container-code-2
|-- container-workspace
|   `-- workspace-code-1
|       `-- data-from-code-1
|-- mnt-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- mnt-code-2
`-- mnt-workspace
    `-- workspace-code-1
        `-- data-from-code-1
```

3、create workspace-code-2

```shell
mkdir /node/mnt-workspace/workspace-code-2
```

4、bind workspace-code-2

```shell
mount --bind /node/mnt-code-2/data-2/ /node/mnt-workspace/workspace-code-2/
```

```
.
|-- container-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- container-code-2
|   `-- data-2
|       `-- data-from-code-2
|-- container-workspace
|   |-- workspace-code-1
|   |   `-- data-from-code-1
|   `-- workspace-code-2
|       `-- data-from-code-2
|-- mnt-code-1
|   `-- data-1
|       `-- data-from-code-1
|-- mnt-code-2
|   `-- data-2
|       `-- data-from-code-2
`-- mnt-workspace
    |-- workspace-code-1
    |   `-- data-from-code-1
    `-- workspace-code-2
        `-- data-from-code-2
```