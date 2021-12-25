# map

- map 是无序的
- map 是使用 hash 表来实现的

```golang
package main

import "fmt"

func main() {
	// 创建哈希表，如果不初始化 map，那么就会创建一个 nil map。nil map 不能用来存放键值对
	// var hashMap map[string]string
	// hashMap = make(map[string]string) // 初始化 map

	// 创建哈希表的同时赋值
	// hashMap := map[string]string{"France": "Paris", "Italy": "Rome", "Japan": "Tokyo"}

	// 创建并初始化哈希表
	hashMap := make(map[string]string)

	// 赋值
	hashMap["France"] = "巴黎"
	hashMap["Italy"] = "罗马"
	hashMap["Japan"] = "东京"

	// 遍历
	for key := range hashMap {
		fmt.Println(key, "首都是：", hashMap[key])
	}

	// 查看元素在集合中是否存在
	val, ok := hashMap["France"]
	fmt.Println(val, ok) // 巴黎 true
	val_, ok_ := hashMap["American"]
	fmt.Println(val_, ok_) //  false

	// 删除集合的元素
	delete(hashMap, "France")

	// 获取键
	keys := make([]string, 0, len(hashMap))
	for k := range hashMap {
		keys = append(keys, k)
	}
	fmt.Println("哈希表中的键为：", keys)
}
```
