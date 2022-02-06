kubectl create configmap id-rsa-file --from-file=id_rsa

导出：

kubectl get configmap id-rsa-file -o yaml > configmap.yaml
