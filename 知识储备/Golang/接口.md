# Golang interface

## 一、概念

interface是「一组方法签名的组合」，这些方法没有具体的实现代码

interface可以被任意对象实现，一个对象也可以实现多个interface

如果某个对象实现了某个接口的所有方法，则此对象就实现了此接口

任意类型都实现了空interface（也就是包含0个method的interface），空interface可以存储任意类型的值。

- **Go 类型系统的核心：根据类型可以执行的「操作」来设计抽象，而不是其所能容纳的数据类型**

- **Go interface最大特色：「隐式实现」，不用显示指定类型实现了什么接口**

- **用 interface 实现泛型编程**

[interface 源码分析](https://blog.csdn.net/weixin_34007020/article/details/88025102)

## 二、基本使用

```go
package main

import "fmt"

/*其他包中定义*/
type Animal interface {
	Eat(int) string
	Say()
}

/*其他包中定义*/

type Dog struct {
	weight int
}

type Cat struct {
	weight int
}

type Pig struct {
	weight int
}

func (d *Dog) Say() {
	fmt.Println("Wang Wang")
}

func (d *Dog) Eat(food int) string {
	d.weight += food
	fmt.Printf("After eat, dog weight:%d\n", d.weight)
	return "dog eat Good"
}

func (c *Cat) Say() {
	fmt.Println("Miao Miao")
}

func (d *Cat) Eat(food int) string {
	d.weight += food
	fmt.Printf("After eat, cat weight:%d\n", d.weight)
	return "cat eat Good"
}

func (c *Pig) Say() {
	fmt.Println("Heng Heng")
}

func main() {
	// 使用方法一
	var animal Animal = &Dog{}
	animal.Say()         // Wang Wang
	res := animal.Eat(5) // After eat, dog weight:5
	fmt.Println(res)     // dog eat Good

	animal = &Cat{}
	animal.Say() // Miao Miao
	// animal = &Pig{} // 报错，因为 Pig 没有实现 Eat 方法，所以没有实现 Animal 接口

	// 使用方法二
	cat := Cat{}
	Animal.Say(&cat)           // Miao Miao
	res = Animal.Eat(&cat, 10) // After eat, cat weight:10
	fmt.Println(res)           // cat eat Good

	// 用法三
	animals := []Animal{&Dog{}, &Cat{}}
	for _, ani := range animals {
		ani.Say()
	}
	// Wang Wang
	// Miao Miao
}
```



## 三、为什么要用接口

### 1、泛型编程 writing generic algorithm

```go
package main

import "fmt"

/*其他包中定义*/
type Animal interface {
	Eat(int) string
	Say()
}

/*其他包中定义*/

type Dog struct {
	name   string
	weight int
}

func (d *Dog) Say() {
	fmt.Printf("%s: Wang Wang\n", d.name)
}

func (d *Dog) Eat(food int) string {
	d.weight += food
	fmt.Printf("%s: weight:%d\n", d.name, d.weight)
	return d.name + ": eat Good"
}

func doJob(animal Animal) {
	// 这里的逻辑是通用的
	animal.Say()
	res := animal.Eat(2)
	fmt.Println(res)
}

func main() {
	var dog1 Animal = &Dog{name: "dodo"}
	var dog2 Animal = &Dog{name: "xixi"}

	doJob(dog1)
	// dodo: Wang Wang
	// dodo: weight:2
	// dodo: eat Good
	doJob(dog2)
	// xixi: Wang Wang
	// xixi: weight:2
	// xixi: eat Good
}
```

### 2、隐藏具体实现 hiding implementation detail

隐藏具体实现，这个很好理解。比如我设计一个函数给你返回一个 interface，那么你只能通过 interface 里面的方法来做一些操作，但是内部的具体实现是完全不知道的。

我们常用的 context 包，就是这样的，context 最先由 google 提供，现在已经纳入了标准库，而且在原有 context 的基础上增加了：cancelCtx，timerCtx，valueCtx

**文件1：描述了Animal接口**

```go
type Animal interface {
	Say()
	Eat(int) string
}
```

**文件二：Dog和Cat两个结构体实现了Animal接口**

```go
type Dog struct {
	Animal
	name   string
	weight int
	sex    bool
}

type Cat struct {
	Animal
	name   string
	weight int
}

/*隐藏了下面👇具体实现*/
func (d *Dog) Say() {
	fmt.Printf("%s father: %v\n", d.name, d.Animal)
}

func (d *Dog) Eat(food int) string {
	d.weight += food
	fmt.Printf("%s: weight:%d\n", d.name, d.weight)
	return d.name + ": eat Good"
}
func (c *Cat) Say() {
	fmt.Printf("%s father: %v\n", c.name, c.Animal)
}

func (c *Cat) Eat(food int) string {
	c.weight += food
	fmt.Printf("%s: weight:%d\n", c.name, c.weight)
	return c.name + ": eat Good"
}
/*隐藏了上面👆具体实现*/
```

**文件三：业务代码**

开发业务代码时（main函数中），尽管 WithDog 和 WithCat 返回的具体结构体不一样，但对于使用dog或者cat的人「完全无感知」

隐藏了方法Say、Eat的具体实现，也隐藏了Dog内很多用户不需要关注的字段（例如sex）

用户只用知道 Dog 和 Cat 实现了Animal接口，就直接看接口的中描述方法（只用看文件1），就会使用 dog 和 cat 了

```go
func WithDog(father Animal) (child Animal) {
	dog := Dog{Animal: father, name: "dodo", weight: 10}
	dog.Eat(4)
	return &dog
}

func WithCat(father Animal) (child Animal) {
	cat := Cat{Animal: father, name: "xixi", weight: 10}
	cat.Eat(8)
	return &cat
}

func main() {
  // 业务代码
	dog := WithDog(&Dog{}) // dodo: weight:14
	dog.Say()              // dodo father: &{<nil>  0 false}

	dog = WithDog(dog) // dodo: weight:14
	dog.Say()          // dodo father: &{0xc000100030 dodo 14 false}

	cat := WithCat(&Cat{}) // xixi: weight:18
	cat.Say()              // xixi father: &{<nil>  0}
}
```



### 3、providing interception points

还不理解



## 四、interface{} 类型

`interface{}` 类型，**空接口**，是导致很多混淆的根源。`interface{}` 类型是没有方法的接口。由于没有 `implements` 关键字，所以所有类型都至少实现了 0 个方法，所以 **所有类型都实现了空接口**。这意味着，如果您编写一个函数以 `interface{}` 值作为参数，那么您可以为该函数提供任何值。例如：

```go
package main

import (
	"fmt"
)

func PrintAll(vals []interface{}) {
	for _, val := range vals {
		fmt.Println(val)
	}
}

func main() {
	names := []string{"stanley", "david", "oscar"}
	vals := make([]interface{}, len(names))
	for i, v := range names {
		vals[i] = v
	}
	PrintAll(vals)
}
```

