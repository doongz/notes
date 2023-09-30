# C++执行shell命令

来源：https://blog.csdn.net/u012234115/article/details/89215980

在linux系统下，用C++程序执行shell命令有多种方式

**管道方式**

```cpp
#include <iostream>
#include <unistd.h>
#include <sys/types.h>

int main()
{
	FILE *pp = popen("cd /xxxx && ls -l", "r"); // build pipe
	if (!pp)
		return 1;

	// collect cmd execute result
	char tmp[1024];
	while (fgets(tmp, sizeof(tmp), pp) != NULL)
		std::cout << tmp << std::endl; // can join each line as string
	pclose(pp);

	return 0;
}
```

- popen会调用fork来产生子进程，由子进程来执行命令行
- 子进程建立管道连接到输入输出，返回文件指针，输出执行结果

**系统调用方式**

```cpp
#include <cstdlib>
int main()
{   
    system("ps -ef| grep myprocess");

    return 0;
}
```

- system函数调用fork来产生子进程，执行命令行