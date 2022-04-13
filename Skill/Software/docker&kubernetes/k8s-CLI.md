# k8s CLI

## 一、pod

## 二、deployment & service

## 三、pv & pvc

## 四、secret

## 五、configmap

## 六、cronjob





## 一、命令

### 1、查看某个资源列表

`kubectl get pod -n <namespace> -o wide`

pod：指定的资源

-n: 指定命名空间（包含一系列相关的pod）

-o wide: 看到资源的所在ip和所在节点node了

-o yaml 查看某个现有资源的配置项

### 2、进入容器

`kubectl exec -it  <podName> -c <containerName> -n <namespace> -- <shell comand>`

例如进入pod

`kubectl exec -ti <podName> -n <namespace> -- /bin/sh`

### 3、查看pod列表中的某个pod的详细信息

`kubectl describe pod <podName> -n <namespace>` 

### 4、查看日志

`kubectl logs <podName> -n <namespace> -c <containerName>`

-c 执行pod中的某个容器

-f参数可以持续查看日志

### 5、创建资源

`kubectl create -f <配置文件名.yaml>`

`kubectl create <资源类型> <资源名>` 

### 6、删除

`kubectl delete -f <配置文件名.yaml>`

`kubectl delete <资源类型> <资源名>`

`kubectl delete pod --all`

### 7、修改配置

`kubectl edit pod kubia-manual`


给节点打标签，可有多个标签

kubectl label nodes k8s-node-a03-19-10 usage=code-highway

kubectl label nodes k8s-node-a03-19-10 department=kirin-po

kubectl label nodes k8s-node-b02-06-05 usage=code-highway department=kirin-ai

### 8、查看标签

kubectl get node --show-labels

根据label查node

kubectl get node -l 'usage=code-highway'

删除label

kubectl label nodes k8s-node-a03-19-10 department-

精简看label

kubectl get nodes --show-labels |awk -F'[ ,]+' '{print $$1}{for(i=8;i<=NF;i++)if($$i!~"kubernetes.io"){print "\t"$i}}'

### 9、秘钥

K8s 存放秘钥的方式

```python
kubectl create secret generic ldap-secret --from-literal='LDAP_ACCOUNT=pphisik3jenkins' --from-literal='LDAP_CERTIFICATION=8sbbfnN$'
```

### 10、复制文件

kubectl cp -h

kubectl cp collect_connection_info_v1.py workspace-10-121-222-30-4129:/repotools

### 11、执行命令

kubectl exec -it workspace-10-121-219-89-6359 -- ls /repotools


kubectl get nodes  --show-labels |awk -F'[ ,]+' '{print $1}{for(i=8;i<=NF;i++)if($i!~"kubernetes.io"){print "\t"$i}}'





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

 



 



 



