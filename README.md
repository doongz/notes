# 今天学习的人

***今天学习的人***  

> 是未来之星  
> 是国家「栋」梁  
> 是自然界的丛林之王  
> 是俗语里的下凡仙子  
> 是粤语里的巴鸠撚闭  
> 是成语里面的学富五车  
> 是武侠小说里的人中龙  
> 是都市小说里的城市之光  
> 是吾日三省吾身的自律者  
> 是相亲节目里面的心动嘉宾  
> 是世间所有丑与恶的唾弃者  
> 是世间所有美与好的创造者  

<p>
    <a>
        <img src="https://img.shields.io/badge/mardown-writing-white?logo=markdown" />
    </a>
    <a>
        <img src="https://img.shields.io/github/license/dowalle/algo?color=white" />
    </a>
    <a>
        <img src="https://img.shields.io/github/workflow/status/dowalle/algo/Markdown-CI?color=white&logo=github" />
    </a>
    <a>
        <img src="https://img.shields.io/github/repo-size/dowalle/algo?color=white&logo=git&logoColor=white" />
    </a>
    <a>
        <img src="https://img.shields.io/github/stars/dowalle/algo?color=white&logo=github" />
    </a>
    <a>
        <img src="https://img.shields.io/github/last-commit/dowalle/algo?color=white&logo=github" />
    </a>
    <a>
        <img src="https://img.shields.io/github/commit-activity/m/dowalle/algo?color=white&logo=github" />
    </a>
</p>

## Contents

### 第一章 [算法](https://dowalle.gitbook.io/algo/algorithm)

- [前述](https://dowalle.gitbook.io/algo/algorithm/0-qian-shu)  `刷题经验`  `C++调试模版`  `常见报错`
- [数据结构](https://dowalle.gitbook.io/algo/algorithm/1-shu-ju-jie-gou)
  - [概述](./Algorithm/1-数据结构/0-概述.md)  `基本概念`  `算法评价`
  - [线性表](./Algorithm/1-数据结构/1-线性表.md)  `顺序存储(数组)`  `环状数组`  `链式存储(链表)`  `哨兵`  `多画`  `舍得变量`  `双指针`  `环状链表`  `Medium`
  - [栈](./Algorithm/1-数据结构/2-栈.md)  `顺序、链式存储`  `单调栈`  `括号匹配`  `表达式求值`  `递归`  `移除问题`   `Medium`
  - [队列](./Algorithm/1-数据结构/3-队列.md)  `顺序、链式、双端`  `单调队列`  `层遍历`  `Medium`
  - [字符串「未完工」](./Algorithm/1-数据结构/4-字符串.md)  `顺序、堆分配、块链存储`  `KMP算法`
  - [树 & 二叉树](./Algorithm/1-数据结构/5-树和二叉树.md)  `树的种类`  `二叉树遍历(前序、中序、后序、层)`  `二叉树构造「未完工」`   `线索二叉树`  `Easy`
    - [排序树 & 平衡树 & 搜索树「未完工」](./Algorithm/1-数据结构/5-排序树&平衡树&搜索树.md)  `AVL树`  `红黑树`  `查找、插入、删除 O(logn)`
    - [B树 & B+树「未完工」](./Algorithm/1-数据结构/5-B树&B+树.md)
    - [并查集](./Algorithm/1-数据结构/5-并查集.md)  `连通`  `连通分量`  `连通性判断`  `添加、连通、查找O(logn)`  `Medium`
    - [树状数组 & 线段树](./Algorithm/1-数据结构/5-树状数组&线段树.md)  `维护区间信息`  `单点更新O(logn)`  `区间查询O(logn)`  `Hard+`
    - [字典树](./Algorithm/1-数据结构/5-字典树.md)  `前缀树`  `字符串/字符前缀是否存在`  `dfs`  `Hard`
    - [哈夫曼树「未完工」](./Algorithm/1-数据结构/5-哈夫曼树.md)
  - [散列表](./Algorithm/1-数据结构/6-散列表.md)  `哈希表`  `本质-数组`  `核心-散列函数`  `哈希冲突`  `扩容`  `查找`
  - [堆](./Algorithm/1-数据结构/7-堆.md)  `优先队列`  `大/小根堆`  `TopK`  `多路归并`  `中位数`  `插入O(logn)`  `查找O(1)`  `删除O(logn)`  `Hard`
- [算法基础](https://dowalle.gitbook.io/algo/algorithm/2-suan-fa-ji-chu)
  - [排序](./Algorithm/2-算法基础/1-排序.md)  `选择O(n^2)`  `冒泡O(n^2)`  `插入O(n^2)`  `计数O(n)`  `桶O(n)`  `快速O(nlogn)「未完工」`  `归并O(nlogn)`  `外部排序「未完工」`  `Hard`
  - [二分法](./Algorithm/2-算法基础/2-二分法.md)  `不可套模版`  `二段性`  `寻找一个数`  `lower_bound`  `upper_bound`  `O(logn)`  `三分`  `Hard+`
  - [双指针](./Algorithm/2-算法基础/3-双指针.md)  `快慢双指针`  `左右双指针`  `前后双指针`  `指向各自集合的双指针`  `Floyd判圈算法`  `时O(n)`  `空O(1)`  `Medium`
  - [滑动窗口](./Algorithm/2-算法基础/4-滑动窗口.md)  `单调性`  `窗口数据结构`  `右边届入窗`  `左边届收缩`  `延时删除`  `采集答案`  `步长`  `起始位置`  `Medium`
  - [前缀和](./Algorithm/2-算法基础/5-前缀和.md)  `相减`  `哈希表`  `二维前缀和`  `前缀和思想`
  - [差分](./Algorithm/2-算法基础/6-差分.md)  `两端操作`  `操作区间从O(k)降至O(1)`  `二维差分`
  - [贪心](./Algorithm/2-算法基础/7-贪心.md)  `排序预处理`  `区间调度问题`  `跳跃问题`  `环形贪心`  `堆`  `单调栈`  `Hard`
  - [位运算](./Algorithm/2-算法基础/8-位运算.md)  `异或`  `奇偶`  `除2`  `求中值`  `平均数`  `交换值`  `加法`  `1个数`
  - [分治](./Algorithm/2-算法基础/9-分治.md)  `分解 -> 解决 -> 合并`
- [动态规划](https://dowalle.gitbook.io/algo/algorithm/3-dong-tai-gui-hua)
  - [动态规划基础](./Algorithm/3-动态规划/0-动态规划基础.md)  `三要素(重复子问题、最优子结构、动态转移方程)`  `斐波那契数列`  `凑零钱问题`
  - [记忆化搜索](./algo/Algorithm/3-动态规划/1-记忆化搜索.md)  `具备最优子结构`  `具备重叠子问题`  `memo记录子问题`  `子问题构成`
  - [线性 DP「未完工」](./Algorithm/3-动态规划/2-线性DP.md)
  - [背包 DP「未完工」](./Algorithm/3-动态规划/3-背包DP.md)
  - [序列 DP](./Algorithm/3-动态规划/4-序列DP.md)  `无后效性`  `最长上升子序列(LIS)`  `最长公共子序列(LCS)`  `最大子数组和`  `LCS和LIS相互转化`
  - [区间 DP](./Algorithm/3-动态规划/5-区间DP.md)  `f(l,r)=max(f(l,k), f(k+1,r))+cost k in [l,r]`  `遍历方法`  `初始化(dp[i][i]=1)`  `返回(dp[0][i])`  `回文问题`
- [图论「未完工」](https://dowalle.gitbook.io/algo/algorithm/4-tu-lun)
  - [基本知识](./Algorithm/4-图论/1-基本知识.md)
  - [图的存储](./Algorithm/4-图论/2-图的存储.md)  `邻接表`  `邻接矩阵`  `类边`  `一维数组`
  - [图的种类](./Algorithm/4-图论/3-图的种类.md)  `二分图`
  - [DFS](./Algorithm/4-图论/4-DFS.md)  `回溯`  `记忆化dfs`
  - [BFS](./Algorithm/4-图论/5-BFS.md)  `最短路径`  `双向bfs`
  - [拓扑排序](./Algorithm/4-图论/6-拓扑排序.md)  `有向无环图`  `学完a课才能学b课`
  - [最短路径](./Algorithm/4-图论/7-最短路径.md)  `Dijkstra、非负权、O(nlogn)`  `Floyd、多源、O(n^3)`  `Bellman-Ford、负环、O(n^2)`
  - [欧拉图](./Algorithm/4-图论/8-欧拉图.md)  `一笔画完整个图`
- [数学「未完工」]()  `倍增`  `快速幂`  `求余`
  - [计算机算法](./Algorithm/5-数学/计算机算法.md)  `num->arr（短除法）`  `arr->num`  `bin_to_dec`  `dec_to_bin`  `向上取整`
  - [数学算法](./Algorithm/5-数学/数学算法.md)  `高斯求和`  `蓄水池抽样算法`  `洗牌算法`
  - [余数相关性质](./Algorithm/5-数学/余数相关性质.md)  `同余定理`  `加`  `减`  `乘`  `乘方`

### 第二章 [技能](https://dowalle.gitbook.io/algo/skill)

- [C++](https://dowalle.gitbook.io/algo/skill/c++)
  - [基础知识](https://dowalle.gitbook.io/algo/skill/c++/1-ji-chu-zhi-shi)  `GCC`  `数据类型`  `条件`  `循环`  `运算符`  `函数`  `char`  `string`  `数组`  `指针`  `shared_ptr`  `引用`  `struct`  `namespace`  `头文件`  `链接库`  `异常处理`  `输入输出流`  `文件操作`  `多文件编程`
  - [面向对象](https://dowalle.gitbook.io/algo/skill/c++/2-mian-xiang-dui-xiang)  `类和对象`  `继承和派生`  `多态与虚函数`  `运算符重载`  `模版和范型`
  - [标准模版库](https://dowalle.gitbook.io/algo/skill/c++/3-biao-zhun-mo-ban-ku)  `vector`  `deque`  `multimap`  `multiset`  `unordered_map`  `unordered_set`  `queue`  `priority_queue`  `algorithm`
  - [C语言内存](https://dowalle.gitbook.io/algo/skill/c++/4c-yu-yan-nei-cun)  `虚拟内存`  `内存对齐`  `内存分页`  `MMU`  `内存模型`  `内核模式`  `用户模式`  `栈`  `堆`  `动态内存分配`  `内存池`  `野指针`  `内存泄漏`
- [Golang](https://dowalle.gitbook.io/algo/skill/golang)
  - [基础知识](https://dowalle.gitbook.io/algo/skill/golang/1-ji-chu-zhi-shi)   `string`  `slice`  `map`  `struct`  `指针`  `interface`
  - [Go语言并发](https://dowalle.gitbook.io/algo/skill/golang/2go-yu-yan-bing-fa)  `go`  `chan`  `WaitGroup`  `如何实现`  `sync.Mutex`  `sync.RWMutex`  `atomic`  `死锁`
  - [go tool「未完工」]()
  - [进阶知识](https://dowalle.gitbook.io/algo/skill/golang/3-jin-jie-zhi-shi)  `常见GC算法`  `Go GC`  `观察GC`  `内存泄漏`  `GC调优`
  - [实用函数](https://dowalle.gitbook.io/algo/skill/golang/4-shi-yong-han-shu)  `计时器`
- [Python](https://dowalle.gitbook.io/algo/skill/python)  `str`  `list`  `set`  `tuple`  `dict`  `defaultdict`  `deque`  `bisect`  `heapq`  `SortedList`  `__lt__`
- [Linux](https://dowalle.gitbook.io/algo/skill/linux)
  - [filesystem](./Skill/Linux/filesystem)  `overlayfs`  `shared-subrees`
- [开发软件](https://dowalle.gitbook.io/algo/skill/kai-fa-ruan-jian)  `开发`  `创作`  `效率`  `文献`  `vscode`  `git`  `vim`
- [后端软件](https://dowalle.gitbook.io/algo/skill/hou-duan-ruan-jian)  
  - [docker 原理](./Skill/后端软件/1-docker原理.md)  `Namespace(进程、网络、存储)`  `CGgroups`  `UnionFS`
  - [k8s 原理](./Skill/后端软件/2-k8s原理.md)  `介绍`  `设计`  `架构(master、worker)`  `实现(对象、pod、控制器)`
  - [k8s 详解「未完工」](https://dowalle.gitbook.io/algo/skill/hou-duan-ruan-jian/k8s-xiang-jie)  `pod`  `service`  `volume`  `replicaSet`
  - [CLI](https://dowalle.gitbook.io/algo/skill/hou-duan-ruan-jian)  `docker CLI`  `k8s CLI`  `ceph CLI`
- [Markdown](./Skill/Markdown/README.md)
- [LaTeX](https://dowalle.gitbook.io/algo/skill/latex)
  - [数学符号](./Skill/LaTeX/1-数学符号.md)  `运算符`  `关系符`  `定界符`  `箭头`  `希腊字母`  `常用符号`  `重音符`
  - [公式格式](./Skill/LaTeX/2-公式格式.md)  `求和`  `分数`  `大括号`  `等号对齐`
- [Mermaid](./Skill/Mermaid/README.md)  `流程图`  `时序图`  `甘特图`  `类图`  `状态图`  `饼图`  `用户体验旅程图`


### 第三章 [知识](https://dowalle.gitbook.io/algo/knowledge)

> *系统性的理解一门学科，更利于产生「兴趣」，培养「创造性」思维*

- [计算机组成](https://dowalle.gitbook.io/algo/knowledge/1-ji-suan-ji-zu-cheng)
  - [序](./Knowledge/1-计算机组成/0-序.md)  `大纲`  `程序是如何在计算机里跑起来的`
  - [计算机系统概述](./Knowledge/1-计算机组成/1-计算机系统概述.md)  `软硬件分类及发展`  `冯•诺依曼结构`  `工作过程`  `性能指标`
  - [数据的表示和运算](./Knowledge/1-计算机组成/2-数据的表示和运算.md)  `数制`  `定点数`  `浮点数`  `算术逻辑单元`
  - [存储系统](./Knowledge/1-计算机组成/3-存储系统.md)  `分类`  `性能指标`  `层次化结构`  `SRAM(cache)`  `DRAM(内存)`  `ROM(闪存、固态)`  `MM组成和使用`  `Cache`  `虚拟存储器`
  - [指令系统](./Knowledge/1-计算机组成/4-指令系统.md)  `指令(操作码+地址码)`  `指令寻址`  `数据寻址`  `指令集`  `CISC`  `RISC`
  - [中央处理器](./Knowledge/1-计算机组成/5-中央处理器.md)  `CPU(运算器+控制器)`  `指令执行`  `数据通路`  `硬布线控制器`  `微程序控制器`  `指令流水线`
  - [总线](./Knowledge/1-计算机组成/6-总线.md)  `片内、系统、通信总线`  `性能指标`  `总线仲裁`  `传输和定时`  `总线标准`
  - [输入输出系统](./Knowledge/1-计算机组成/7-输入输出系统.md)  `外部设备`  `IO接口`  `IO方式(查询、中断、DMA)`
- [操作系统](https://dowalle.gitbook.io/algo/knowledge/2-cao-zuo-xi-tong)
  - [计算机系统概述](./Knowledge/2-操作系统/1-计算机系统概述.md)  `目的(管理、调度软硬资源、提供接口)`  `特征(并发、共享、虚拟、异步)`  `分类`  `运行环境(内核态、用户态)`  `中断`  `系统调用`
  - [进程管理](./Knowledge/2-操作系统/2-进程管理.md)  `进程(程序段、数据段、进程控制块)`  `目的(并发、共享)`  `进程通信`  `线程(ID、计数器、寄存器集合)`  `目的(减少开销)`  `实现方式(用户级、内核级)`  `处理机调度`  `进程同步`  `互斥`  `死锁`  `饥饿`
  - [进程 & 线程 & 协程](./Knowledge/2-操作系统/进程&线程&协程.md)  `时间角度`  `资源角度`
  - [内存管理](./Knowledge/2-操作系统/3-内存管理.md)  `目的(并发)`  `覆盖与交换`  `连续分配`  `非连续分配(分页存储)`  `分段存储`  `虚拟内存`  `局部性原理(时间、空间)`
  - [文件管理](./Knowledge/2-操作系统/4-文件管理.md)  `文件结构`  `目录结构`  `共享`  `保护`  `文件系统结构`  `目录实现`  `文件实现`  `磁盘(结构、调度、管理)`
  - [输入输出管理](./Knowledge/2-操作系统/5-输入输出管理.md)  `IO设备`  `IO控制方式`  `IO层次`  `设备分配、回收`  `Cache(缓存)`  `Buffer(缓冲区)`
- [计算机网络](https://dowalle.gitbook.io/algo/knowledge/3-ji-suan-ji-wang-luo)
  - [计算机网络体系结构](./Knowledge/3-计算机网络/1-计算机网络体系结构.md)  `组成`  `功能`  `分类`  `性能指标`  `OSI模型(7层)`  `TCP/IP模型(4层)`  `5层协议体系`  `报文、包、帧等概念`
  - [物理层](./Knowledge/3-计算机网络/2-物理层.md)  `传输比特流`  `数字信道(基带信号)`  `模拟信道(宽带信号)`  `奈奎斯特定理(码元极限传输速率)`  `香农定理(数据极限传输速率)`  `编码与调制PSK`  `电路、报文、分组交换`  `数据报、虚电路服务`  `传输介质`  `中继器`  `集线器`
  - [数据链路层](./Knowledge/3-计算机网络/3-数据链路层.md)  `数据逻辑上无差错`  `链路管理`  `组帧`  `差错控制`  `流量控制(滑窗)`  `介质访问控制(多路复用、随机访问CSMA)`  `局域网(以太网)`  `IEEE 802.3/11`  `网卡(MAC地址)`  `广域网(交换机+链路)`  `网桥`  `以太网交换机`
  - [网络层](./Knowledge/3-计算机网络/4-网络层.md)  `功能(异构互联、分组转发、拥塞控制)`  `路由算法`  `IPv4`  `IP数据报`  `IP地址`  `子网`  `IPv6`  `路由协议`  `IP组播`  `移动IP`  `路由器`
  - [传输层](./Knowledge/3-计算机网络/5-传输层.md)  `功能(进程间通信)`  `端口`  `socket(嵌套字)`  `UDP(无连接)`  `TCP(连接)`  `报文段`  `TCP建立连接(三次挥手)`  `TCP释放连接(四次握手)`  `可靠传输`  `流量控制`  `拥塞控制`
  - [应用层](./Knowledge/3-计算机网络/6-应用层.md)  `网络应用模型(C/S、P2P)`  `DNS`  `FTP`  `电子邮件(SMTP、POP3/IMAP)`  `万维网(HTTP)`  `Cookie`
- [数据 & 存储](https://dowalle.gitbook.io/algo/knowledge/4-shu-ju-cun-chu)
  - [设计数据密集型应用「未完工」](https://dowalle.gitbook.io/algo/knowledge/4-shu-ju-cun-chu/1-she-ji-shu-ju-mi-ji-xing-ying-yong)
  - [数据库](https://dowalle.gitbook.io/algo/knowledge/4-shu-ju-cun-chu/2-shu-ju-ku)  `关系型数据库`  `NoSQL`
  - [消息队列](https://dowalle.gitbook.io/algo/knowledge/4-shu-ju-cun-chu/3-xiao-xi-dui-lie)
- [面向对象「未完工」](https://dowalle.gitbook.io/algo/knowledge/5-mian-xiang-dui-xiang)  `多态和多态性`  `设计模式`

### 第四章 [数学](https://dowalle.gitbook.io/algo/math)

> *2016年留存下来的手稿，再翻开时已是2022年*

- [微积分](https://dowalle.gitbook.io/algo/math/wei-ji-fen)  `微分->趋势->时间`  `积分->面积(概率)->空间`
  - [极限](./Math/微积分/1-极限.md)
  - [一元函数微积分](./Math/微积分/2-一元函数微积分.md)
  - [多元函数微分学](./Math/微积分/3-多元函数微分学.md)
  - [二重积分](./Math/微积分/4-二重积分.md)
  - [微分方程](./Math/微积分/5-微分方程.md)
- [线性代数](https://dowalle.gitbook.io/algo/math/xian-xing-dai-shu)
  - [行列式](./Math/线性代数/1-行列式.md)
  - [矩阵](./Math/线性代数/2-矩阵.md)
  - [向量组与方程组](./Math/线性代数/3-向量组与方程组.md)
  - [特征与二次型](./Math/线性代数/4-特征与二次型.md)

### 第五章 [面试](https://dowalle.gitbook.io/algo/interview)

- [找工作经验](https://dowalle.gitbook.io/algo/interview/1-zhao-gong-zuo-jing-yan)
- [面经](https://dowalle.gitbook.io/algo/interview/2-mian-jing)

### 第六章 竞赛

> *得到一点点「感悟」比得到答案更重要*

## TODO

- [ ] 单调栈 [概念](https://www.jianshu.com/p/6bbd3653a57f) [题目](https://leetcode-cn.com/problems/longest-well-performing-interval/solution/can-kao-liao-ji-ge-da-shen-de-ti-jie-zhi-hou-zong-/)
- [ ] 矩阵快速幂

## Usage

[Generate SUMMARY.md](https://github.com/imfly/gitbook-summary) for gitbook:

```shell
book sm
```

## Statement

> *「学习」唯有靠自己的积累和总结，其他所有的资料和题解都只是参考，包括此仓库也仅用作自己的积累*

`感谢`  大家不用 Star

`发布`  于 [Gitbook](https://dowalle.gitbook.io/algo/)

`侵删`  本仓库全部为自己总结，部分来源于 [oi-wiki](https://oi-wiki.org) | [leetcode](https://leetcode-cn.com/problemset/all/) | [luogu](https://www.luogu.com.cn) | [c-biancheng](http://c.biancheng.net/) | [geeksforgeeks](https://www.geeksforgeeks.org/) | [draveness](https://draveness.me/)

