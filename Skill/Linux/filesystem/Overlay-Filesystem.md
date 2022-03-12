# Overlay Filesystem

https://docs.kernel.org/filesystems/overlayfs.html



```shell
 mount -t overlay overlay -o lowerdir=.lower,upperdir=.upper,workdir=.worker/ /srv/code_a03-19-10/merge/
```

