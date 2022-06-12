# Android 系统

## Overview

- 应用视角的操作系统
  - 对象 + API
- 硬件视角的操作系统
  - 一个控制了整个计算机硬件的程序

## Android

[Android 官方主页](https://developer.android.google.cn/)

- Linux + Framework + JVM
  - 在 Linux/Java 上做了个二次开发？
  - 并不完全是：Android 定义了应用模型
- 支持 Java 是一个非常高瞻远瞩的决定
  - Qualcomm MSM7201
    - ARMv6 指令集
    - 528MHz x 1CPU, 顺序八级流水线
    - TSMC 90nm
  - “跑个地图都会卡”
    - 但摩尔定律生效了！

## Android Apps

一个运行在 Java 虚拟机 ([Android Runtime](http://aospxref.com/android-12.0.0_r3/xref/art/)) 上的应用程序

- Platform (Framework)
- NDK (Native Development Kit)
- Java Native Interface (C/C++ 代码)

官方文档 (RTFM)

- [Kotlin](https://developer.android.google.cn/kotlin)
- [Platform](https://developer.android.google.cn/reference/packages)
  - [android.view.View](https://developer.android.google.cn/reference/android/view/View): “the basic building block for user interface components”
  - [android.webkit.WebView](https://developer.android.google.cn/reference/android/webkit/WebView) - 嵌入应用的网页
  - [android.hardware.camera2](https://developer.android.google.cn/reference/android/hardware/camera2/package-summary) - 相机
  - [android.database.database](https://developer.android.google.cn/reference/android/database/sqlite/package-summary) - 数据库

### “四大组件”

Activity

- 应用程序的 UI 界面 (Event Driven)
- 存在一个 Activity Stack (应用拉起)

Service

- 无界面的后台服务

Broadcast

- 接受系统消息，做出反应
  - 例如 “插上电源”、“Wifi 断开”

ContentProvider

- 可以在应用间共享的数据存储 (insert, update, query, ...)

应用就是如下的时间循环：

![android-activity](./doc/android-activity.png)

## Android 系统

 ### Platform API 之下：一个 “微内核”

通过 “Binder IPC”

- Remote Procedure Call (RPC)
  - `remote.transact()`
- 在性能优化和易用之间的权衡
  - 注册机制
    - 相比之下，管道/套接字就太 “底层” 了，需要手工管理的东西太多
  - 基于共享内存实现
    - Linux Kernel binder driver
  - 服务端线程池

![android-stack](./doc/android-stack.png)

### 然后……海量的代码

例子：如何杀死一个 Android 进程？

- RTFSC:[ActivityManagerService.java](http://aospxref.com/android-12.0.0_r3/xref/frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java#3688)
  - Android 每个 App 都有独立的 uid
  - 遍历进程表，找到属于 uid 的进程
  - Process.KillProcessGroup
    - [间隔 5ms，连续杀死 40 次](http://aospxref.com/android-12.0.0_r3/xref/system/core/libprocessgroup/processgroup.cpp#411)，防止数据竞争
    - Operating System Transactions 的必要性

那么，我们是不是就可以利用数据竞争进程保活了呢？

- 成为孤儿进程从而不会立即收到 SIGKILL 信号
- 在被杀死后立即唤醒另一个进程:[flock-demo.c](http://jyywiki.cn/pages/OS/2022/demos/flock-demo.c)
  - [A lightweight framework for fine-grained lifecycle control of Android applications](https://dl.acm.org/doi/10.1145/3302424.3303956) (EuroSys'19); “diehard apps”

### 一个真正的 “操作系统”

adb (Android Debug Bridge)

- adb push/pull/install
- adb shell
  - screencap /sdcard/screen.png
  - sendevent
- adb forward
- adb logcat/jdwp

一系列衍生的工具

- 开发者选项
- scrcpy
- Monkey/UI Automator

## 总结

本次课回答的问题

- **Q**: 一个真正 “实用” 的操作系统 (生态) 是如何构成的？

Takeaway messages

- 服务、服务、服务
  - Android Platform API
  - Google Mobile Service (GMS)
  - 海量的工程细节
- 复杂系统无处不在
  - 能驾驭整个系统复杂性的架构师
  - 大量高水准的工程师，他们都在哪里？