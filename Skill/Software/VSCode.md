# VSCode

## 一、快捷键

| 按键 | 说明 |
| ---- | ---- |
|      |      |
|      |      |
|      |      |

## 二、代码格式化

### c++

谷歌风格，缩进4字符，访问说明符顶格，行数不受限

```
{BasedOnStyle: Google, AccessModifierOffset: -4, IndentWidth: 4, ColumnLimit: 0, NamespaceIndentation: All}
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
