复制

1. 将光标移动到要复制的文本开始的地方，按v进入可视模式。

2. 将光标移动到要复制的文本的结束的地方，按y复制。此时vim会自动将光标定位到选中文本的开始的地方，并退出可视模式。

3. 移动光标到文本结束的地方，按p粘贴。

清空：gg dG

删行：shift d  或者dd

u   撤销上一步的操作

Ctrl+r 恢复上一步被撤销的操作

page 翻页

Home 移动到当前行行首

end 移动到当前行行尾

显示行数

:set nu

第一种方式

	• :$ 跳转到最后一行
	
	• :1 跳转到第一行
	
	• :n 跳转到第n行

第二种方式

	• shift+g 跳转到最后一行
	
	• gg 跳转到第一行
	
	• command+上下箭头

查找

/print

回车

n下一个

多行注释

1、进入vi/vim编辑器，按CTRL+V进入可视化模式（VISUAL BLOCK）

2、移动光标上移或者下移，选中多行的开头，如下图所示

3、选择完毕后，按大写的的I键，此时下方会提示进入“insert”模式，输入你要插入的注释符，例如#

4、最后按ESC键，你就会发现多行代码已经被注释了

5、删除多行注释的方法，同样 Ctrl+v 进入列选择模式，移到光标把注释符选中，按下d，注释就被删除了。

vim设置

vim ~/.vimrc

set tabstop=4        设置tab键缩进为4个字符

set expandtab    转化为空格

set autoindent  设置自动缩进

set paste               首行 不会自动添加好多空格了 

 

set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936

set termencoding=utf-8

set encoding=utf-8


光标回到上次退出的地方

if has("autocmd")

  au BufReadPost * if line("'\"") > 1 && line("'\"") <= line("$") | exe "normal! g'\"" | endif

endif







