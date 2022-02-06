更新

```shel
kubectl set image deployment/<deployment name> <deployment name>=<docker image>:<tag> --record
```

缩放

```shell
kubectl scale deployment.v1.apps/<deployment name> --replicas=1
```

查看历史版本记录

```shell
kubectl rollout history deployment <deployment name> 
```

指定版本 回滚 --revision参数：

```shell
kubectl rollout undo deployment <deployment name> --to-revision=<revision id>
```



