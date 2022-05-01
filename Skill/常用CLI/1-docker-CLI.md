# docker CLI

## 1、登陆远端docker库

```shell
docker login <docker库地址>
```

报错：Error response from daemon: Get http: server gave HTTP response to HTTPS client

报错：Error response from daemon: Get x509: certificate signed by unknown authority

解决：

`vim /etc/docker/daemon.json`

```
{
  "storage-driver": "overlay2",
  "insecure-registries": ["<docker库地址1>", "<docker库地址2>", "<docker库地址3>"]
}
```

重启服务：`systemctl restart docker`

## 2、拉镜像

```
docker pull ubuntu
```

## 3、制作镜像

```
docker build -t <镜像名>:<镜像版本> .
```

Dockerfile 自行改写

不想让容器退出，在 Dockerfile 后面加上 `ENTRYPOINT ["tail","-f","/dev/null"]`

## 4、启动容器

```
docker run -itd \
--name <容器名> \
-p 8888:8888 \
-v /root/configs/Server:/root/configs \
-v /root/logs/Server:/root/logs \
-v /usr/share/zoneinfo:/usr/share/zoneinfo \
<镜像名>:<镜像版本>
```

## 5、进入容器

```
docker exec -it <容器名或容器ID> /bin/bash
```

-u 用户名，可指定进入时的用户

## 7、删除容器

```
docker rm -f <容器名或容器ID>
```

## 8、停止容器

```
docker stop <容器名或容器ID>
```

## 9、启动已停止的容器

```
docker start <容器名或容器ID>
```

## 10、查看所有的容器

```
docker ps -a 
```

## 11、查看所有镜像

```
docker images
```

- REPOSITORY：表示镜像的仓库源
- TAG：镜像的标签
- IMAGE ID：镜像ID
- CREATED：镜像创建时间
- SIZE：镜像大小

## 12、删除镜像

```
docker rmi <镜像名>
```

## 13、改标签

```
docker tag <容器ID> <docker库地址>/<镜像名>:<镜像版本>
```

## 14、从宿主机拷贝文件到容器里

```
docker cp <宿主机文件路径> <容器名>:<容器里面对应的路径>
```

## 15、从容器里拷文件到宿主机

```
docker cp <容器名>:<容器里面对应的路径> <宿主机文件路径>
```

## 16、推送镜像

```
docker push <docker库地址>/<镜像名>:<镜像版本>
```

## 17、导出容器

```
docker export 1e560fca3906 > ubuntu.tar
```

## 18、导入容器快照

```
docker import ubuntu.tar <容器名>
```

