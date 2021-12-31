# Golang 字符串 string

[文档](https://zhuanlan.zhihu.com/p/143352497)

golang当中的字符串本质是**只读的字符型数组**，和C语言当中的char[]类似，但是golang为它封装了一个变量类型，叫做string。与python的字符串一样，**不允许修改**

```go
var str string
str1 := "hello world"
var str2 = "hello 世界"

// 统计长度，如果含中文需要将string转化成rune数组
fmt.Println(len(str1))         // 11
fmt.Println(len(str2))         // 12 在utf-8编码当中，一个汉字需要3个字节编码
fmt.Println(len([]rune(str2))) // 8

// 拼接
c := str1 + str2
fmt.Println(c) // hello worldhello 世界

// 截取
fmt.Println(c[3:]) // lo worldhello 世界
```

## **字符串运算**

字符串本身的一些操作，有一个专门的包叫做 `strings`

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	str1 := "ab"
	str2 := "bcd sub"

	// 字符串比较
	// -1 表示str1字典序小于str2，0 表示str1字典序等于str2，1 表示str1字典序大于str2
	cmp := strings.Compare(str1, str2)
	fmt.Println(cmp) // -1

	// 查找函数
	// Index 返回第一次出现的位置，如果不存在返回-1
	// LastIndex，返回出现的最后一个位置，不存在返回-1.
	idx := strings.Index(str2, "sub")
	lastIdx := strings.LastIndex(str2, "last")
	fmt.Println(idx, lastIdx) // 4 -1

	// 统计子串在整体当中出现的次数
	cnt := strings.Count("abcabc", "abc")
	fmt.Println(cnt) // 2

	// 重复字符串
	repeat := strings.Repeat("abc", 3)
	fmt.Println(repeat) // abcabcabc

	// 替换字符串中的部分
	// 接收四个参数，分别是字符串，匹配串和目标串，还有替换的次数(小于0，全部替换)
	rp1 := strings.Replace("aaaddc", "a", "x", 2)
	rp2 := strings.Replace("aaaddc", "a", "x", -1)
	fmt.Println(rp1, rp2) // xxaddc xxxddc

	// 分割字符串，返回字符串切片 []string
	spl := strings.Split("a,b,c", ",")
	fmt.Println(spl) // [a b c]

	// 拼接字符串数组
	str3 := strings.Join([]string{"aa", "bb", "cc"}, ",")
	fmt.Println(str3) // aa,bb,cc

	// 判断字符串首、尾
	str4 := "test"
	fmt.Println(strings.HasPrefix(str4, "te")) // true
	fmt.Println(strings.HasSuffix(str4, "st")) // true

	// 转大、小写
	str5 := strings.ToUpper("Test")
	str6 := strings.ToLower("Test")
	fmt.Println(str5, str6) // TEST test
}
```

## 类型转换

`strconv` 库，用来实现字符串的一些转换操作

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	// 字符串 -> 整数、浮点数
	v1, _ := strconv.Atoi("123")
	v2, _ := strconv.ParseInt("123", 10, 32)
	v3, _ := strconv.ParseFloat("33.33", 32) // 第二个参数是bit的大小
	fmt.Println(v1, v2, v3)                  // 123 123 33.33000183105469

	// 整数 -> 字符串，浮点数转看文档
	str1 := strconv.Itoa(180)          // 转成10进制
	str2 := strconv.FormatInt(180, 16) // 转成16进制
	fmt.Println(str1, str2)

	// 字符串 -> bool型
	str3 := strconv.FormatBool(true)
	str4 := strconv.FormatBool(false)
	fmt.Println(str3, str4) // true false
}
```

