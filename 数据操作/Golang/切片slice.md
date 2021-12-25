# 切片 slice

Go 语言切片是对数组的抽象。**类似 Python 里面的列表**

Go 数组的长度不可改变，在特定场景中这样的集合就不太适用，Go 中提供了一种灵活，功能强悍的内置类型切片(**动态数组**)，与数组相比切片的长度是不固定的，可以追加元素，在追加时可能使切片的容量增大。

## 声明切片

make([]type, length, capacity)

length: 切片长度

capacity: 切片容量，可选参数

```go
var slice []int
fmt.Println(slice, len(slice), cap(slice))
// [] 0 0
// slice := []string{} 效果一样

var slice1 []int = make([]int, 5)
// [0 0 0 0 0] 5 5

slice2 := make([]int, 4) // 常用
// [0 0 0 0] 4 4

slice3 := make([]int, 4, 5)
// [0 0 0 0] 4 5
```

## 直接初始化切片

直接初始化切片，**[]** 表示是切片类型，**{1,2,3}** 初始化值依次是 **1,2,3**，其 **cap=len=3**

```go
slice := []int{1, 2, 3}  // 常用
// [1 2 3] 3 3

slice1 := []string{"jack", "mark", "nick"}
// [jack mark nick] 3 3

// 创建长度和容量都是5的切片，并将第5个元素赋值为0，其余值为默认值0
slice2 := []int{4: 0}
// [0 0 0 0 0] 5 5

slice3 := []int{4: 2}
// [0 0 0 0 2] 5 5
```

**注：**如果在 [] 运算符里指定了一个值，那么创建的就是数组。 [] 中不指定值的时候，创建的才是切片

```go
slice := []int{1, 2, 3}
fmt.Println(slice, len(slice), cap(slice))
// [1 2 3] 3 3 切片

array := [3]int{1, 2, 3}
fmt.Println(array, len(array), cap(array))
// [1 2 3] 3 3 数组
```

## 遍历

```go
slice := []string{"a", "b", "c", "d", "e"}
for i, v := range slice {
    fmt.Println("idx:", i, "val:", v)
}
// idx: 0 val: a
// idx: 1 val: b
// idx: 2 val: c
// idx: 3 val: d
// idx: 4 val: e
```

## 截取

 ```go
slice := []string{"a", "b", "c", "d", "e"}
fmt.Println(slice, len(slice), cap(slice))
// [a b c d e] 5 5

t := slice[1]
fmt.Println(t) // b

sl1 := slice[2:]
sl2 := slice[1 : len(slice)-2]       // 没有python的[:-2] 用法
fmt.Println(sl1, len(sl1), cap(sl1)) // [c d e] 3 3
fmt.Println(sl2, len(sl2), cap(sl2)) // [b c] 2 4
 ```

## 添加

```go
slice := []string{}
fmt.Println(slice, len(slice), cap(slice))
// [] 0 0

sl1 := append(slice, "a")
fmt.Println(slice, len(slice), cap(slice)) // [] 0 0
fmt.Println(sl1, len(sl1), cap(sl1))       // [a] 1 1

slice = append(slice, "a", "b", "c")       // 注意不用:，赋值给原切片
fmt.Println(slice, len(slice), cap(slice)) // [a b c] 3 3
```

## 浅、深拷贝

```go
slice := []string{"a", "b", "c", "d", "e"}

// 浅拷贝
sl1 := slice
sl2 := slice[:]
sl3 := slice[1:4]

// 深拷贝 copy，需提前申请空间
sl4 := make([]string, 4, 4)
sl5 := make([]string, 5, 5)
copy(sl4, slice)
copy(sl5, slice)

slice[1] = "Kevin"

fmt.Println(slice)                   // [a Kevin c d e]
fmt.Println(sl1)                     // [a Kevin c d e]
fmt.Println(sl2)                     // [a Kevin c d e]
fmt.Println(sl3, len(sl3), cap(sl3)) // [Kevin c d] 3 4
fmt.Println(sl4)                     // [a b c d]
fmt.Println(sl5)                     // [a b c d e]
```

