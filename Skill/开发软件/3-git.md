**git init** 

​	创建新的git仓库

**git clone** 

​	拷贝一个git仓到本地

**git add**  

​	将文件添加到缓存（暂存区） 或者 git add . 添加所有文件，如果已添加文件修改了，要在执行下git add

**git status**

​	查看提交后是否有改动

**git diff** 

​	显示已写入缓存与已修改但尚未写入缓存的改动

**git commit**  

​	将缓存区的内容添加到本地版本仓库（版本库）中

**git reset HEAD** 

​	取消已缓存的内容，不在下次commit提交，如果想提交git commit -am

**git rm**   

​	从工作目录删除文件 git rm -r * 递归删除整个目录中的所有子目录和文件

​	git rm -f  # 删除之前修改过并已放到暂存区的

​	git rm --cached  # 从暂存区删除，但保留在当前工作目录

* 情况一：确实要从版本库里删除该文件，输入命令git commit ，git rm 相当于git add
* 情况二：删错了，由于版本库里还有，把误删的文件恢复，git checkout -- <file_name>

**git push**  

​	将本地版本库的分支推送到远程服务器的对应分支

* 一般形式：git push <远程主机名> <本地分支名> <远程分支名>
* 例如 git push origin master：refs/for/master ，即是将本地的master分支推送到远程主机origin上的对应master分支， origin 是远程主机名。第一个master是本地分支名，第二个master是远程分支名。
* **git push origin master**
      如果远程分支被省略，如上则表示将本地分支推送到与之存在追踪关系的远程分支（通常两者同名），如果该远程分支不存在，则会被新建
  * git push origin ：refs/for/master
      如果省略本地分支名，则表示删除指定的远程分支，因为这等同于推送一个空的本地分支到远程分支，等同于 git push origin –delete master
  * git push origin
      如果当前分支与远程分支存在追踪关系，则本地分支和远程分支都可以省略，将当前分支推送到origin主机的对应分支
  * git push
      如果当前分支只有一个远程分支，那么主机名都可以省略，形如 git push，可以使用git branch -r ，查看远程的分支名

**git fetch**

​	将远程主机的最新内容拉到本地，用户检查后决定是否合并到工作区

**git pull**

​	将远程主机的最新内容拉下来后直接合并



git fetch更新本地仓库的两种用法：

* 方法一
      $ git fetch origin master        #从远程的origin仓库的master分支下载代码到本地的origin maste
      $ git log -p master.. origin/master   #比较本地的仓库和远程参考的区别
      $ git merge origin/master        #把远程下载下来的代码合并到本地仓库，远程的和本地的合并
* 方法二
      $ git fetch origin master:temp      #从远程的origin仓库的master分支下载到本地并新建一个分支temp
      $ git diff temp             #比较master分支和temp分支的不同
      $ git merge temp             #合并temp分支到master分支
      $ git branch -d temp           #删除temp


git pull 相当于：

* git fetch origin master  # 冲远程主机的master分支拉取最新内容
* git merge FETCH_HEAD # 将拉取下来的最新内容合并到当前所在分支中

### 常见问题

#### 1、修改最近一次的commit信息

1. git commit --amend

2. 进入vim操作界面之后, 点击字母键 i 然后进入INSERT模式，然后对commit信息进行修改，然后ESC 然后 :wq 保存退出

3. 然后执行 git log 会发现最近的一次commit信息被修改成功了

#### 2、更改仓名或用户名后，要更新本地url

```
git remote set-url origin <url>
```

#### 3、删除 commit

```
git reset --hard commit_id
```

进行版本回溯。那么，在该commit_id后更新的版本包括此版本都一并删除，工作区也将回溯到HEAD-1的版本，且无法恢复

#### 4、git commit错了，多commit了文件，怎么排除掉不想要的文件？

假如基础commit是A，修改了文件foo.txt和bar.txt以后生成commit B。

**如果还没push**，这时发现bar.txt的修改是不需要commit进去的，那么可以用以下命令把bar.txt从commit B里面去掉：

```bash
git reset HEAD^ -- bar.txt
git commit --amend --no-edit
```

第一个命令把index中的bar.txt回退到commit A的版本，这样下一次commit的时候，bar.txt的版本还是commit A里的。但是查看仓库里也就是work tree里的bar.txt，是修改过后的版本。

第二个命令再次commit。如果不加--amend，会在commit B的基础上生成一个commit C。这样做虽然C里bar.txt的版本是和A的一样（相当于没修改）而且foo.txt的版本是B里的版本（是修改过的），但是commit C显得累赘，目的只是要修改并commit foo.txt而已，现在搞了2个commit出来。所以可以加上--amend，这样会在commit A的基础上重新commit一次，会生成一个新的commit B'，相当于编辑了commit B。commit B'里只包含了foo.txt的修改。B'会默认使用B的commit message，如果不需要编辑的话，可以加上--no-edit。

**如果已经push了**，并且这个仓库允许force push，那可以先按照上面的方法修改以后再force push。如果不允许force push，那可以用不加--amend的版本，然后再push。

```bash
git reset HEAD^ -- bar.txt
git commit
git push
```

不允许force push的情况下，已经push的历史不能“篡改”，那只能在后面做出新的commit来修正。
