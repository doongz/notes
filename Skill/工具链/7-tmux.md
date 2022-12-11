# tmux

![img](./doc/tmux-cheatsheet.png)

鼠标可以做很多操作，

可以上下拖动，查看结果，并且可以选择windows，选择pane，调整pane大小，都可以使用鼠标或者trackpad

```shell
$ vim ~/.tmux.conf
set-option -g mouse on
$ tmux source ~/.tmux.conf
```



参考：[tmux基本操作](https://blog.csdn.net/sui_152/article/details/121650341)

Tmux 窗口有大量的快捷键。所有快捷键都要通过前缀键唤起。默认的前缀键是Ctrl+b，即先按下Ctrl+b，快捷键才会生效。

举例来说，帮助命令的快捷键是Ctrl+b ?。它的用法是，在 Tmux 窗口中，先按下Ctrl+b，再按下?，就会显示帮助信息。

然后，按下 ESC 键或q键，就可以退出帮助。


| 命令                    | 说明                                         |
| ----------------------- | -------------------------------------------- |
| Ctrl+b  %               | 左右分窗口                                   |
| Ctrl+b  “               | 上下分窗口                                   |
| Ctrl+b 上下左右         | 再按上下左右键切换窗口                       |
| Ctrl+b o                | 切换窗口                                     |
| Ctrl+b  d               | 退出当前窗口                                 |
| Ctrl+b [                | 进行上下翻页，q取消翻页                      |
| Ctrl+b x                | 关闭当前窗格，exit                           |
| Ctrl+b Ctrl+<arrow key> | 按箭头方向调整窗格大小                       |
| Ctrl+b !                | 将当前窗格拆分为一个独立窗口。               |
| Ctrl+b z                | 当前窗格全屏显示，再使用一次会变回原来大小。 |
| Ctrl+b q + 数字         | 显示窗格编号，快速按数字键可跳转窗口         |
|                         |                                              |
| Ctrl+b {                | 当前窗格与上一个窗格交换位置                 |
| Ctrl+b }                | 当前窗格与下一个窗格交换位置                 |
| Ctrl+b s                | 列出所有会话                                 |
|                         |                                              |
|                         |                                              |
|                         |                                              |
|                         |                                              |



## 会话管理

[tmux使用 安装、分屏、切换窗口](https://www.csdn.net/tags/MtjaMg4sNTAyMTItYmxvZwO0O0OO0O0O.html)

新建一个窗口

```bash
tmux new -s cpr(cpr是一个窗口的名字)
```

新建其他窗口

```bash
先ctrl+b 再 c
```

跳转到下一个窗口

```bash
先ctrl+b 再 n
```

跳转到上一个窗口

```bash
先ctrl+b 再 p
```

跳转到指定窗口

```bash
先ctrl+b 再分号键
出现index界面输入bash号
```

左右分屏

```bash
先ctrl+b 再shift+%
```

上下分屏

```bash
先ctrl+b 再shift+分号键
```

分屏跳转

```bash
先ctrl+b 再上下左右方向键
```





### 1、创建会话

第一个启动的 Tmux 窗口，编号是`0`，第二个窗口的编号是`1`，以此类推。这些窗口对应的会话，就是 0 号会话、1 号会话。

```shell
tmux
```

### 2、退出当前会话

在 Tmux 窗口中，按下`Ctrl+b` `d`或者输入：`tmux detach`命令，就会将当前会话窗退出。

```shell
Ctrl+b d
tmux detach
```

上面命令执行后，就会退出当前 tmux 窗口，但是会话和里面的进程仍然在后台运行。

`tmux ls`命令可以查看当前所有的 tmux 会话。

```shell
tmux ls
# or
tmux list-session
```

### 3、进入tmux会话

`tmux attach`命令用于重新接入某个已存在的会话。

```shell
# 使用会话编号
tmux attach -t 0    # 0 是会话名称
#or
tmux a -t 0
# 使用会话名称
tmux attach -t <session-name>
```

### 4、杀死会话

`tmux kill-session`命令用于杀死某个会话。

```shell
# 使用会话编号
tmux kill-session -t 0
# 使用会话名称
tmux kill-session -t <session-name>
```

### 5、切换会话

`tmux switch`命令用于切换会话。

```shell
# 使用会话编号
tmux switch -t 0
# 使用会话名称
tmux switch -t <session-name>
```

### 6、重命名会话

`tmux rename-session`命令用于重命名会话。

```shell
Ctrl+b $ 重命名当前会话 
tmux rename-session -t 0 <new-name>
```

