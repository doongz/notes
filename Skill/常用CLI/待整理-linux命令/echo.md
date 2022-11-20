1.在窗口输出指定内容

echo “content”

2.向文件中写入内容

echo “cover” > a.txt

（文件原先的内容会被覆盖掉）

3.向文件追加内容

echo “add add” >> a.txt

会在文件下面一行添加

echo -e "abc\ndef"

输出：

abc

def

-e表示启用解释反斜杠转义

默认为-E：禁用转义

echo本身默认最后会输出一个换行，要禁用最后的换行，可使用

echo -n "abc"

-n     do not output the trailing newline

echo具体语法如下：

Linux echo命令不能显示文件中的内容。

功能说明：显示文字。

语   法：echo [-ne] [字符串]或 echo [--help] [--version]

补充说明：echo会将输入的字符串送往标准输出。输出的字符串间以空白字符隔开, 并在最后加上换行号。

参   数：-n 不要在最后自动换行

 -e 若字符串中出现以下字符，则特别加以处理，而不会将它当成一般文字输出：

\a 发出警告声；

\b 删除前一个字符；

\c 最后不加上换行符号；

\f 换行但光标仍旧停留在原来的位置；

\n 换行且光标移至行首；

\r 光标移至行首，但不换行；

\t 插入tab；

\v 与\f相同；

\ 插入\字符；

\nnn 插入nnn（八进制）所代表的ASCII字符；

