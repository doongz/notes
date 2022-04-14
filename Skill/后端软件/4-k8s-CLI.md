# k8s CLI

## 一、pod

### 1、查看某个资源列表

```
kubectl get pod -n <namespace> -o wide
```

pod：指定的资源

-n: 指定命名空间（包含一系列相关的pod）

-o wide: 看到资源的所在ip和所在节点node了

-o yaml 查看某个现有资源的配置项

### 2、创建资源

```
kubectl create -f <配置文件名.yaml>
```

### 3、进入容器

```
kubectl exec -it <podName> -c <containerName> -n <namespace> -- <shell comand>
kubectl exec -it <podName> -n <namespace> -- /bin/sh
```

### 4、查看pod列表中的某个pod的详细信息

```
kubectl describe pod <podName> -n <namespace>
```

### 5、查看日志

```
kubectl logs <podName> -n <namespace> -c <containerName>
```

-c 执行pod中的某个容器

-f 参数可以持续查看日志

### 6、删除

```
kubectl delete -f <配置文件名.yaml>
kubectl delete <资源类型> <资源名>
kubectl delete pod --all
```

### 7、修改配置

```
kubectl edit pod kubia-manual
```

### 8、复制文件

```shell
kubectl cp -h
kubectl cp <file> <pod>:<path>
```

### 9、执行命令

```shell
kubectl exec -it <pod> -- <cmd>
```

### 10、yaml模版

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: <pod-name>
spec:
  nodeSelector:
    label1: <label1>
    label2: <label2>
  tolerations:
    - operator: "Exists" 
      effect: "NoExecute" 
  containers:
    - name: <container-name>
      image: <image-name>:<tag>
      args: ['arg1','arg2','arg3']
      securityContext:
        privileged: true
      volumeMounts:
        - name: dir1
          mountPath: /srv/dir
          mountPropagation: "HostToContainer"
        - name: dir2
          mountPath: /home
        - name: volume
          mountPath: /volume
      resources:       
        requests:
          cpu: "{{cpu_cores}}"          
  volumes:
    - name: dir1
      hostPath:
        path: <host-path-1>
        type: DirectoryOrCreate
    - name: dir2
      hostPath:
        path: <host-path>
        type: DirectoryOrCreate
    - name: volume
      persistentVolumeClaim:
        claimName: <pvc-name>
        readOnly: false
  restartPolicy: Always
```

mountPropagation: "HostToContainer"、"Bidirectional"

## 二、deployment & service

更新

```shell
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

yaml文件

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: <service-name>
  labels:
    app: <app-name>
spec:
  selector:
    app: <app-name>
  ports:
    - name: http-metrics
      port: 8080
      protocol: TCP
      targetPort: 8080
  type: ClusterIP

---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: <deployment-name>
  labels:
    app: <app-name>
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <app-name>
  template:
    metadata:
      name: <pod-name>
      namespace: default
      labels:
        app: <app-name>
    spec:
      nodeSelector:
        usage: <label>
      containers:
        - name: <container-name>
          image: <image-name>:<tag>
          env:
            - name: MODE
              value: test
          volumeMounts:
            - name: kube-config
              mountPath: /srv/config/kube/
            - name: config-secret
              mountPath: /etc/config-secret
      volumes:
        - name: kube-config
          configMap:
            name: kube-config
        - name: config-secret
          secret:
            secretName: config-secret
```

## 三、node

### 1、查看结点

```shell
kubectl get node
kubectl get node --show-labels
```

精简看label

```shell
kubectl get nodes --show-labels |awk -F'[ ,]+' '{print $$1}{for(i=8;i<=NF;i++)if($$i!~"kubernetes.io"){print "\t"$i}}'
```

### 2、打标签


给节点打标签，可有多个标签

```shell
kubectl label nodes <node-name> <label-key>=<label-val>
kubectl label nodes <node-name> <label-key-1>=<label-val-1> <label-key-2>=<label-val-2>
```

### 3、删除标签

```shell
kubectl label nodes <node-name> <label-key>-
```

## 四、存储相关

### 1、StorageClass

```yaml
allowVolumeExpansion: true
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: storageclass-name
mountOptions:
- discard
parameters:
  clusterID: <id>
  csi.storage.k8s.io/controller-expand-secret-name: <name>
  csi.storage.k8s.io/controller-expand-secret-namespace: <namespace>
  csi.storage.k8s.io/fstype: xfs
  csi.storage.k8s.io/node-stage-secret-name: csi-rbd-secret
  csi.storage.k8s.io/node-stage-secret-namespace: volume
  csi.storage.k8s.io/provisioner-secret-name: csi-rbd-secret
  csi.storage.k8s.io/provisioner-secret-namespace: volume
  imageFeatures: layering,exclusive-lock,object-map,fast-diff,deep-flatten
  overlay: "true"
  permissionServiceEndpoint: <point>
  pool: <pool>
provisioner: rbd.csi.ceph.com
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

### 2、PV

```yaml
apiVersion: v1
items:
- apiVersion: v1
  kind: PersistentVolume
  metadata:
    name: pv-name
  spec:
    accessModes:
    - ReadWriteOnce
    capacity:
      storage: 2Ti
    storageClassName: csi-disk
```

### 3、PVC

从 pv 创建

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  annotations:
    everest.io/disk-volume-type: SSD
    kubernetes.io/service.name: eks
    pv.kubernetes.io/bind-completed: "yes"
    volume.beta.kubernetes.io/storage-provisioner: everest-csi-provisioner
  finalizers:
  - kubernetes.io/pvc-protection
  name: pvc-name
  namespace: default
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 2Ti
  storageClassName: csi-disk
  volumeMode: Filesystem
  volumeName: pv-name
```

从snapshot创建克隆卷

```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-name
spec:
  storageClassName: <storage_class>
  dataSource:
    name: {{snapshot_name}}
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: {{size}}
```

### 4、Snapshot

```yaml
---
apiVersion: snapshot.storage.k8s.io/v1alpha1
kind: VolumeSnapshot
metadata:
  name: <volumesnapshot_name>
spec:
  snapshotClassName: <snapshotClassName>
  source:
    name: <pvc_name>
    kind: PersistentVolumeClaim
```

## 五、secret

yaml 模版

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-name
type: Opaque
stringData:
  ip: '10.0.0.0'
  username: 'user'
  password: 'pwd'
```

```shell
kubectl create secret generic <secret-name> --from-literal='secret-val-1' --from-literal='secret-val-2'
```

## 六、configmap

以文件方式导入

```
kubectl create configmap id-rsa-file --from-file=id_rsa
```

导出配置文件

```
kubectl get configmap id-rsa-file -o yaml > configmap.yaml
```

yaml文件方式创建

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: user-configs
  namespace: default
data:
  config_file_1.yaml: |
    KEY1:
      key1: val1
      key2: val2

  config_file_2.yaml: |
    KEY2:
      key1: val1
      key2: val2
```

## 七、cronjob

```yaml
---
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: cronjob-pod
spec:
  schedule: "*/1 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: container-name
            image: <镜像名>:<tag>
          restartPolicy: OnFailure
```

查看任务状态：

```
kubectl get cronjob
```

实时看到每次Cron Job定期触发任务执行的历史和现状情况

```
kubectl get job --watch
```

找出由CronJob资源对象创建出来的Pod：

```
kubectl get pods
```


## 参考链接

中文文档：https://www.kubernetes.org.cn/k8s

官方文档：https://kubernetes.io/zh/docs/concepts/

命令列表：http://docs.kubernetes.org.cn/683.html

k8s存储卷详解：https://www.cnblogs.com/along21/p/10338242.html

例子：https://blog.csdn.net/wucong60/article/details/81458409

基本使用：

https://www.jianshu.com/p/8d60ce1587e1

https://www.jianshu.com/p/116ce601a60f

Yaml:

https://blog.csdn.net/Ay_Ly/article/details/89393281

https://www.cnblogs.com/wswang/p/10736766.html

排查service的问题

https://blog.csdn.net/Ay_Ly/article/details/89393281

https://blog.csdn.net/weixin_45423952/article/details/108006445

Flask+k8s

https://blog.csdn.net/xw_classmate/article/details/103775680

https://www.leiphone.com/news/201912/xuvpCNLuOTvssqwH.html

https://testdriven.io/blog/running-flask-on-kubernetes/

https://kubernetes.io/blog/2019/07/23/get-started-with-kubernetes-using-python/

 



 



 
