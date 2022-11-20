-i

代表着保存

不加的话，只能看看效果

在第一行后加行ok

sed -i 1a\ok workers

sed -i '2a okok' workers

第一行取代为ok

sed -i 1c\ok workers

删除第一行

sed -i 1d workers

删除/etc/passwd中的第1行

1	sed -i '1d' passwd

删除/etc/passwd中的8行到14行的所有内容

1	sed -i '8,14d' passwd

删除/etc/passwd中的不能登录的用户(筛选条件：/sbin/nologin)

1	sed -i '/\/sbin\/nologin/d' passwd

删除/etc/passwd中以mail开头的行，到以ftp开头行的所有内容

1	sed -i '/^mail/,/^ftp/d' passwd

删除/etc/passwd中第一个不能登录的用户 到 第13行的所有内容

1	# 这个表达式会删除第一个 /sbin/nologin 到 第13行，然后再重新开始再次删除，循环。。。，不建议使用

2	sed -i '/\/sbin\/nologin/,13d' passwd

删除/etc/passwd中第5行到以ftp开头的所有行的内容

1	sed -i '5,/^ftp/d' passwd

删除/etc/passwd中以nobody开头的行到最后行的所有内容

1	sed -i '5,/^ftp/d' passwd

删除/etc/passwd中以nobody开头的行到最后行的所有内容

1	sed -i '/^nobody/,$d' passwd

典型需求：

删除nginx.conf文件中注释行和空行

1	sed -i '/^#/d;/^$/d' nginx.conf

 

删除一个或多个空格加 # 号的行

1	sed -i '/[:blank:]*#/d' nginx.conf

在配置文件中所有不以#开头的行前面添加*符号，注意：以#开头的行不添加

^[^#] 对以#号开头的行取反就是非#开头的行，& 是反向引用代表前面的行，然后加*

1	sed -i 's/^[^#]/*&/g' nginx.conf

来自 <https://www.cnblogs.com/crazymagic/p/11147988.html> 

替换：

sed -ie 's/AcceptEnv LANG LC_*/# AcceptEnv LANG LC_*/g' /etc/ssh/sshd_config

A.txt里面内容如下

A;

B;

C;

write by luohao199621;

1.要将“B；”换为"glad to see you; hello!"

linux 命令如下

sed -ie 's/B;/glad to see you; hello!/g'   A.txt (文件夹所在路径）

2.要将"C;"删除

linux 命令如下

sed -ie  's/C;/ /g'  A.txt  (将"C;"替换为空就相当于删除）

来自 <https://blog.csdn.net/luohao199621/article/details/79486506?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param> 


