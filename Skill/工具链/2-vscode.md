# VSCode

## 一、快捷键

### 查看全部快捷键

```
Ctrl+K Ctrl+S：查看VSCode中全部快捷键
Ctrl+K Ctrl+R：查看keyboard-shortcuts-windows.pdf
```

### 光标操作

| 用途                          | win按键         | mac按键            |
| ----------------------------- | --------------- | ------------------ |
| 光标移动到行首                | Home            | command + ⬅️        |
| 光标移动到行尾                | End             | command + ➡️        |
| 光标移动到文件开头（左上）    | Ctrl+Home       |                    |
| 光标移动到文件结尾（右下）    | Ctrl+End        |                    |
| 选择从光标到行首的内容        | Shift+Home      |                    |
| 选择从光标到行尾的内容        | Shift+End       |                    |
| 扩大选中范围                  | Shift+Alt+Right |                    |
| 缩小选中范围                  | Shift+Alt+Left  |                    |
| 向上复制光标                  | Ctrl+Alt+Up     |                    |
| 向下复制光标                  | Ctrl+Alt+Down   |                    |
| 选中的每行加上光标            | shift + alt + i | shift + option + i |
| 再按上下键 每一列上都出现光标 | ctrl + alt      |                    |
| 转到定义处                    | F12             | F12                |
| 查看定义处缩略图              | Alt+F12         |                    |
| 回退到上一个光标处            | Ctrl+U          |                    |

### 代码查找替换与格式调整

| 用途                                         | win按键                      | mac按键             |
| -------------------------------------------- | ---------------------------- | ------------------- |
| 查找                                         | Ctrl+F                       |                     |
| 查找替换                                     | Ctrl+H                       |                     |
| 全局查找                                     | Ctrl+Shift+F                 |                     |
| 全局查找替换                                 | Ctrl+Shift+H                 |                     |
| 依次找出文中所有的当前选中的单词             | ctrl + D                     | command + D         |
| 一次性找出文所有的当前选中的单词             | ctrl + shift + L             | shift + command + L |
| 向左缩进                                     | Ctrl+[                       |                     |
| 向右缩进                                     | Ctrl+]                       |                     |
| 向上移动当前行                               | Alt+Up                       |                     |
| 向下移动当前行                               | Alt+Down                     |                     |
| 向上复制当前行                               | Shift+Alt+Up                 |                     |
| 向下复制当前行                               | Shift+Alt+Down               |                     |
| 在当前行下方插入空行（光标位置可以不在行尾） | Ctrl+Enter                   |                     |
| 在当前行上方插入空行（光标位置可以不在行尾） | Ctrl+Shift+Enter             |                     |
| 切换内容是否自动换行（底部显示/隐藏滚动条）  | Alt+Z                        |                     |
| 格式化文档                                   |                              | shift + option + f  |
| 折叠所有函数                                 | Ctrl + K, Ctrl + 0           |                     |
| 折叠到某一级的函数                           | Ctrl + K， Ctrl + n(1,2,3..) |                     |
| 展开所有函数                                 | Ctrl + K, Ctrl + J           |                     |
| 仅折叠光标所在代码块处代码                   | ctrl + shift + [             |                     |
| 仅展开光标所在代码块处代码                   | ctrl + shift + ]             |                     |

### 编辑器与窗口管理

| 用途                                                 | win按键          |                     |
| ---------------------------------------------------- | ---------------- | ------------------- |
| 新建文件                                             | Ctrl+N           |                     |
| 打开新窗口                                           |                  | shift + command + n |
| 打开文件                                             | Ctrl+O           |                     |
| 打开文件夹                                           | Ctrl+Shift+O     |                     |
| 关闭当前文件                                         | Ctrl+W           |                     |
| 进行代码页面切换                                     | alt + 1 2 3      |                     |
| 打开终端                                             | ctrl + 反引号    |                     |
| 返回当前代码页面                                     | ctrl + 1         |                     |
| 目录页面和代码页面切换，文件资源管理器（Explorer）   | ctrl + shift + e |                     |
| 移动当前文件到右窗口，若没有右窗口，则创建一个新窗口 | Ctrl+Alt+→       |                     |
| 移动当前文件到左窗口                                 | Ctrl+Alt+←       |                     |
| 切换文件窗口                                         | Ctrl+Tab         |                     |
| 显示/隐藏侧边栏                                      | Ctrl+B           |                     |
| 放大/缩小编辑器窗口                                  | Ctrl +/-         |                     |
| 全屏显示                                             | F11              |                     |
| git管理窗口（Source Control）                        | Ctrl+Shift+G     |                     |
| 扩展（插件）管理窗口（Extentions）                   | Ctrl+Shift+X     |                     |
|                                                      |                  |                     |

## 二、代码格式化

### c++

谷歌风格，缩进4字符，访问说明符顶格，行数不受限

```
{BasedOnStyle: Google, AccessModifierOffset: -4, IndentWidth: 4, ColumnLimit: 0, NamespaceIndentation: All}
```

### c

```json
{BasedOnStyle: Google, AccessModifierOffset: -4, IndentWidth: 2, NamespaceIndentation: All, FixNamespaceComments: false}
```



## 三、配置文件

### Mac

#### setting.json

vscode 本身和一些插件的配置文件

```json
{
    "editor.fontSize": 15,
    "files.autoSave": "afterDelay",
    "terminal.integrated.fontSize": 13,
    "workbench.iconTheme": "material-icon-theme",
    "go.toolsManagement.autoUpdate": true,
    "gopls": {
        "experimentalWorkspaceModule": true
    },
    "extensions.autoCheckUpdates": false,
    "workbench.colorTheme": "One Dark Pro Flat",
    "[python]": {
        "editor.defaultFormatter": "ms-python.python"
    },
    "security.workspace.trust.untrustedFiles": "open",
    "editor.formatOnSave": true,
    "C_Cpp.clang_format_style": "{BasedOnStyle: Google, AccessModifierOffset: -4, IndentWidth: 4, ColumnLimit: 0, NamespaceIndentation: All}"
}
```

#### tasks.json

tasks.json 用于编译的配置文件，可配置 GCC 编译参数

```json
{
    "tasks": [
        {
            "type": "cppbuild",
            "label": "C/C++: g++ 生成活动文件",
            "command": "/usr/bin/g++",
            "args": [
                "-fdiagnostics-color=always",
                "-g",
                "${file}",
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}",
                "-std=c++17", // 设置 c++ 标准
                "-pthread", // 链接上多线程的动态库
                "-Wall", // 显示所有警告
                "-Wextra", // 显示额外警告
                "-Wfatal-errors" // 遇到第一个错误就停止，减少查找错误时间
            ],
            "options": {
                "cwd": "${fileDirname}"
            },
            "problemMatcher": [
                "$gcc"
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "detail": "调试器生成的任务。"
        }
    ],
    "version": "2.0.0"
}
```

#### launch.json

launch.json 用来执行编译后二进制的配置文件

比如用于调试，下面的 `“preLaunchTask"`  必须与 tasks.json 中的 `”label“` 匹配，才能在调试的时候使用编译器的一些参数

```json
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "g++ - 生成和调试活动文件",
            "type": "cppdbg",
            "request": "launch",
            "program": "${fileDirname}/${fileBasenameNoExtension}",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "lldb",
            "preLaunchTask": "C/C++: g++ 生成活动文件"
        }
    ]
}
```

#### c_cpp_properties.json

用于配置编译器环境的，包括启动器代号、位数（这些是自定义的）、编译选项、启动设置、编译模式等

"cppStandard": "c++17" 这个涉及静态检查

```cpp
{
    "configurations": [
        {
            "name": "Mac",
            "includePath": [
                "${workspaceFolder}/**"
            ],
            "defines": [],
            "macFrameworkPath": [
                "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks"
            ],
            "compilerPath": "/usr/bin/clang",
            "cStandard": "c17",
            "cppStandard": "c++17",
            "intelliSenseMode": "macos-clang-x64"
        }
    ],
    "version": 4
}
```

### Windows
