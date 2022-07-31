# VSCode

## 一、快捷键

| 用途                             | mac按键             | win按键          |
| -------------------------------- | ------------------- | ---------------- |
| 选中的每行加上光标               | shift + option + i  |                  |
| 打开新窗口                       | shift + command + n |                  |
| 进行代码页面切换                 |                     | alt + 1 2 3      |
| 打开终端                         |                     | ctrl + 反引号    |
| 返回当前代码页面                 |                     | ctrl + 1         |
| 目录页面和代码页面切换           |                     | ctrl + shift + e |
| 一次性找出文所有的当前选中的单词 | shift + command + l | ctrl + shift + l |
| 依次找出文中所有的当前选中的单词 | command + d         | ctrl + d         |
| 格式化文档                       | shift + option + f  |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |
|                                  |                     |                  |

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

### 1、setting.json

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
    "latex-workshop.view.pdf.viewer": "tab",
    "security.workspace.trust.untrustedFiles": "open",
    "editor.formatOnSave": true,
    "C_Cpp.clang_format_style": "{BasedOnStyle: Google, AccessModifierOffset: -4, IndentWidth: 4, ColumnLimit: 0, NamespaceIndentation: All}"
}
```

### 2、tasks.json

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

### 3、launch.json

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

### 4、c_cpp_properties.json

用于配置编译器环境的，包括启动器代号、位数（这些是自定义的）、编译选项、启动设置、编译模式等

"cppStandard": "c++17" 这个涉及静态检查

```c++
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

