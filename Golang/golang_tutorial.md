# Go语言完整学习教程（Java开发者进阶版）

> 本教程专为有10年以上Java开发经验的程序员编写，从Java开发者视角出发，系统性地讲解Go语言核心知识点。
> 知识点截止至 **2026年5月（Go 1.25 / 1.26）**。本轮更新覆盖 Go 1.23 引入的迭代器、Go 1.24 的泛型类型别名 / Swiss Tables map / weak 包 / `tool` 指令、Go 1.25 的 container-aware GOMAXPROCS / `testing/synctest` / `sync.WaitGroup.Go` / Green Tea GC 等关键变更。

---

## 目录

- [第一章：Go语言概述与环境搭建](#第一章go语言概述与环境搭建)
- [第二章：基础语法](#第二章基础语法)
- [第三章：复合数据类型](#第三章复合数据类型)
- [第四章：接口与多态](#第四章接口与多态)
- [第五章：错误处理](#第五章错误处理)
- [第六章：并发编程](#第六章并发编程)
- [第七章：泛型](#第七章泛型)
- [第八章：标准库精讲](#第八章标准库精讲)
- [第九章：项目工程化](#第九章项目工程化)
- [第十章：Web开发框架](#第十章web开发框架)
- [第十一章：网络编程与长连接](#第十一章网络编程与长连接)
- [第十二章：性能优化与高级特性](#第十二章性能优化与高级特性)
- [第十三章：实战项目示例](#第十三章实战项目示例)
- [第十四章：Go面试题精选](#第十四章go面试题精选)

---

## 第一章：Go语言概述与环境搭建

### 1.1 Go语言历史

Go语言（又称Golang）由Google于2009年11月正式开源发布，由三位计算机科学界的大师设计：

- **Rob Pike**：Unix团队成员，UTF-8编码的共同发明者
- **Ken Thompson**：Unix和C语言的共同发明者，图灵奖得主
- **Robert Griesemer**：参与过V8 JavaScript引擎和Java HotSpot虚拟机的开发

Go的诞生源于Google内部对C++编译速度慢、Java过于复杂的不满。设计目标是创造一种既有静态语言的安全性和性能，又有动态语言的开发效率的语言。

### 1.2 设计哲学对比

| 维度 | Go | Java |
|------|-----|------|
| 核心理念 | 简洁、正交、组合 | 面向对象、设计模式 |
| 并发模型 | CSP（Goroutine + Channel） | 线程 + 锁（虚拟线程 Java 21+） |
| 继承 | 无继承，用组合 | 类继承体系 |
| 异常处理 | 错误即值，显式处理 | try-catch异常体系 |
| 泛型 | 1.18+引入，约束式泛型 | 类型擦除式泛型 |
| 编译 | 直接编译为机器码，极快 | 编译为字节码，JVM运行 |
| 部署 | 单一静态二进制文件 | 需要JVM环境 |
| GC | 低延迟并发GC（亚毫秒级STW） | 多种GC可选（G1, ZGC等） |

### 1.3 版本历史关键节点

| 版本 | 时间 | 重要特性 |
|------|------|----------|
| Go 1.0 | 2012.03 | 首个稳定版本，兼容性承诺 |
| Go 1.5 | 2015.08 | 自举（编译器由Go重写），并发GC |
| Go 1.11 | 2018.08 | Go Modules实验性支持 |
| Go 1.13 | 2019.09 | 错误包装（%w），Go Modules默认开启 |
| Go 1.14 | 2020.02 | Go Modules生产就绪 |
| Go 1.16 | 2021.02 | embed包，默认启用Modules |
| Go 1.18 | 2022.03 | **泛型**、模糊测试、workspace模式 |
| Go 1.19 | 2022.08 | GOMEMLIMIT，修订内存模型 |
| Go 1.21 | 2023.08 | slog 结构化日志，`min`/`max`/`clear` 内置函数，`cmp.Ordered`，`sync.OnceFunc`/`OnceValue`/`OnceValues` |
| Go 1.22 | 2024.02 | for 循环变量语义修复，`range` over integers，`net/http.ServeMux` 增强路由模式（method + path 参数） |
| Go 1.23 | 2024.08 | **range over func（用户自定义迭代器）**、`iter` 包、`unique` 包、`time.Timer/Ticker` 不再被运行时引用（GC 更友好）、`structs` 包 |
| Go 1.24 | 2025.02 | **泛型类型别名**、Swiss Tables 实现的 map（更快更省内存）、`weak` 包（弱指针）、`runtime.AddCleanup` 替代 `SetFinalizer`、`os.Root` 防目录穿越、JSON `omitzero` tag、`go.mod` 中的 `tool` 指令、`crypto/mlkem`（后量子）、`testing.B.Loop` 改进基准测试 |
| Go 1.25 | 2025.08 | **`testing/synctest`（并发代码确定性测试）**、`sync.WaitGroup.Go`、容器感知的 `GOMAXPROCS`（自动读取 cgroup CPU 配额）、**Green Tea 实验性 GC**、`encoding/json/v2`（实验性）、新的 `runtime.GOROOT()` 行为、`os.CopyFS` |
| Go 1.26 | 预计 2026.02 | （筹划中）继续完善迭代器生态、`encoding/json/v2` 推进、性能优化 |

### 1.4 安装配置

#### 下载安装

从官网 https://go.dev/dl/ 下载对应平台安装包（推荐 Go 1.25.x，截至 2026 年 5 月最新稳定版）。

Windows 安装后验证：

```bash
go version
# go version go1.25.x windows/amd64
```

#### 环境变量

```bash
# 查看Go环境配置
go env

# 关键环境变量
go env GOPATH    # 工作区路径，默认 ~/go
go env GOROOT    # Go安装目录
go env GOPROXY   # 模块代理

# 国内推荐设置代理
go env -w GOPROXY=https://goproxy.cn,direct
go env -w GOPRIVATE=your-company.com
```

#### GOPATH vs Go Modules

**GOPATH时代（已过时）**：所有项目必须放在`$GOPATH/src`下，依赖管理混乱。

**Go Modules时代（当前标准）**：项目可以在任意目录，通过`go.mod`管理依赖。

```bash
# 初始化新项目
mkdir myproject && cd myproject
go mod init github.com/yourname/myproject
```

Java类比：`go.mod`相当于`pom.xml`或`build.gradle`，`go.sum`相当于lock文件。

### 1.5 IDE推荐

| IDE | 优势 | 适合 |
|-----|------|------|
| **GoLand**（JetBrains） | 功能最全，重构强大，调试方便 | IntelliJ用户无缝切换 |
| **VS Code + Go插件** | 免费，轻量，插件生态丰富 | 喜欢轻量级编辑器的开发者 |

GoLand对Java开发者最友好——快捷键、界面布局与IntelliJ IDEA几乎一致。

### 1.6 第一个Go程序

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
```

对比Java：

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}
```

关键差异：
- Go没有类，`main`函数直接属于`main`包
- 没有`public`/`private`关键字，通过首字母大小写控制可见性
- 不需要分号（编译器自动插入）
- 导入的包如果不使用会编译报错（Java只是警告）

### 1.7 go命令行工具

```bash
# 编译并运行（不生成二进制文件）
go run main.go

# 编译生成二进制文件
go build -o myapp main.go

# 运行测试
go test ./...

# 模块管理
go mod init module-name    # 初始化模块
go mod tidy                # 整理依赖（添加缺少的，移除多余的）
go mod download            # 下载依赖到本地缓存
go mod vendor              # 将依赖复制到vendor目录

# 获取依赖
go get github.com/gin-gonic/gin@latest

# 格式化代码
go fmt ./...
# 或使用 goimports（自动管理import）
goimports -w .

# 静态检查
go vet ./...

# 查看文档
go doc fmt.Println

# 性能分析
go test -bench=. -benchmem ./...
```

---

## 第二章：基础语法

### 2.1 变量声明

Go提供多种变量声明方式：

```go
package main

import "fmt"

// 包级变量（不能用 :=）
var globalVar int = 100

func main() {
    // 方式1：完整声明
    var name string = "Go"
    
    // 方式2：类型推断
    var age = 25
    
    // 方式3：短变量声明（最常用，仅限函数内部）
    city := "Beijing"
    
    // 方式4：批量声明
    var (
        x int    = 1
        y string = "hello"
        z bool   // 零值：false
    )
    
    // 多重赋值
    a, b := 10, 20
    a, b = b, a  // 交换，无需临时变量
    
    fmt.Println(name, age, city, x, y, z, a, b)
}
```

**Java对比**：Go的`:=`相当于Java的`var`（Java 10+局部变量类型推断），但更简洁。Go变量声明后必须使用，否则编译错误。

#### 零值（Zero Value）

Go的所有变量声明后都有确定的零值（Java中基本类型也有默认值，但引用类型是null）：

| 类型 | 零值 |
|------|------|
| int, float | 0 |
| string | "" |
| bool | false |
| pointer, slice, map, channel, func, interface | nil |

### 2.2 基本数据类型

```go
// 整数类型
var i int       // 平台相关：32位系统是int32，64位系统是int64
var i8 int8     // -128 ~ 127
var i16 int16   // -32768 ~ 32767
var i32 int32   // -2^31 ~ 2^31-1（等同于Java的int）
var i64 int64   // -2^63 ~ 2^63-1（等同于Java的long）
var u uint      // 无符号整数（Java没有无符号类型）
var u8 uint8    // 0 ~ 255，等同于 byte
var u32 uint32
var u64 uint64

// 浮点
var f32 float32  // 等同于Java的float
var f64 float64  // 等同于Java的double（推荐默认使用）

// 布尔
var b bool       // true/false

// 字符串（不可变的字节序列，UTF-8编码）
var s string

// 字节和字符
var by byte      // uint8的别名
var r rune       // int32的别名，表示一个Unicode码点（类似Java的char但是32位）
```

**重要区别**：Go的`string`底层是`[]byte`（字节切片），按UTF-8编码。Java的String底层是`char[]`（Java 9+为`byte[]`）按UTF-16编码。

```go
s := "你好Go"
fmt.Println(len(s))         // 8（字节数：中文3字节*2 + G + o）
fmt.Println(len([]rune(s))) // 4（字符数）

// 遍历字符串
for i, ch := range s {
    fmt.Printf("index=%d, char=%c, unicode=%U\n", i, ch, ch)
}
```

### 2.3 类型转换

Go不允许任何隐式类型转换，所有转换必须显式：

```go
var i int32 = 100
var j int64 = int64(i)   // 必须显式转换
var f float64 = float64(i)

// 字符串与数字的转换
import "strconv"

s := strconv.Itoa(42)           // int -> string: "42"
n, err := strconv.Atoi("42")   // string -> int: 42, nil
f, err := strconv.ParseFloat("3.14", 64) // string -> float64
```

**Java对比**：Java允许int自动提升为long、float自动提升为double。Go完全不允许，即使int32到int64也必须显式转换。

### 2.4 常量与iota

```go
// 常量声明
const Pi = 3.14159
const (
    StatusOK    = 200
    StatusError = 500
)

// iota：常量生成器，从0开始递增
type Weekday int

const (
    Sunday    Weekday = iota  // 0
    Monday                     // 1
    Tuesday                    // 2
    Wednesday                  // 3
    Thursday                   // 4
    Friday                     // 5
    Saturday                   // 6
)

// iota位运算用法（类似Java的枚举+位标志）
type Permission uint8

const (
    Read    Permission = 1 << iota  // 1  (001)
    Write                            // 2  (010)
    Execute                          // 4  (100)
)

func main() {
    perm := Read | Write  // 3 (011)
    fmt.Println(perm & Read != 0)  // true：有读权限
}
```

**Java对比**：Go没有`enum`关键字。iota + const组合是Go的枚举惯用法。Java的enum是完整的类，功能更丰富但也更重。

### 2.5 控制结构

#### if语句

```go
// 可以在条件前加初始化语句（变量作用域限定在if块内）
if err := doSomething(); err != nil {
    fmt.Println("error:", err)
} else {
    fmt.Println("success")
}
// err 在这里不可用
```

#### for循环（Go中唯一的循环语句）

```go
// 传统for循环（等同于Java的for）
for i := 0; i < 10; i++ {
    fmt.Println(i)
}

// while循环（Go用for代替while）
n := 1
for n < 100 {
    n *= 2
}

// 无限循环
for {
    // 等同于 for(;;) 或 while(true)
    break
}

// range遍历（等同于Java的for-each）
nums := []int{1, 2, 3, 4, 5}
for index, value := range nums {
    fmt.Printf("index=%d, value=%d\n", index, value)
}

// Go 1.22+: range over integers
for i := range 10 {
    fmt.Println(i)  // 0, 1, 2, ..., 9
}

// Go 1.23+: range over func（迭代器，详见第七章）
// 任何形如 func(yield func(V) bool) 或 func(yield func(K, V) bool) 的函数
// 都可以直接被 range 消费。
seq := func(yield func(int) bool) {
    for i := 0; i < 3; i++ {
        if !yield(i * i) {
            return
        }
    }
}
for v := range seq {
    fmt.Println(v) // 0, 1, 4
}
```

#### switch语句

```go
// Go的switch默认break，不需要写break（与Java相反）
// 想要fallthrough需要显式声明
day := "Monday"
switch day {
case "Monday":
    fmt.Println("周一")
case "Saturday", "Sunday":  // 多值匹配
    fmt.Println("周末")
default:
    fmt.Println("工作日")
}

// 无条件switch（替代if-else链）
score := 85
switch {
case score >= 90:
    fmt.Println("优秀")
case score >= 80:
    fmt.Println("良好")
case score >= 60:
    fmt.Println("及格")
default:
    fmt.Println("不及格")
}
```

### 2.6 函数

```go
// 多返回值（Go的标志性特征）
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// 命名返回值
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return  // 裸return，返回命名变量的当前值
}

// 可变参数
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}

// 函数作为一等公民
func apply(f func(int, int) int, a, b int) int {
    return f(a, b)
}

func main() {
    result := apply(func(x, y int) int {
        return x + y
    }, 3, 4)
    fmt.Println(result)  // 7
}

// 闭包
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}
```

**Java对比**：
- Java方法只能返回一个值（需要用对象或Pair包装多个值）
- Go的函数是一等公民，Java需要用函数式接口（Function, Consumer等）
- Go的闭包类似Java的Lambda，但Go的闭包可以修改捕获的变量

### 2.7 指针

```go
func main() {
    x := 42
    p := &x      // 取地址，p是*int类型
    fmt.Println(*p)  // 解引用，输出42
    *p = 100
    fmt.Println(x)   // 100，通过指针修改了x

    // 用指针实现函数内修改外部变量
    y := 10
    increment(&y)
    fmt.Println(y)  // 11
}

func increment(val *int) {
    *val++
}
```

**Java对比**：
- Java的对象引用本质上就是指针，但Java隐藏了这一概念
- Go的指针是显式的，但没有指针运算（不能`p++`移动指针），比C安全
- Go的基本类型是值传递（和Java一样），但Go可以通过指针传递来修改

### 2.8 包管理与可见性

```go
// 文件 mypackage/helper.go
package mypackage

// 首字母大写 = 导出（public）
func PublicFunc() string {
    return "I am public"
}

// 首字母小写 = 未导出（package-private）
func privateFunc() string {
    return "I am private"
}

// 结构体字段同理
type User struct {
    Name  string  // 导出字段（其他包可访问）
    email string  // 未导出字段（仅包内可访问）
}
```

**Java对比**：
- Java用`public/private/protected/默认`四级访问控制
- Go只有两级：导出（大写开头）和未导出（小写开头）
- Go没有Java的`protected`概念，没有继承所以不需要

---

## 第三章：复合数据类型

### 3.1 数组

```go
// 数组：固定长度，值类型（赋值会复制）
var arr [5]int                    // [0 0 0 0 0]
arr2 := [3]string{"a", "b", "c"}
arr3 := [...]int{1, 2, 3, 4, 5}  // 编译器推断长度

// 数组是值类型！（Java中数组是引用类型）
a := [3]int{1, 2, 3}
b := a        // 完整复制
b[0] = 100
fmt.Println(a[0])  // 仍然是1
```

**实际开发中数组很少直接使用，切片（slice）才是主角。**

### 3.2 切片（Slice）

切片是Go中最重要的数据结构之一，类似Java的ArrayList但更底层。

#### 底层结构

```go
// 切片的底层结构（runtime/slice.go）：
// type slice struct {
//     array unsafe.Pointer  // 指向底层数组的指针
//     len   int             // 当前长度
//     cap   int             // 容量
// }
```

#### 创建和使用

```go
// 方式1：从数组或切片创建
arr := [5]int{1, 2, 3, 4, 5}
s := arr[1:4]  // [2, 3, 4]，len=3, cap=4

// 方式2：make创建
s2 := make([]int, 5)      // len=5, cap=5, 全零
s3 := make([]int, 0, 10)  // len=0, cap=10

// 方式3：字面量
s4 := []int{1, 2, 3}

// 切片操作
fmt.Println(len(s4))  // 3
fmt.Println(cap(s4))  // 3
```

#### append与扩容机制

```go
s := make([]int, 0, 4)
s = append(s, 1, 2, 3)     // len=3, cap=4
s = append(s, 4)            // len=4, cap=4
s = append(s, 5)            // len=5, cap=8（触发扩容）

// 扩容规则（Go 1.18 起调整，1.21 微调，截至 1.25 仍以下述策略为准）：
// - 当请求容量 > 2*旧容量时，直接使用请求容量。
// - 旧容量 < 256 时：新容量 = 2*旧容量（指数增长）。
// - 旧容量 >= 256 时：每次按 newcap += (newcap + 3*256) / 4 平滑增长，
//   增长曲线从 2x 渐进逼近 1.25x，避免大切片浪费。
// - 最终容量再按 mallocgc 的 size class 向上对齐到合适的内存块。
// 说明：源码位于 runtime/slice.go 的 growslice，未来仍可能调整，
// 不要依赖具体数字，只能依赖 cap >= 请求容量这一保证。
```

#### 切片的陷阱

```go
// 陷阱1：切片共享底层数组
original := []int{1, 2, 3, 4, 5}
sub := original[1:3]  // [2, 3]
sub[0] = 200
fmt.Println(original)  // [1, 200, 3, 4, 5]  原始切片被修改！

// 安全复制
safeCopy := make([]int, len(sub))
copy(safeCopy, sub)

// 陷阱2：append可能创建新底层数组
s1 := []int{1, 2, 3}
s2 := s1[:]
s2 = append(s2, 4)  // 如果触发扩容，s2会指向新数组，与s1脱离关系

// 三索引切片表达式（Go 1.2 即引入，常用于库 API 防止下游修改原数组）
// 语法：a[low : high : max]，新切片 cap = max - low
s3 := original[1:3:3]  // len=2, cap=2，append 时必定触发扩容并复制
```

### 3.3 Map

```go
// 创建
m := make(map[string]int)
m["age"] = 25

// 字面量初始化
scores := map[string]int{
    "Alice": 95,
    "Bob":   87,
}

// 访问（key不存在返回零值）
val := scores["Charlie"]  // 0

// 判断key是否存在（comma ok模式）
val, ok := scores["Charlie"]
if !ok {
    fmt.Println("key not found")
}

// 删除
delete(scores, "Bob")

// 遍历（顺序随机！每次遍历顺序可能不同）
for key, value := range scores {
    fmt.Printf("%s: %d\n", key, value)
}
```

**Java对比**：
- Go的map类似Java的HashMap，但**不是线程安全的**
- 并发读写map会panic（Java的HashMap只是数据不一致，不会panic）
- 需要并发安全时使用`sync.Map`或加互斥锁
- Go的map遍历顺序是随机的（故意设计，避免依赖遍历顺序）

```go
// 并发访问map会panic
m := make(map[int]int)
go func() {
    for {
        m[1] = 1  // 写
    }
}()
go func() {
    for {
        _ = m[1]  // 读
    }
}()
// fatal error: concurrent map read and map write
```

### 3.4 结构体（Struct）

```go
// 定义（相当于Java的class，但没有构造方法）
type User struct {
    ID        int64
    Name      string
    Email     string
    CreatedAt time.Time
}

// 创建实例
u1 := User{ID: 1, Name: "Alice", Email: "alice@example.com"}
u2 := User{1, "Alice", "alice@example.com", time.Now()} // 按顺序（不推荐）
u3 := &User{Name: "Bob"}  // 返回指针，其他字段为零值

// Go没有构造方法，惯用工厂函数
func NewUser(name, email string) *User {
    return &User{
        ID:        generateID(),
        Name:      name,
        Email:     email,
        CreatedAt: time.Now(),
    }
}
```

### 3.5 结构体方法

```go
type Rectangle struct {
    Width, Height float64
}

// 值接收者：方法内操作的是副本
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// 指针接收者：方法内可以修改原始值
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

func main() {
    rect := Rectangle{Width: 10, Height: 5}
    fmt.Println(rect.Area())  // 50
    rect.Scale(2)
    fmt.Println(rect.Area())  // 200
}
```

**何时使用指针接收者？**
1. 需要修改接收者的值
2. 结构体较大，避免复制开销
3. 保持一致性：如果一个方法用了指针接收者，其他方法也应该用

**Java对比**：Java的方法默认就是通过引用调用（this就是引用），相当于Go永远使用指针接收者。

### 3.6 结构体嵌入（组合）

```go
// Go没有继承，使用组合（composition over inheritance）
type Animal struct {
    Name string
}

func (a Animal) Speak() string {
    return a.Name + " makes a sound"
}

type Dog struct {
    Animal       // 嵌入（匿名字段），不是继承！
    Breed string
}

func main() {
    d := Dog{
        Animal: Animal{Name: "Rex"},
        Breed:  "Labrador",
    }
    // 可以直接访问嵌入结构体的字段和方法（语法糖）
    fmt.Println(d.Name)    // Rex（等同于 d.Animal.Name）
    fmt.Println(d.Speak()) // Rex makes a sound
}

// 可以"覆盖"嵌入结构体的方法
func (d Dog) Speak() string {
    return d.Name + " barks"
}
```

**Java对比**：
- Java：`class Dog extends Animal`（is-a关系）
- Go：`type Dog struct { Animal }`（has-a关系，但语法上看起来像is-a）
- Go的方法"覆盖"不是多态——没有虚方法表，没有动态分派

### 3.7 自定义类型与类型别名

```go
// 自定义类型（创建全新类型，与底层类型不兼容）
type UserID int64
type Celsius float64
type Handler func(w http.ResponseWriter, r *http.Request)

var id UserID = 42
// var n int64 = id  // 编译错误！UserID和int64是不同类型

// 可以为自定义类型添加方法
func (c Celsius) ToFahrenheit() float64 {
    return float64(c)*9/5 + 32
}

// 类型别名（完全等同于原类型）
type byte = uint8   // Go内置定义
type rune = int32   // Go内置定义
type MyInt = int    // MyInt和int是同一类型

// Go 1.24+：泛型类型别名（Generic Type Aliases）
// 类型别名现在也可以带类型参数；对库重构（搬包/改名时保持向后兼容）非常有用。
type Set[T comparable] = map[T]struct{}

func main() {
    s := Set[string]{"a": {}, "b": {}}
    _ = s["a"]
}
```

---

## 第四章：接口与多态

### 4.1 Go接口的隐式实现

Go接口最大的特点：**隐式实现**。一个类型只要实现了接口定义的所有方法，就自动满足该接口，无需显式声明。

```go
// 定义接口
type Speaker interface {
    Speak() string
}

// Dog类型——没有任何"implements Speaker"声明
type Dog struct {
    Name string
}

func (d Dog) Speak() string {
    return d.Name + " says woof!"
}

// Cat类型
type Cat struct {
    Name string
}

func (c Cat) Speak() string {
    return c.Name + " says meow!"
}

// 多态使用
func MakeNoise(s Speaker) {
    fmt.Println(s.Speak())
}

func main() {
    MakeNoise(Dog{Name: "Rex"})   // Rex says woof!
    MakeNoise(Cat{Name: "Kitty"}) // Kitty says meow!
}
```

**Java对比**：
```java
// Java必须显式声明 implements
public class Dog implements Speaker {
    @Override
    public String speak() { return "woof"; }
}
```

Go的隐式接口优势：
- 无需修改第三方库的代码就能让其满足你的接口
- 接口可以在消费端定义，而非提供端（依赖倒置天然实现）
- 减少包之间的耦合

### 4.2 空接口与any

```go
// 空接口：没有任何方法要求，所有类型都满足
// Go 1.18之前
var anything interface{}
anything = 42
anything = "hello"
anything = []int{1, 2, 3}

// Go 1.18+ 引入 any 作为 interface{} 的类型别名
var anything2 any = "world"

// 用途：类似Java的Object，当不确定类型时使用
func PrintAnything(v any) {
    fmt.Println(v)
}
```

### 4.3 类型断言与类型Switch

```go
var i interface{} = "hello"

// 类型断言（可能panic）
s := i.(string)
fmt.Println(s)  // "hello"

// 安全的类型断言（comma ok模式）
s, ok := i.(string)
if ok {
    fmt.Println("string:", s)
}

n, ok := i.(int)
if !ok {
    fmt.Println("not an int")  // 走这里
}

// 类型switch
func describe(i interface{}) string {
    switch v := i.(type) {
    case string:
        return "string: " + v
    case int:
        return "int: " + strconv.Itoa(v)
    case bool:
        return "bool: " + strconv.FormatBool(v)
    default:
        return fmt.Sprintf("unknown: %T", v)
    }
}
```

### 4.4 常用标准库接口

```go
// io.Reader - 最重要的接口之一
type Reader interface {
    Read(p []byte) (n int, err error)
}

// io.Writer
type Writer interface {
    Write(p []byte) (n int, err error)
}

// fmt.Stringer - 相当于Java的toString()
type Stringer interface {
    String() string
}

// error接口
type error interface {
    Error() string
}

// sort.Interface
type Interface interface {
    Len() int
    Less(i, j int) bool
    Swap(i, j int)
}

// 实现Stringer
type User struct {
    Name string
    Age  int
}

func (u User) String() string {
    return fmt.Sprintf("%s (age %d)", u.Name, u.Age)
}

func main() {
    u := User{Name: "Alice", Age: 30}
    fmt.Println(u)  // Alice (age 30)  自动调用String()
}
```

### 4.5 接口组合

```go
// 小接口组合成大接口（Go推崇小而专的接口）
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

type Closer interface {
    Close() error
}

// 组合接口
type ReadWriter interface {
    Reader
    Writer
}

type ReadWriteCloser interface {
    Reader
    Writer
    Closer
}
```

### 4.6 接口最佳实践

1. **接口应该小**：Go标准库的接口大多只有1-3个方法
2. **在消费端定义接口**：谁用谁定义，而不是在实现端
3. **不要为了接口而接口**：如果只有一个实现，不需要接口
4. **返回具体类型，接受接口类型**

```go
// 推荐：在消费端定义所需的最小接口
// repository.go（消费端）
type UserStore interface {
    GetByID(id int64) (*User, error)
}

// service.go
type UserService struct {
    store UserStore  // 依赖接口，方便测试mock
}

func NewUserService(store UserStore) *UserService {
    return &UserService{store: store}
}
```

---

## 第五章：错误处理

### 5.1 Go的错误处理哲学

Go的核心理念：**错误是值（errors are values）**，不是异常。

```go
// Go的错误处理模式
result, err := doSomething()
if err != nil {
    // 处理错误
    return err
}
// 使用result
```

**Java对比**：
```java
// Java的异常处理
try {
    Result result = doSomething();
} catch (SomeException e) {
    // 处理异常
}
```

为什么Go选择这种方式：
- 错误路径和正常路径同样重要，不应被隐藏
- 强制开发者立即处理错误，避免异常被忽略
- 没有异常展开（stack unwinding）的性能开销
- 代码流程清晰，没有隐藏的控制流

### 5.2 error接口

```go
// error是一个内置接口
type error interface {
    Error() string
}

// 最简单的错误创建
err1 := errors.New("something went wrong")
err2 := fmt.Errorf("user %d not found", userID)
```

### 5.3 自定义错误类型

```go
// 自定义错误类型（携带更多上下文信息）
type NotFoundError struct {
    Resource string
    ID       int64
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with ID %d not found", e.Resource, e.ID)
}

// 使用
func GetUser(id int64) (*User, error) {
    user := db.Find(id)
    if user == nil {
        return nil, &NotFoundError{Resource: "user", ID: id}
    }
    return user, nil
}

// 业务错误常量（哨兵错误）
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInternal     = errors.New("internal error")
)
```

### 5.4 错误包装（Go 1.13+）

```go
// 使用 %w 包装错误（保留错误链）
func GetUserProfile(id int64) (*Profile, error) {
    user, err := GetUser(id)
    if err != nil {
        return nil, fmt.Errorf("GetUserProfile: %w", err)
    }
    // ...
    return profile, nil
}

// errors.Is：判断错误链中是否包含特定错误（类似Java的instanceof判断cause链）
if errors.Is(err, ErrNotFound) {
    // 处理未找到
}

// errors.As：从错误链中提取特定类型的错误
var notFoundErr *NotFoundError
if errors.As(err, &notFoundErr) {
    fmt.Printf("Resource: %s, ID: %d\n", notFoundErr.Resource, notFoundErr.ID)
}

// 多错误合并（Go 1.20+）
err := errors.Join(err1, err2, err3)
```

### 5.5 panic/recover

```go
// panic：程序不可恢复时使用（不要用来做常规错误处理！）
func MustParseURL(rawURL string) *url.URL {
    u, err := url.Parse(rawURL)
    if err != nil {
        panic(fmt.Sprintf("invalid URL: %s", rawURL))
    }
    return u
}

// recover：捕获panic（只能在defer中使用）
func SafeExecute(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic recovered: %v", r)
        }
    }()
    fn()
    return nil
}
```

**使用原则**：
- `panic`仅用于真正不可恢复的错误（程序员错误，如数组越界、nil指针）
- 库代码不应该panic（应返回error）
- Web框架通常在最外层有recover中间件，防止单个请求crash整个进程

### 5.6 defer关键字

```go
// defer：函数返回前执行（LIFO顺序）
func ReadFile(path string) ([]byte, error) {
    f, err := os.Open(path)
    if err != nil {
        return nil, err
    }
    defer f.Close()  // 确保文件关闭，相当于Java的try-with-resources
    
    return io.ReadAll(f)
}

// 多个defer按LIFO（后进先出）顺序执行
func main() {
    defer fmt.Println("1")
    defer fmt.Println("2")
    defer fmt.Println("3")
    // 输出：3, 2, 1
}

// defer与闭包
func count() {
    for i := 0; i < 3; i++ {
        defer func() {
            fmt.Println(i)  // 注意：i是引用，defer执行时i已经是3
        }()
    }
    // 输出：3, 3, 3

    // 正确做法：传参
    for i := 0; i < 3; i++ {
        defer func(n int) {
            fmt.Println(n)
        }(i)
    }
    // 输出：2, 1, 0（LIFO）
}

// defer与命名返回值
func doublePlus(x int) (result int) {
    defer func() {
        result++  // defer可以修改命名返回值
    }()
    return x * 2  // 实际返回 x*2 + 1
}
```

**Java对比**：`defer`相当于Java的`try-finally`或`try-with-resources`，但更灵活——可以在任何地方声明，不限于资源管理。

---

## 第六章：并发编程（核心重点）

### 6.1 Goroutine

Goroutine是Go并发的核心，是一种由Go运行时管理的轻量级线程。

```go
func sayHello(name string) {
    fmt.Printf("Hello, %s!\n", name)
}

func main() {
    // 启动goroutine，只需加 go 关键字
    go sayHello("Alice")
    go sayHello("Bob")
    
    // 匿名函数goroutine
    go func() {
        fmt.Println("Anonymous goroutine")
    }()
    
    time.Sleep(time.Second)  // 等待goroutine完成（生产中不这样用）
}
```

**Goroutine vs Java线程**：

| 特性 | Goroutine | Java线程 | Java虚拟线程(21+) |
|------|-----------|----------|-------------------|
| 初始栈大小 | 2-8KB（动态增长） | 1MB（固定） | ~几KB |
| 创建成本 | 极低（纳秒级） | 高（微秒级） | 低 |
| 切换成本 | ~几十ns（用户态） | ~几μs（内核态） | 低 |
| 数量级 | 轻松百万级 | 通常数千 | 可百万级 |
| 调度 | Go运行时（协作+抢占） | OS内核 | JVM |

### 6.2 GMP调度模型

Go的并发调度基于GMP模型：

```
G (Goroutine) - 待执行的goroutine
M (Machine)   - 操作系统线程
P (Processor) - 逻辑处理器（默认等于CPU核心数）

          ┌─────────┐
          │   G G G │  Global Queue
          └────┬────┘
               │
     ┌─────────┼─────────┐
     │         │         │
  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐
  │  P  │  │  P  │  │  P  │   Processors (GOMAXPROCS)
  │     │  │     │  │     │
  │G G G│  │G G G│  │G G  │   Local Run Queue
  └──┬──┘  └──┬──┘  └──┬──┘
     │         │         │
  ┌──▼──┐  ┌──▼──┐  ┌──▼──┐
  │  M  │  │  M  │  │  M  │   OS Threads
  └─────┘  └─────┘  └─────┘
```

核心机制：
- **Work Stealing**：P的本地队列为空时，从其他P或全局队列偷取G
- **Hand Off**：M阻塞（如系统调用）时，P会转移到空闲M上
- **抢占式调度**（Go 1.14+）：基于信号的异步抢占，解决了长时间运算不让出的问题

```go
import "runtime"

func main() {
    // 查看/设置使用的CPU核心数
    fmt.Println(runtime.GOMAXPROCS(0))  // 获取当前值
    runtime.GOMAXPROCS(4)                // 设置为4
    
    fmt.Println(runtime.NumGoroutine()) // 当前goroutine数量
}
```

### 6.3 Channel

Channel是goroutine之间通信的管道，是Go并发的核心机制。

> "Don't communicate by sharing memory; share memory by communicating." — Go谚语

```go
// 创建channel
ch := make(chan int)      // 无缓冲channel
bch := make(chan int, 10) // 有缓冲channel，容量10

// 发送和接收
ch <- 42     // 发送
val := <-ch  // 接收

// 关闭channel
close(ch)
```

#### 无缓冲 vs 有缓冲

```go
// 无缓冲channel：发送和接收必须同时就绪（同步）
func main() {
    ch := make(chan string)
    
    go func() {
        ch <- "hello"  // 阻塞直到有人接收
    }()
    
    msg := <-ch  // 阻塞直到有人发送
    fmt.Println(msg)
}

// 有缓冲channel：缓冲区满时发送阻塞，空时接收阻塞
func main() {
    ch := make(chan int, 3)
    ch <- 1  // 不阻塞
    ch <- 2  // 不阻塞
    ch <- 3  // 不阻塞
    // ch <- 4  // 阻塞！缓冲区满
    
    fmt.Println(<-ch)  // 1
}
```

#### Channel方向性

```go
// 只发送channel
func producer(ch chan<- int) {
    for i := 0; i < 10; i++ {
        ch <- i
    }
    close(ch)
}

// 只接收channel
func consumer(ch <-chan int) {
    for val := range ch {  // range会在channel关闭时自动退出
        fmt.Println(val)
    }
}

func main() {
    ch := make(chan int, 5)
    go producer(ch)
    consumer(ch)
}
```

#### Channel底层结构

```go
// runtime/chan.go 中的hchan结构（简化）
// type hchan struct {
//     qcount   uint           // 当前元素数量
//     dataqsiz uint           // 缓冲区大小
//     buf      unsafe.Pointer // 环形缓冲区
//     sendx    uint           // 发送索引
//     recvx    uint           // 接收索引
//     recvq    waitq          // 等待接收的goroutine队列
//     sendq    waitq          // 等待发送的goroutine队列
//     lock     mutex          // 互斥锁
// }
```

### 6.4 select语句

select用于同时等待多个channel操作，类似switch但用于channel。

```go
func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)
    
    go func() {
        time.Sleep(100 * time.Millisecond)
        ch1 <- "one"
    }()
    
    go func() {
        time.Sleep(200 * time.Millisecond)
        ch2 <- "two"
    }()
    
    // 等待第一个就绪的channel
    select {
    case msg := <-ch1:
        fmt.Println("Received from ch1:", msg)
    case msg := <-ch2:
        fmt.Println("Received from ch2:", msg)
    }
}

// 超时控制
select {
case result := <-ch:
    fmt.Println(result)
case <-time.After(3 * time.Second):
    fmt.Println("timeout")
}

// 非阻塞操作（default分支）
select {
case msg := <-ch:
    fmt.Println(msg)
default:
    fmt.Println("no message available")
}
```

### 6.5 sync包

```go
import "sync"

// Mutex：互斥锁
type SafeCounter struct {
    mu    sync.Mutex
    count map[string]int
}

func (c *SafeCounter) Inc(key string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count[key]++
}

func (c *SafeCounter) Get(key string) int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count[key]
}

// RWMutex：读写锁（多读单写）
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()         // 读锁，多个goroutine可同时持有
    defer c.mu.RUnlock()
    val, ok := c.data[key]
    return val, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()          // 写锁，独占
    defer c.mu.Unlock()
    c.data[key] = value
}

// WaitGroup：等待一组goroutine完成
func main() {
    var wg sync.WaitGroup
    
    urls := []string{"url1", "url2", "url3"}
    
    for _, url := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()
            // fetch(u)
            fmt.Println("Fetched:", u)
        }(url)
    }
    
    wg.Wait()  // 阻塞直到所有goroutine完成
    fmt.Println("All done")
}

// Once：确保某操作只执行一次（单例模式）
var (
    instance *Database
    once     sync.Once
)

func GetDB() *Database {
    once.Do(func() {
        instance = &Database{}
        instance.Connect()
    })
    return instance
}

// sync.Map：并发安全的map（特定场景下使用）
var cache sync.Map

cache.Store("key", "value")
val, ok := cache.Load("key")
cache.Delete("key")
cache.Range(func(key, value any) bool {
    fmt.Println(key, value)
    return true  // 返回false停止遍历
})

// sync.Pool：对象池（减少GC压力）
var bufPool = sync.Pool{
    New: func() any {
        return new(bytes.Buffer)
    },
}

func process() {
    buf := bufPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufPool.Put(buf)
    }()
    // 使用buf...
}

// sync.OnceFunc / OnceValue / OnceValues（Go 1.21+）：
// 比 sync.Once.Do 更直观——返回一个"首次调用执行、后续调用复用结果"的闭包。
var loadConfig = sync.OnceValue(func() *Config {
    return readConfigFromDisk()
})
cfg := loadConfig()  // 第一次：真正读盘
cfg2 := loadConfig() // 之后：直接返回缓存值（==cfg）

// sync.WaitGroup.Go（Go 1.25+）：
// 把 Add(1) + go + defer Done() 三步合成一步，是新代码推荐写法。
var wg sync.WaitGroup
for _, url := range urls {
    wg.Go(func() {
        fetch(url)
    })
}
wg.Wait()
```

### 6.6 context包

context用于控制goroutine的生命周期，传递超时、取消信号和请求范围的值。

```go
import "context"

// 超时控制
func fetchWithTimeout(url string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()  // 必须调用cancel释放资源
    
    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err  // 超时时err会包含context.DeadlineExceeded
    }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}

// 取消传播
func longRunningTask(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()  // context.Canceled 或 context.DeadlineExceeded
        default:
            // 继续工作...
            doWork()
        }
    }
}

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    
    go longRunningTask(ctx)
    
    time.Sleep(3 * time.Second)
    cancel()  // 通知所有使用此ctx的goroutine停止
}

// 传递请求范围的值（谨慎使用，仅用于跨API边界的请求数据）
type contextKey string

const userIDKey contextKey = "userID"

func WithUserID(ctx context.Context, userID int64) context.Context {
    return context.WithValue(ctx, userIDKey, userID)
}

func GetUserID(ctx context.Context) (int64, bool) {
    id, ok := ctx.Value(userIDKey).(int64)
    return id, ok
}
```

**Java对比**：context类似Java的`CompletableFuture`的取消机制 + `ThreadLocal`的请求传值功能的结合体。

### 6.7 并发模式

```go
// Pipeline模式
func generator(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

func square(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}

func main() {
    nums := generator(2, 3, 4, 5)
    squares := square(nums)
    for v := range squares {
        fmt.Println(v)  // 4, 9, 16, 25
    }
}

// Worker Pool模式
func workerPool(jobs <-chan int, results chan<- int, numWorkers int) {
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }(i)
    }
    wg.Wait()
    close(results)
}

// Fan-out, Fan-in
func fanOut(input <-chan int, workers int) []<-chan int {
    channels := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        channels[i] = worker(input)
    }
    return channels
}

func fanIn(channels ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    merged := make(chan int)
    
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for val := range c {
                merged <- val
            }
        }(ch)
    }
    
    go func() {
        wg.Wait()
        close(merged)
    }()
    
    return merged
}
```

### 6.8 数据竞争检测

```go
// 使用 -race 标志检测数据竞争
// go run -race main.go
// go test -race ./...

// 示例：有数据竞争的代码
func main() {
    counter := 0
    var wg sync.WaitGroup
    
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            counter++  // DATA RACE!
        }()
    }
    wg.Wait()
}

// 修复方案1：使用Mutex
// 修复方案2：使用atomic
import "sync/atomic"

var counter int64

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 1000; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            atomic.AddInt64(&counter, 1)
        }()
    }
    wg.Wait()
    fmt.Println(atomic.LoadInt64(&counter))  // 1000
}
```

---

## 第七章：泛型（Go 1.18+）

### 7.1 类型参数

Go 1.18引入泛型，使用方括号`[]`定义类型参数（Java用尖括号`<>`）。

```go
// 泛型函数
func Min[T int | float64 | string](a, b T) T {
    if a < b {
        return a
    }
    return b
}

func main() {
    fmt.Println(Min[int](3, 5))       // 3（显式指定类型）
    fmt.Println(Min(3.14, 2.71))      // 2.71（类型推断）
    fmt.Println(Min("apple", "banana")) // apple
}
```

### 7.2 类型约束（Constraints）

```go
// 约束是接口，定义了类型参数必须满足的条件
type Number interface {
    int | int8 | int16 | int32 | int64 |
    float32 | float64
}

func Sum[T Number](numbers []T) T {
    var total T
    for _, n := range numbers {
        total += n
    }
    return total
}

// 使用 ~ 表示底层类型（包含自定义类型）
type MyInt int

type Integer interface {
    ~int | ~int8 | ~int16 | ~int32 | ~int64
}

// MyInt 满足 Integer 约束，因为其底层类型是 int
func Double[T Integer](v T) T {
    return v * 2
}

var x MyInt = 5
fmt.Println(Double(x))  // 10
```

### 7.3 内置约束

```go
// comparable：支持 == 和 != 操作
func Contains[T comparable](slice []T, target T) bool {
    for _, v := range slice {
        if v == target {
            return true
        }
    }
    return false
}

// any：等同于 interface{}，无任何约束
func PrintAll[T any](items []T) {
    for _, item := range items {
        fmt.Println(item)
    }
}

// cmp.Ordered（Go 1.21+）：支持 < > <= >= 的类型
import "cmp"

func MaxSlice[T cmp.Ordered](s []T) T {
    m := s[0]
    for _, v := range s[1:] {
        if v > m {
            m = v
        }
    }
    return m
}
```

### 7.4 自定义约束接口

```go
// 约束可以同时要求类型集合和方法
type Stringer interface {
    comparable
    String() string
}

// 约束中的方法
type Addable interface {
    ~int | ~float64
    IsPositive() bool
}

// 实际应用：可排序切片
type Sortable[T cmp.Ordered] struct {
    data []T
}

func (s *Sortable[T]) Add(item T) {
    s.data = append(s.data, item)
}

func (s *Sortable[T]) Sort() {
    slices.Sort(s.data)
}
```

### 7.5 泛型类型

```go
// 泛型结构体
type Pair[T, U any] struct {
    First  T
    Second U
}

// 泛型方法
func (p Pair[T, U]) String() string {
    return fmt.Sprintf("(%v, %v)", p.First, p.Second)
}

// 泛型Stack
type Stack[T any] struct {
    items []T
}

func (s *Stack[T]) Push(item T) {
    s.items = append(s.items, item)
}

func (s *Stack[T]) Pop() (T, bool) {
    var zero T
    if len(s.items) == 0 {
        return zero, false
    }
    item := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return item, true
}

// 泛型Map/Filter/Reduce
func Map[T, U any](slice []T, fn func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = fn(v)
    }
    return result
}

func Filter[T any](slice []T, fn func(T) bool) []T {
    var result []T
    for _, v := range slice {
        if fn(v) {
            result = append(result, v)
        }
    }
    return result
}

func Reduce[T, U any](slice []T, initial U, fn func(U, T) U) U {
    result := initial
    for _, v := range slice {
        result = fn(result, v)
    }
    return result
}
```

### 7.6 Go泛型 vs Java泛型

| 特性 | Go泛型 | Java泛型 |
|------|--------|----------|
| 实现方式 | GCShape stenciling（部分单态化） | 类型擦除 |
| 运行时类型信息 | 保留 | 擦除（运行时不知道T是什么） |
| 原始类型 | 支持（int, float64等） | 不支持（必须用Integer, Double包装） |
| 约束表达 | 接口（类型集合+方法） | extends/super通配符 |
| 协变/逆变 | 无 | 有（? extends T, ? super T） |
| 类型参数语法 | `[T constraint]` | `<T extends Bound>` |
| 引入时间 | 2022 (Go 1.18) | 2004 (Java 5) |

```go
// Go：编译器为不同shape生成代码
func Print[T any](v T) { fmt.Println(v) }
// Print[int](42) 和 Print[string]("hi") 可能共享或独立代码

// Java：类型擦除，编译后T变成Object
// public <T> void print(T v) { System.out.println(v); }
// 编译后等同于 public void print(Object v)
```

### 7.7 泛型使用建议

1. **不要滥用**：如果`interface{}`/`any`就够用，不必用泛型
2. **适合场景**：容器类型、通用算法（排序、查找）、减少类型断言
3. **不适合场景**：仅为了少写几行代码、业务逻辑差异大时
4. **方法不能有类型参数**：只有函数和类型可以有

```go
// 错误：方法不能有自己的类型参数
// func (s *Stack[T]) Transform[U any](fn func(T) U) *Stack[U] {}  // 编译错误

// 正确：用顶层函数代替
func Transform[T, U any](s *Stack[T], fn func(T) U) *Stack[U] {
    result := &Stack[U]{}
    for _, item := range s.items {
        result.Push(fn(item))
    }
    return result
}
```

### 7.8 迭代器与 `iter` 包（Go 1.23+）

Go 1.23 把"自定义迭代器"作为一等概念加入语言，对应的标准库是 [`iter`](https://pkg.go.dev/iter)。其核心是「**push-style 迭代器**」：迭代器不是返回一个一个元素，而是接受一个 `yield` 回调，由迭代器主动把元素推给消费方；`yield` 返回 `false` 表示消费方不再需要更多元素，应当立即停止。

```go
import "iter"

// iter.Seq[V]    = func(yield func(V) bool)
// iter.Seq2[K,V] = func(yield func(K, V) bool)

// 从 0 计到 n-1 的迭代器
func CountTo(n int) iter.Seq[int] {
    return func(yield func(int) bool) {
        for i := 0; i < n; i++ {
            if !yield(i) {
                return // 消费方提前退出（如 break）
            }
        }
    }
}

func main() {
    for v := range CountTo(5) { // for-range 直接消费迭代器
        fmt.Println(v)
        if v == 3 {
            break // 会让 yield 返回 false，迭代器函数立刻 return
        }
    }
}
```

**配套的标准库扩展**（截至 Go 1.25）：

| 包 | 关键 API | 用途 |
|----|----------|------|
| `slices` | `All`, `Values`, `Backward`, `Sorted`, `Collect`, `AppendSeq`, `Chunk` | 切片 ↔ 迭代器互转 |
| `maps` | `All`, `Keys`, `Values`, `Collect`, `Insert` | map ↔ 迭代器互转 |
| `iter` | `Pull`, `Pull2` | 把 push 迭代器转换成手动调用的 next/stop 形式 |
| `strings` / `bytes` | `SplitSeq`, `FieldsSeq`, `Lines` | 流式拆分，避免一次性分配整个 `[]string` |

```go
// 例：把 map 排序后遍历
m := map[string]int{"b": 2, "a": 1, "c": 3}
for _, k := range slices.Sorted(maps.Keys(m)) {
    fmt.Println(k, m[k])
}

// 例：把"无限"迭代器转成 pull 形式
next, stop := iter.Pull(CountTo(1_000_000))
defer stop() // 必须调用以释放迭代器内部 goroutine
v, ok := next()
fmt.Println(v, ok) // 0, true
```

**最佳实践**：
- 库 API 优先返回 `iter.Seq`/`iter.Seq2`，调用方可以 `range`，也可以用 `slices.Collect` 收成切片。
- 写迭代器时一定要检查 `yield` 的返回值，否则消费方 `break` 后还会继续运算，造成"看起来正常但实际跑过头"的 bug。
- `iter.Pull` 内部会启动一个 goroutine 来翻转控制流，开销不小，**只在确实需要 next/stop 风格时使用**。

**Java 对比**：Go 的 push 迭代器 + `yield` 类似 Python 的生成器，但在 Go 里不是协程级机制，而是普通函数 + 编译器对 `for ... range f` 的特殊重写。Java 的 `Iterator`/`Stream` 是 pull 风格，Go 选 push 是为了让"提前 break"和"defer 资源释放"自然工作。

---

## 第八章：标准库精讲

### 8.1 fmt包

```go
import "fmt"

type User struct {
    Name string
    Age  int
}

u := User{"Alice", 30}

fmt.Printf("%v\n", u)   // {Alice 30}       默认格式
fmt.Printf("%+v\n", u)  // {Name:Alice Age:30}  带字段名
fmt.Printf("%#v\n", u)  // main.User{Name:"Alice", Age:30}  Go语法表示
fmt.Printf("%T\n", u)   // main.User        类型

// 常用动词
fmt.Printf("%d\n", 42)       // 十进制整数
fmt.Printf("%x\n", 255)      // ff 十六进制
fmt.Printf("%b\n", 10)       // 1010 二进制
fmt.Printf("%f\n", 3.14)     // 3.140000
fmt.Printf("%.2f\n", 3.14)   // 3.14 精度控制
fmt.Printf("%s\n", "hello")  // 字符串
fmt.Printf("%q\n", "hello")  // "hello" 带引号
fmt.Printf("%p\n", &u)       // 指针地址
fmt.Printf("%c\n", 65)       // A 字符

// Sprintf返回字符串（不输出）
s := fmt.Sprintf("Name: %s, Age: %d", u.Name, u.Age)

// Fprintf写入io.Writer
fmt.Fprintf(os.Stderr, "error: %v\n", err)
```

### 8.2 strings/strconv

```go
import (
    "strings"
    "strconv"
)

// strings包
strings.Contains("hello world", "world")  // true
strings.HasPrefix("hello", "he")           // true
strings.HasSuffix("hello", "lo")           // true
strings.Split("a,b,c", ",")               // ["a", "b", "c"]
strings.Join([]string{"a", "b"}, "-")     // "a-b"
strings.Replace("hello", "l", "L", -1)    // "heLLo"
strings.ToUpper("hello")                   // "HELLO"
strings.TrimSpace("  hello  ")            // "hello"
strings.Repeat("ha", 3)                    // "hahaha"
strings.Index("hello", "ll")              // 2
strings.Count("hello", "l")               // 2

// strings.Builder（高效字符串拼接，类似Java的StringBuilder）
var sb strings.Builder
for i := 0; i < 1000; i++ {
    sb.WriteString("hello")
}
result := sb.String()

// strconv包：字符串与基本类型转换
strconv.Itoa(42)                    // "42"
strconv.Atoi("42")                  // 42, nil
strconv.FormatFloat(3.14, 'f', 2, 64)  // "3.14"
strconv.ParseFloat("3.14", 64)     // 3.14, nil
strconv.FormatBool(true)            // "true"
strconv.ParseBool("true")           // true, nil
```

### 8.3 io/bufio

```go
import (
    "io"
    "bufio"
    "os"
)

// io.Reader和io.Writer是Go I/O的基石
// 一切皆Reader/Writer：文件、网络连接、压缩流、加密流...

// 读取全部内容
data, err := io.ReadAll(reader)

// 复制流
written, err := io.Copy(dst, src)  // dst实现Writer，src实现Reader

// bufio：带缓冲的I/O
// 按行读取文件
file, _ := os.Open("data.txt")
defer file.Close()

scanner := bufio.NewScanner(file)
for scanner.Scan() {
    line := scanner.Text()
    fmt.Println(line)
}
if err := scanner.Err(); err != nil {
    log.Fatal(err)
}

// 带缓冲的写入
writer := bufio.NewWriter(file)
writer.WriteString("hello\n")
writer.Flush()  // 别忘了刷新缓冲区
```

### 8.4 os/filepath

```go
import (
    "os"
    "path/filepath"
)

// 文件操作
// 读取整个文件
data, err := os.ReadFile("config.json")

// 写入文件
err := os.WriteFile("output.txt", []byte("content"), 0644)

// 创建/打开文件
f, err := os.Create("new.txt")     // 创建（截断已有）
f, err := os.Open("exist.txt")     // 只读打开
f, err := os.OpenFile("log.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

// 目录操作
os.Mkdir("dir", 0755)
os.MkdirAll("a/b/c", 0755)  // 递归创建
entries, _ := os.ReadDir(".")

// filepath包
filepath.Join("path", "to", "file.txt")  // "path/to/file.txt"
filepath.Ext("main.go")                   // ".go"
filepath.Base("/path/to/file.txt")        // "file.txt"
filepath.Dir("/path/to/file.txt")         // "/path/to"
filepath.Abs("relative/path")             // 绝对路径

// 遍历目录树
filepath.WalkDir(".", func(path string, d fs.DirEntry, err error) error {
    if err != nil {
        return err
    }
    fmt.Println(path)
    return nil
})
```

### 8.5 encoding/json

```go
import "encoding/json"

// struct tag控制JSON序列化
type User struct {
    ID        int64     `json:"id"`
    Name      string    `json:"name"`
    Email     string    `json:"email,omitempty"`  // 空值时省略
    Password  string    `json:"-"`                // 永不序列化
    CreatedAt time.Time `json:"created_at"`
}

// 序列化（Marshal）
user := User{ID: 1, Name: "Alice"}
data, err := json.Marshal(user)
// {"id":1,"name":"Alice","created_at":"0001-01-01T00:00:00Z"}

// 格式化输出
data, err := json.MarshalIndent(user, "", "  ")

// 反序列化（Unmarshal）
var u User
err := json.Unmarshal([]byte(`{"id":1,"name":"Bob"}`), &u)

// 流式处理（大文件）
decoder := json.NewDecoder(reader)
var result MyStruct
err := decoder.Decode(&result)

encoder := json.NewEncoder(writer)
err := encoder.Encode(result)

// 处理动态JSON
var raw map[string]interface{}
json.Unmarshal(data, &raw)

// json.RawMessage延迟解析
type Event struct {
    Type string          `json:"type"`
    Data json.RawMessage `json:"data"`
}
```

**Java对比**：Go的struct tag类似Java的Jackson注解（@JsonProperty, @JsonIgnore），但更轻量。

### 8.6 net/http

```go
import "net/http"

// HTTP 服务端（Go 1.22+ 增强路由，至 1.25 仍是标准库主力）
func main() {
    mux := http.NewServeMux()

    // Go 1.22+ 支持「方法 + 路径参数 + 通配段」
    mux.HandleFunc("GET /users/{id}", getUser)
    mux.HandleFunc("POST /users", createUser)
    mux.HandleFunc("GET /files/{path...}", serveFile) // {x...} 匹配剩余路径
    mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("ok"))
    })
    
    server := &http.Server{
        Addr:         ":8080",
        Handler:      mux,
        ReadTimeout:  10 * time.Second,
        WriteTimeout: 10 * time.Second,
    }
    
    log.Fatal(server.ListenAndServe())
}

func getUser(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")  // Go 1.22+ 获取路径参数
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]string{"id": id})
}

// HTTP客户端
func fetchData(url string) ([]byte, error) {
    client := &http.Client{Timeout: 10 * time.Second}
    
    resp, err := client.Get(url)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("status: %d", resp.StatusCode)
    }
    
    return io.ReadAll(resp.Body)
}
```

### 8.7 time包

```go
import "time"

// Go的时间格式化使用参考时间：2006-01-02 15:04:05（Mon Jan 2 15:04:05 MST 2006）
// 记忆技巧：1月2日下午3点4分5秒2006年（1-2-3-4-5-6）
now := time.Now()
fmt.Println(now.Format("2006-01-02 15:04:05"))  // 2024-03-15 14:30:00
fmt.Println(now.Format("2006/01/02"))            // 2024/03/15
fmt.Println(now.Format(time.RFC3339))            // 2024-03-15T14:30:00+08:00

// 解析时间
t, err := time.Parse("2006-01-02", "2024-03-15")
t, err := time.ParseInLocation("2006-01-02 15:04:05", "2024-03-15 14:30:00", time.Local)

// 时间运算
future := now.Add(24 * time.Hour)
duration := future.Sub(now)
fmt.Println(duration)  // 24h0m0s

// 定时器
ticker := time.NewTicker(time.Second)
defer ticker.Stop()

for i := 0; i < 5; i++ {
    <-ticker.C
    fmt.Println("tick")
}

// 超时
timer := time.NewTimer(3 * time.Second)
<-timer.C
fmt.Println("timeout")

// Go 1.23+ 重要变更：未引用的 Timer/Ticker 现在可以被 GC 回收。
// 旧版本中即使没有任何变量引用 timer，runtime 仍会持有它直到触发，
// 导致"忘记 Stop 就泄漏"。新版本下忘记 Stop 不再泄漏，
// 但显式 Stop() 仍然是良好实践（更早释放、避免还要触发一次）。
//
// 同时 timer.Reset 行为更稳健：不再要求先 Stop+drain channel。
```

### 8.8 log/slog（Go 1.21+）

```go
import "log/slog"

// 结构化日志（替代传统log包）
slog.Info("user logged in",
    "user_id", 42,
    "ip", "192.168.1.1",
)
// 输出: 2024/03/15 14:30:00 INFO user logged in user_id=42 ip=192.168.1.1

// JSON格式
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelDebug,
}))
slog.SetDefault(logger)

slog.Debug("debug message", "key", "value")
// {"time":"2024-03-15T14:30:00Z","level":"DEBUG","msg":"debug message","key":"value"}

// 带上下文的logger
logger = logger.With("service", "user-api", "version", "1.0")
logger.Info("server started", "port", 8080)

// 分组
slog.Info("request",
    slog.Group("request",
        slog.String("method", "GET"),
        slog.String("path", "/users"),
    ),
    slog.Int("status", 200),
)
```

### 8.9 testing包

```go
// math_test.go（文件名必须以_test.go结尾）
package math

import "testing"

// 单元测试（函数名必须以Test开头）
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d, want 5", result)
    }
}

// 表驱动测试（Go的最佳实践）
func TestAdd_TableDriven(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
        {"mixed", -1, 5, 4},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

// 基准测试（函数名以 Benchmark 开头）
// Go 1.24+ 推荐写法：testing.B.Loop()，自动处理迭代次数 + 内置防优化保护。
func BenchmarkAdd(b *testing.B) {
    for b.Loop() {
        _ = Add(2, 3)
    }
}

// 旧写法仍可用，但 b.N 在每次迭代中可能被重新评估，
// 容易出现"循环外的初始化被算进基准时间"的坑。
func BenchmarkAddLegacy(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
// 运行: go test -bench=. -benchmem

// 模糊测试（Go 1.18+，函数名以 Fuzz 开头）
func FuzzAdd(f *testing.F) {
    f.Add(1, 2)  // 种子语料
    f.Fuzz(func(t *testing.T, a, b int) {
        result := Add(a, b)
        if result != a+b {
            t.Errorf("Add(%d, %d) = %d", a, b, result)
        }
    })
}
// 运行: go test -fuzz=FuzzAdd
```

#### `testing/synctest`：并发代码确定性测试（Go 1.25+）

测试涉及 `time.Sleep`、`time.Ticker`、超时的并发代码一直是 Go 的痛点：要么实际等待（慢），要么手写假时钟（侵入业务）。Go 1.25 标准库的 `testing/synctest` 提供「**虚拟时间气泡（bubble）**」：

- `synctest.Test` 内启动的 goroutine 共享一个**假时钟**，`time.Sleep` 立即返回但相对顺序保持正确；
- `synctest.Wait` 阻塞直到气泡内所有 goroutine 全部"durably blocked"，可断言并发完成状态；
- 不需要改业务代码，原生 `time` 包 API 在气泡内自动被替换。

```go
import "testing/synctest"

func TestRetryWithBackoff(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        var attempts atomic.Int32
        go func() {
            // 业务代码使用真实的 time.Sleep；
            // 在气泡里这些 Sleep 不会真的等，但顺序 / 超时关系仍然正确。
            for i := 0; i < 3; i++ {
                attempts.Add(1)
                time.Sleep(time.Second << i)
            }
        }()
        synctest.Wait() // 等所有 goroutine 静止
        if got := attempts.Load(); got != 3 {
            t.Fatalf("got %d retries, want 3", got)
        }
    })
}
```

替代第三方库（如 `github.com/benbjohnson/clock`）的"假时钟注入"模式，是测试超时/重试/限流逻辑的官方推荐方式。

### 8.10 `unique` 包（Go 1.23+）

`unique` 提供「**值规范化（interning）**」：相同的值只保留一份，得到一个轻量的 `Handle[T]`，比较只需比较 handle，省内存且 O(1) 比较。

```go
import "unique"

type Tag struct{ K, V string }

a := unique.Make(Tag{"env", "prod"})
b := unique.Make(Tag{"env", "prod"})
fmt.Println(a == b)          // true，handle 直接相等
fmt.Println(a.Value().K)     // "env"
```

适用场景：标签/标签集（label set）、配置键、被大量结构体反复持有的字符串/小结构体。底层用 `weak` 引用，长期不再使用的 handle 可被 GC 回收。

### 8.11 `weak` 包（Go 1.24+）

`weak.Pointer[T]` 是**弱引用**：不会阻止被指向对象被 GC 回收。常用于缓存、规范化表。

```go
import "weak"

obj := &MyObj{...}
wp := weak.Make(obj)

// 使用时要 Value()，可能已被回收返回 nil
if v := wp.Value(); v != nil {
    use(v)
}
```

搭配 `runtime.AddCleanup`（Go 1.24+，替代 `runtime.SetFinalizer`）可以构建稳健的对象池/缓存：

```go
import "runtime"

obj := &File{fd: openFD()}
// 当 obj 被 GC 时，runtime 会调用 cleanup(fd)
runtime.AddCleanup(obj, func(fd int) { syscall.Close(fd) }, obj.fd)
```

> `runtime.SetFinalizer` 仍可用但已**不推荐**：它会重新激活对象，存在循环 finalizer 风险，`AddCleanup` 显式分离对象与清理参数解决了这些问题。

### 8.12 `structs` 包与 `omitzero`（Go 1.24+）

JSON tag 新增 `omitzero` 选项：以 **零值判定**而非 `omitempty` 的"长度/空值"判定，更准确（特别是对 `time.Time`、自定义类型）：

```go
type Event struct {
    Title    string    `json:"title"`
    StartAt  time.Time `json:"start_at,omitzero"` // time.Time{} 不会被序列化
}
```

也支持自定义零值判定：实现 `IsZero() bool` 即可。

`structs.HostLayout` 标签结构（用于 cgo 互操作内存布局），属于较少用的底层 API。

### 8.13 `os.Root`：防目录穿越的文件 API（Go 1.24+）

服务器处理用户提供的路径时，`os.Root` 把所有 I/O 限制在指定目录内，**符号链接也不能逃出**，从根本上消除 Path Traversal 漏洞：

```go
root, err := os.OpenRoot("/var/uploads")
if err != nil { panic(err) }
defer root.Close()

f, err := root.Open(userPath) // 任何指向根外的路径直接报错
```

替代旧的 `filepath.Join + 校验前缀` 的脆弱写法。

### 8.14 `encoding/json/v2`（Go 1.25 实验性）

Go 1.25 引入 `encoding/json/v2`（须通过 `GOEXPERIMENT=jsonv2` 启用），目标是修正 v1 多年积累的设计问题：

- 显著提升的反序列化性能（针对大对象 ~2-3x）。
- 一致的 `MarshalJSON`/`UnmarshalJSON` 调用语义。
- 内置 `omitzero`，行为与 v1 兼容选项可配置。
- 流式 `Decoder.Decode` 不再需要预读整段。

生产环境**仍建议使用 v1**，等待 Go 1.26+ 正式稳定后再迁移。

### 8.15 embed包（Go 1.16+）

```go
import "embed"

// 嵌入单个文件
//go:embed config.json
var configData []byte

// 嵌入为字符串
//go:embed version.txt
var version string

// 嵌入整个目录
//go:embed static/*
var staticFiles embed.FS

// 在HTTP服务中使用嵌入文件
func main() {
    // 作为静态文件服务
    http.Handle("/static/", http.FileServer(http.FS(staticFiles)))
    
    // 读取嵌入文件
    data, err := staticFiles.ReadFile("static/index.html")
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(data))
}
```

---

## 第九章：项目工程化

### 9.1 Go Modules详解

```bash
# 初始化模块
go mod init github.com/yourname/project

# go.mod 文件内容
module github.com/yourname/project

go 1.25            // 最低语言版本
toolchain go1.25.3 // 推荐用的工具链版本（Go 1.21+）；
                   // 如本机版本低于 toolchain，go 命令会自动下载。

require (
    github.com/gin-gonic/gin v1.10.0
    gorm.io/gorm v1.26.0
)

require (
    // 间接依赖（自动管理）
    github.com/bytedance/sonic v1.13.0 // indirect
)

// Go 1.24+：tool 指令
// 替代过去 "在一个 _ "import" 文件里假装依赖工具" 的 hack。
// 把 go run 工具的版本固定到 go.mod 里，团队成员 / CI 一键复现。
tool (
    golang.org/x/tools/cmd/stringer
    google.golang.org/protobuf/cmd/protoc-gen-go
    github.com/google/wire/cmd/wire
)
// 使用： go tool stringer -type=Color
//        go tool wire ./...
```

**`GOTOOLCHAIN` 与版本管理**（Go 1.21+）：

- `go.mod` 的 `go 1.25` 是**最低语言版本要求**——本地工具链旧于此值，命令会失败。
- `toolchain go1.25.3` 是**推荐版本**——更高优先级，会自动下载并使用对应工具链。
- 环境变量 `GOTOOLCHAIN` 可强制覆盖：`GOTOOLCHAIN=go1.25.3 go build` / `GOTOOLCHAIN=local`（强制使用本地版本）。

**版本选择算法MVS（Minimal Version Selection）**：
- Go选择满足所有约束的**最小版本**（不是最新版本）
- 比npm/Maven的依赖解析更确定性，避免"钻石依赖"问题

```bash
# 常用命令
go mod tidy          # 添加缺失、移除多余的依赖
go mod download      # 下载依赖到缓存
go mod verify        # 验证依赖完整性
go mod graph         # 打印依赖图
go mod why <module>  # 解释为何需要某依赖
go get -u ./...      # 更新所有直接依赖

# 版本指定
go get github.com/pkg@v1.2.3   # 精确版本
go get github.com/pkg@latest   # 最新版本
go get github.com/pkg@master   # 特定分支
```

### 9.2 项目目录结构

```
project/
├── cmd/                    # 可执行文件入口
│   ├── api/
│   │   └── main.go        # API服务入口
│   └── worker/
│       └── main.go        # 后台Worker入口
├── internal/               # 私有代码（其他模块不能导入）
│   ├── handler/            # HTTP处理器
│   ├── service/            # 业务逻辑
│   ├── repository/         # 数据访问
│   └── model/              # 数据模型
├── pkg/                    # 公共库（可被外部导入）
│   ├── logger/
│   └── utils/
├── api/                    # API定义（OpenAPI/Protobuf）
├── configs/                # 配置文件
├── scripts/                # 脚本
├── test/                   # 集成测试
├── go.mod
├── go.sum
├── Makefile
└── Dockerfile
```

**关键约定**：
- `internal/`：Go编译器强制保证，外部模块无法导入此目录下的包
- `cmd/`：每个子目录一个main包，编译为一个二进制文件
- `pkg/`：可选，用于可被外部复用的公共库

### 9.3 代码规范与工具

```bash
# gofmt：官方格式化工具（强制统一风格，不可配置）
gofmt -w .

# goimports：gofmt + 自动管理import
go install golang.org/x/tools/cmd/goimports@latest
goimports -w .

# golangci-lint：多合一lint工具（集成几十个检查器）
# 安装: https://golangci-lint.run/usage/install/
golangci-lint run ./...

# .golangci.yml 配置示例
linters:
  enable:
    - errcheck      # 检查未处理的错误
    - gosimple      # 简化代码建议
    - govet         # 可疑代码检查
    - ineffassign   # 无效赋值
    - staticcheck   # 静态分析
    - unused        # 未使用的代码
    - gosec         # 安全检查
```

### 9.4 构建与交叉编译

```bash
# 基本构建
go build -o bin/app ./cmd/api

# 交叉编译（Go天然支持，无需额外工具）
# 编译Linux版本（在Windows/Mac上）
GOOS=linux GOARCH=amd64 go build -o bin/app-linux ./cmd/api

# 编译Mac ARM版本
GOOS=darwin GOARCH=arm64 go build -o bin/app-mac ./cmd/api

# 编译Windows版本
GOOS=windows GOARCH=amd64 go build -o bin/app.exe ./cmd/api

# 减小二进制体积
go build -ldflags="-s -w" -o bin/app ./cmd/api
# -s 去掉符号表  -w 去掉调试信息

# 注入版本信息
go build -ldflags="-X main.version=1.0.0 -X main.buildTime=$(date -u +%Y%m%d%H%M%S)" ./cmd/api
```

### 9.5 Makefile

```makefile
.PHONY: build run test lint clean

APP_NAME := myapp
VERSION := $(shell git describe --tags --always)
BUILD_TIME := $(shell date -u +%Y%m%d%H%M%S)
LDFLAGS := -ldflags "-X main.version=$(VERSION) -X main.buildTime=$(BUILD_TIME) -s -w"

build:
	go build $(LDFLAGS) -o bin/$(APP_NAME) ./cmd/api

run:
	go run ./cmd/api

test:
	go test -race -cover ./...

lint:
	golangci-lint run ./...

clean:
	rm -rf bin/

docker:
	docker build -t $(APP_NAME):$(VERSION) .

# 交叉编译所有平台
build-all:
	GOOS=linux GOARCH=amd64 go build $(LDFLAGS) -o bin/$(APP_NAME)-linux-amd64 ./cmd/api
	GOOS=darwin GOARCH=arm64 go build $(LDFLAGS) -o bin/$(APP_NAME)-darwin-arm64 ./cmd/api
	GOOS=windows GOARCH=amd64 go build $(LDFLAGS) -o bin/$(APP_NAME)-windows-amd64.exe ./cmd/api
```

### 9.6 依赖注入（Wire）

Wire是Google出品的编译时依赖注入工具：

```go
// 安装
// go install github.com/google/wire/cmd/wire@latest

// provider函数（提供依赖）
func NewDB(cfg *Config) (*sql.DB, error) {
    return sql.Open("mysql", cfg.DSN)
}

func NewUserRepo(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}

func NewUserService(repo *UserRepository) *UserService {
    return &UserService{repo: repo}
}

// wire.go（Wire的注入定义文件）
//go:build wireinject

package main

import "github.com/google/wire"

func InitializeApp(cfg *Config) (*App, error) {
    wire.Build(
        NewDB,
        NewUserRepo,
        NewUserService,
        NewApp,
    )
    return nil, nil  // Wire会生成实际代码
}

// 运行 wire 命令会生成 wire_gen.go
```

**Java对比**：Wire类似Spring的DI，但在编译时完成注入（无反射），性能更好，错误在编译期暴露。

### 9.7 配置管理（Viper）

```go
import "github.com/spf13/viper"

// 配置文件 config.yaml
// server:
//   port: 8080
//   host: localhost
// database:
//   dsn: "user:pass@tcp(localhost:3306)/dbname"
//   max_open: 100

func LoadConfig() (*Config, error) {
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath("./configs")
    viper.AddConfigPath(".")
    
    // 环境变量覆盖（SERVER_PORT会覆盖server.port）
    viper.AutomaticEnv()
    viper.SetEnvPrefix("APP")
    
    // 默认值
    viper.SetDefault("server.port", 8080)
    
    if err := viper.ReadInConfig(); err != nil {
        return nil, err
    }
    
    var cfg Config
    if err := viper.Unmarshal(&cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}

type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
}

type ServerConfig struct {
    Port int    `mapstructure:"port"`
    Host string `mapstructure:"host"`
}

type DatabaseConfig struct {
    DSN     string `mapstructure:"dsn"`
    MaxOpen int    `mapstructure:"max_open"`
}
```

---

## 第十章：Web开发框架

### 10.1 标准库 net/http 构建Web服务

Go标准库的net/http已经足够强大，适合简单服务：

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
    "time"
)

type Response struct {
    Code    int         `json:"code"`
    Message string      `json:"message"`
    Data    interface{} `json:"data,omitempty"`
}

func jsonResponse(w http.ResponseWriter, status int, resp Response) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    json.NewEncoder(w).Encode(resp)
}

// 中间件模式
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /api/health", func(w http.ResponseWriter, r *http.Request) {
        jsonResponse(w, http.StatusOK, Response{Code: 0, Message: "ok"})
    })

    handler := loggingMiddleware(mux)

    server := &http.Server{
        Addr:         ":8080",
        Handler:      handler,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }
    log.Fatal(server.ListenAndServe())
}
```

### 10.2 Gin框架

Gin是Go生态中最流行的Web框架，高性能（基于httprouter），API友好。

```bash
go get -u github.com/gin-gonic/gin
```

#### 基础使用

```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()  // 包含Logger和Recovery中间件

    // 路由
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(http.StatusOK, gin.H{"message": "pong"})
    })

    // 路径参数
    r.GET("/users/:id", func(c *gin.Context) {
        id := c.Param("id")
        c.JSON(http.StatusOK, gin.H{"id": id})
    })

    // 查询参数
    r.GET("/search", func(c *gin.Context) {
        keyword := c.DefaultQuery("q", "")
        page := c.DefaultQuery("page", "1")
        c.JSON(http.StatusOK, gin.H{"keyword": keyword, "page": page})
    })

    r.Run(":8080")
}
```

#### 参数绑定与验证

```go
// 请求体绑定
type CreateUserRequest struct {
    Name     string `json:"name" binding:"required,min=2,max=50"`
    Email    string `json:"email" binding:"required,email"`
    Age      int    `json:"age" binding:"required,gte=1,lte=150"`
    Password string `json:"password" binding:"required,min=8"`
}

func createUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    // 处理业务逻辑...
    c.JSON(http.StatusCreated, gin.H{"id": 1, "name": req.Name})
}
```

#### 路由分组

```go
func main() {
    r := gin.Default()

    // API v1分组
    v1 := r.Group("/api/v1")
    {
        users := v1.Group("/users")
        {
            users.GET("", listUsers)
            users.POST("", createUser)
            users.GET("/:id", getUser)
            users.PUT("/:id", updateUser)
            users.DELETE("/:id", deleteUser)
        }

        // 需要认证的路由
        auth := v1.Group("/admin")
        auth.Use(AuthMiddleware())
        {
            auth.GET("/dashboard", dashboard)
        }
    }

    r.Run(":8080")
}
```

#### 中间件

```go
// 自定义中间件
func AuthMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
            return
        }

        claims, err := validateToken(token)
        if err != nil {
            c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
            return
        }

        // 将用户信息存入context
        c.Set("userID", claims.UserID)
        c.Next()  // 继续处理
    }
}

// CORS中间件
func CORSMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
        c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

        if c.Request.Method == "OPTIONS" {
            c.AbortWithStatus(http.StatusNoContent)
            return
        }

        c.Next()
    }
}

// 限流中间件
func RateLimitMiddleware(rps int) gin.HandlerFunc {
    limiter := rate.NewLimiter(rate.Limit(rps), rps)
    return func(c *gin.Context) {
        if !limiter.Allow() {
            c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{"error": "rate limit exceeded"})
            return
        }
        c.Next()
    }
}
```

### 10.3 GORM

GORM是Go中最流行的ORM框架。

```bash
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

#### 模型定义

```go
import (
    "gorm.io/gorm"
    "time"
)

// 模型定义（struct tag控制映射）
type User struct {
    ID        uint           `gorm:"primaryKey;autoIncrement" json:"id"`
    Name      string         `gorm:"size:100;not null" json:"name"`
    Email     string         `gorm:"size:200;uniqueIndex" json:"email"`
    Age       int            `gorm:"default:0" json:"age"`
    Role      string         `gorm:"size:20;default:user" json:"role"`
    Profile   Profile        `gorm:"foreignKey:UserID" json:"profile,omitempty"`
    Orders    []Order        `gorm:"foreignKey:UserID" json:"orders,omitempty"`
    CreatedAt time.Time      `json:"created_at"`
    UpdatedAt time.Time      `json:"updated_at"`
    DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`  // 软删除
}

type Profile struct {
    ID     uint   `gorm:"primaryKey"`
    UserID uint   `gorm:"uniqueIndex"`
    Bio    string `gorm:"size:500"`
    Avatar string `gorm:"size:200"`
}

type Order struct {
    ID     uint    `gorm:"primaryKey"`
    UserID uint    `gorm:"index"`
    Amount float64 `gorm:"not null"`
    Status string  `gorm:"size:20;default:pending"`
}
```

#### CRUD操作

```go
// 初始化
import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

dsn := "user:pass@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})

// 自动迁移
db.AutoMigrate(&User{}, &Profile{}, &Order{})

// Create
user := User{Name: "Alice", Email: "alice@example.com", Age: 25}
result := db.Create(&user)  // user.ID会被自动填充
fmt.Println(user.ID, result.RowsAffected)

// Read
var u User
db.First(&u, 1)                          // 按主键查找
db.First(&u, "email = ?", "alice@example.com")  // 条件查找
db.Where("age > ?", 18).Find(&users)     // 多条记录
db.Preload("Profile").Preload("Orders").Find(&users)  // 预加载关联

// Update
db.Model(&user).Update("name", "Bob")
db.Model(&user).Updates(User{Name: "Bob", Age: 30})
db.Model(&user).Updates(map[string]interface{}{"name": "Bob", "age": 30})

// Delete（软删除）
db.Delete(&user, 1)

// 事务
db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Create(&user).Error; err != nil {
        return err  // 返回错误会自动回滚
    }
    if err := tx.Create(&order).Error; err != nil {
        return err
    }
    return nil  // 返回nil提交事务
})
```

**Java对比**：GORM类似JPA/Hibernate，但没有那么"魔法"。相比MyBatis，GORM更自动化。

### 10.4 数据库操作（database/sql + sqlx）

```go
// 当GORM太重或需要更精细控制时，使用database/sql或sqlx
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
    "github.com/jmoiron/sqlx"
)

// sqlx：database/sql的增强版，支持结构体映射
db, err := sqlx.Connect("mysql", dsn)
db.SetMaxOpenConns(100)
db.SetMaxIdleConns(10)
db.SetConnMaxLifetime(time.Hour)

type User struct {
    ID    int64  `db:"id"`
    Name  string `db:"name"`
    Email string `db:"email"`
}

// 查询单条
var user User
err := db.Get(&user, "SELECT * FROM users WHERE id = ?", 1)

// 查询多条
var users []User
err := db.Select(&users, "SELECT * FROM users WHERE age > ?", 18)

// 命名参数
result, err := db.NamedExec(
    "INSERT INTO users (name, email) VALUES (:name, :email)",
    map[string]interface{}{"name": "Alice", "email": "alice@example.com"},
)
```

### 10.5 Redis操作

```go
import "github.com/redis/go-redis/v9"

func NewRedisClient() *redis.Client {
    return redis.NewClient(&redis.Options{
        Addr:     "localhost:6379",
        Password: "",
        DB:       0,
        PoolSize: 100,
    })
}

func main() {
    ctx := context.Background()
    rdb := NewRedisClient()

    // String
    rdb.Set(ctx, "key", "value", 10*time.Minute)
    val, err := rdb.Get(ctx, "key").Result()

    // Hash
    rdb.HSet(ctx, "user:1", "name", "Alice", "age", 25)
    name, _ := rdb.HGet(ctx, "user:1", "name").Result()

    // List
    rdb.LPush(ctx, "queue", "task1", "task2")
    task, _ := rdb.RPop(ctx, "queue").Result()

    // Set
    rdb.SAdd(ctx, "online_users", "user1", "user2")
    members, _ := rdb.SMembers(ctx, "online_users").Result()

    // Sorted Set
    rdb.ZAdd(ctx, "leaderboard", redis.Z{Score: 100, Member: "player1"})
    top, _ := rdb.ZRevRangeWithScores(ctx, "leaderboard", 0, 9).Result()

    // Pipeline（批量操作）
    pipe := rdb.Pipeline()
    pipe.Set(ctx, "key1", "val1", 0)
    pipe.Set(ctx, "key2", "val2", 0)
    pipe.Exec(ctx)

    // 分布式锁（简化版）
    lock, err := rdb.SetNX(ctx, "lock:resource", "owner", 10*time.Second).Result()
    if lock {
        defer rdb.Del(ctx, "lock:resource")
        // 执行临界区代码
    }
}
```

### 10.6 JWT认证

```go
import "github.com/golang-jwt/jwt/v5"

var jwtSecret = []byte("your-secret-key")

type Claims struct {
    UserID int64  `json:"user_id"`
    Role   string `json:"role"`
    jwt.RegisteredClaims
}

// 生成Token
func GenerateToken(userID int64, role string) (string, error) {
    claims := Claims{
        UserID: userID,
        Role:   role,
        RegisteredClaims: jwt.RegisteredClaims{
            ExpiresAt: jwt.NewNumericDate(time.Now().Add(24 * time.Hour)),
            IssuedAt:  jwt.NewNumericDate(time.Now()),
            Issuer:    "myapp",
        },
    }

    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(jwtSecret)
}

// 解析Token
func ParseToken(tokenString string) (*Claims, error) {
    token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (interface{}, error) {
        return jwtSecret, nil
    })
    if err != nil {
        return nil, err
    }

    claims, ok := token.Claims.(*Claims)
    if !ok || !token.Valid {
        return nil, fmt.Errorf("invalid token")
    }
    return claims, nil
}
```

### 10.7 优雅关闭

```go
func main() {
    r := gin.Default()
    // 注册路由...

    srv := &http.Server{
        Addr:    ":8080",
        Handler: r,
    }

    // 在goroutine中启动服务
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("listen: %s\n", err)
        }
    }()

    // 等待中断信号
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    log.Println("Shutting down server...")

    // 给5秒处理完当前请求
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }
    log.Println("Server exiting")
}
```

---

## 第十一章：网络编程与长连接

### 11.1 TCP编程

```go
// TCP服务端
func startTCPServer() {
    listener, err := net.Listen("tcp", ":9000")
    if err != nil {
        log.Fatal(err)
    }
    defer listener.Close()

    for {
        conn, err := listener.Accept()
        if err != nil {
            log.Println("accept error:", err)
            continue
        }
        go handleConn(conn)
    }
}

func handleConn(conn net.Conn) {
    defer conn.Close()
    buf := make([]byte, 4096)
    for {
        n, err := conn.Read(buf)
        if err != nil {
            return
        }
        // 回显
        conn.Write(buf[:n])
    }
}

// TCP粘包处理（Length-Prefixed协议）
// 消息格式：[4字节长度][消息体]
func readMessage(conn net.Conn) ([]byte, error) {
    header := make([]byte, 4)
    if _, err := io.ReadFull(conn, header); err != nil {
        return nil, err
    }
    length := binary.BigEndian.Uint32(header)
    
    body := make([]byte, length)
    if _, err := io.ReadFull(conn, body); err != nil {
        return nil, err
    }
    return body, nil
}

func writeMessage(conn net.Conn, data []byte) error {
    header := make([]byte, 4)
    binary.BigEndian.PutUint32(header, uint32(len(data)))
    if _, err := conn.Write(header); err != nil {
        return err
    }
    _, err := conn.Write(data)
    return err
}
```

### 11.2 WebSocket

```go
// 使用 gorilla/websocket（最成熟的WebSocket库）
import "github.com/gorilla/websocket"

var upgrader = websocket.Upgrader{
    ReadBufferSize:  1024,
    WriteBufferSize: 1024,
    CheckOrigin: func(r *http.Request) bool {
        return true  // 生产中应检查Origin
    },
}

func wsHandler(w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Println("upgrade error:", err)
        return
    }
    defer conn.Close()

    for {
        messageType, message, err := conn.ReadMessage()
        if err != nil {
            if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway) {
                log.Printf("error: %v", err)
            }
            break
        }
        // 回显消息
        err = conn.WriteMessage(messageType, message)
        if err != nil {
            break
        }
    }
}
```

### 11.3 长连接管理

```go
// 连接管理器
type ConnectionManager struct {
    connections map[string]*Connection
    mu          sync.RWMutex
    register    chan *Connection
    unregister  chan *Connection
    broadcast   chan []byte
}

type Connection struct {
    ID       string
    UserID   int64
    Conn     *websocket.Conn
    Send     chan []byte
    manager  *ConnectionManager
    lastPing time.Time
}

func NewConnectionManager() *ConnectionManager {
    return &ConnectionManager{
        connections: make(map[string]*Connection),
        register:    make(chan *Connection),
        unregister:  make(chan *Connection),
        broadcast:   make(chan []byte, 256),
    }
}

func (m *ConnectionManager) Run() {
    for {
        select {
        case conn := <-m.register:
            m.mu.Lock()
            m.connections[conn.ID] = conn
            m.mu.Unlock()

        case conn := <-m.unregister:
            m.mu.Lock()
            if _, ok := m.connections[conn.ID]; ok {
                delete(m.connections, conn.ID)
                close(conn.Send)
            }
            m.mu.Unlock()

        case message := <-m.broadcast:
            m.mu.RLock()
            for _, conn := range m.connections {
                select {
                case conn.Send <- message:
                default:
                    close(conn.Send)
                    delete(m.connections, conn.ID)
                }
            }
            m.mu.RUnlock()
        }
    }
}

// 心跳检测
func (c *Connection) readPump() {
    defer func() {
        c.manager.unregister <- c
        c.Conn.Close()
    }()

    c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
    c.Conn.SetPongHandler(func(string) error {
        c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
        return nil
    })

    for {
        _, message, err := c.Conn.ReadMessage()
        if err != nil {
            break
        }
        // 处理消息...
        _ = message
    }
}

func (c *Connection) writePump() {
    ticker := time.NewTicker(30 * time.Second)
    defer func() {
        ticker.Stop()
        c.Conn.Close()
    }()

    for {
        select {
        case message, ok := <-c.Send:
            if !ok {
                c.Conn.WriteMessage(websocket.CloseMessage, []byte{})
                return
            }
            c.Conn.WriteMessage(websocket.TextMessage, message)

        case <-ticker.C:
            // 发送Ping心跳
            if err := c.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                return
            }
        }
    }
}
```

### 11.4 Protocol Buffers + gRPC

```protobuf
// user.proto
syntax = "proto3";
package user;
option go_package = "./pb";

service UserService {
    rpc GetUser(GetUserRequest) returns (UserResponse);
    rpc ListUsers(ListUsersRequest) returns (stream UserResponse);  // 服务端流
}

message GetUserRequest {
    int64 id = 1;
}

message UserResponse {
    int64 id = 1;
    string name = 2;
    string email = 3;
}
```

```go
// gRPC服务端实现
import (
    "google.golang.org/grpc"
    pb "myproject/pb"
)

type userServer struct {
    pb.UnimplementedUserServiceServer
}

func (s *userServer) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.UserResponse, error) {
    // 查询用户...
    return &pb.UserResponse{
        Id:    req.Id,
        Name:  "Alice",
        Email: "alice@example.com",
    }, nil
}

func main() {
    lis, _ := net.Listen("tcp", ":50051")
    s := grpc.NewServer()
    pb.RegisterUserServiceServer(s, &userServer{})
    s.Serve(lis)
}
```

### 11.5 消息序列化方案对比

| 方案 | 大小 | 速度 | 可读性 | 适用场景 |
|------|------|------|--------|----------|
| JSON | 大 | 慢 | 好 | REST API, 调试 |
| Protocol Buffers | 小 | 快 | 差 | 微服务间通信, 游戏 |
| MessagePack | 中 | 快 | 差 | 游戏实时通信 |
| FlatBuffers | 最小 | 最快（零拷贝） | 差 | 极致性能场景 |

游戏服务器推荐：**Protobuf**（客户端兼容性好）或 **MessagePack**（更简单灵活）。

### 11.6 实时游戏服务器架构

#### 帧同步 vs 状态同步

| 方案 | 原理 | 优势 | 劣势 | 适合 |
|------|------|------|------|------|
| 帧同步 | 同步玩家输入，各端独立计算 | 流量小，回放简单 | 对延迟敏感，反作弊难 | 格斗/MOBA |
| 状态同步 | 服务器计算，同步状态结果 | 防作弊好，延迟容忍高 | 流量大 | MMO/射击 |

#### 房间模型

```go
type Room struct {
    ID         string
    Players    map[int64]*Player
    MaxPlayers int
    State      RoomState
    mu         sync.RWMutex
    ticker     *time.Ticker
    done       chan struct{}
    broadcast  chan []byte
}

type Player struct {
    ID     int64
    Conn   *Connection
    X, Y   float64
    HP     int
    Ready  bool
}

type RoomState int

const (
    RoomWaiting RoomState = iota
    RoomPlaying
    RoomFinished
)

func NewRoom(id string, maxPlayers int) *Room {
    return &Room{
        ID:         id,
        Players:    make(map[int64]*Player),
        MaxPlayers: maxPlayers,
        State:      RoomWaiting,
        done:       make(chan struct{}),
        broadcast:  make(chan []byte, 256),
    }
}

func (r *Room) Join(player *Player) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    if len(r.Players) >= r.MaxPlayers {
        return fmt.Errorf("room is full")
    }
    if r.State != RoomWaiting {
        return fmt.Errorf("game already started")
    }

    r.Players[player.ID] = player
    return nil
}

// 游戏主循环（Tick-based Update）
func (r *Room) StartGameLoop() {
    r.State = RoomPlaying
    r.ticker = time.NewTicker(time.Second / 30)  // 30 FPS

    go func() {
        frameID := 0
        for {
            select {
            case <-r.ticker.C:
                frameID++
                r.update(frameID)
            case <-r.done:
                r.ticker.Stop()
                return
            }
        }
    }()
}

func (r *Room) update(frameID int) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    // 1. 处理玩家输入
    // 2. 更新游戏状态（碰撞检测、伤害计算等）
    // 3. 构建帧数据
    state := r.buildFrameState(frameID)
    
    // 4. 广播给所有玩家
    data, _ := json.Marshal(state)
    for _, player := range r.Players {
        select {
        case player.Conn.Send <- data:
        default:
            // 玩家连接缓冲满，可能断线
        }
    }
}

// 消息协议定义
type MessageType uint16

const (
    MsgJoinRoom    MessageType = 1001
    MsgLeaveRoom   MessageType = 1002
    MsgPlayerMove  MessageType = 2001
    MsgPlayerAttack MessageType = 2002
    MsgGameState   MessageType = 3001
    MsgGameOver    MessageType = 3002
)

type GameMessage struct {
    Type      MessageType `json:"type"`
    Timestamp int64       `json:"ts"`
    Data      json.RawMessage `json:"data"`
}

type MoveData struct {
    X         float64 `json:"x"`
    Y         float64 `json:"y"`
    Direction float64 `json:"dir"`
}
```

### 11.7 相关开源游戏框架

| 框架 | 特点 | GitHub |
|------|------|--------|
| **Nano** | 轻量级，适合中小型游戏 | lonng/nano |
| **Pitaya** | Nano的增强版（TFG维护），支持集群 | topfreegames/pitaya |
| **Leaf** | 模块化设计，适合学习 | name5566/leaf |
| **GoWorld** | 分布式游戏服务器框架 | xiaonanln/goworld |

---

## 第十二章：性能优化与高级特性

### 12.1 内存管理与GC

Go 使用**并发三色标记清除**垃圾回收器，目标是亚毫秒级 STW（Stop-the-World）。

**三色标记算法**：
1. 初始时所有对象为白色
2. 从根对象（栈、全局变量）出发，标记为灰色
3. 取出灰色对象，将其引用的白色对象标记为灰色，自身标记为黑色
4. 重复步骤 3 直到没有灰色对象
5. 白色对象即为垃圾，回收

**混合写屏障**（Go 1.8+）：保证 GC 和程序并发执行时的正确性。

**Green Tea GC（Go 1.25 实验性）**：传统 Go GC 是全堆 mark-sweep，新一代 Green Tea GC 引入「**面向 span 的局部扫描**」，对大堆（数十 GB）和高分配率服务能将 GC CPU 占用降低 10–40%。当前为实验特性，需要 `GOEXPERIMENT=greenteagc` 启用，预计 1.26/1.27 默认开启。

```go
// GC 触发时机：
// 1. 堆内存增长到上次 GC 后的 GOGC 百分比（默认 100%，即翻倍）
// 2. 距离上次 GC 超过 2 分钟
// 3. 手动调用 runtime.GC()
// 4. 接近 GOMEMLIMIT 软上限时（Go 1.19+）

// 查看 GC 信息
// GODEBUG=gctrace=1 go run main.go
```

#### Swiss Tables map 实现（Go 1.24+）

Go 1.24 把内置 `map` 的底层实现从经典 hashmap 切换到 Google **Swiss Tables**：

- 大 map（>10 万元素）查找/迭代速度提升 ~30–60%；
- 小 map 内存占用减少（不再为每桶预留大空槽）；
- 哈希迭代仍是随机的，但顺序与 1.23 不同——不要依赖具体顺序。

完全透明替换，无需改代码；仅影响微基准的绝对数字与某些"恰好依赖旧顺序"的脆弱测试。

#### 容器感知的 GOMAXPROCS（Go 1.25+）

历史上 `GOMAXPROCS` 默认 = `runtime.NumCPU()` = 宿主机核数；在 K8s/容器里只分到 0.5C 也会启动几十个 P，导致 CPU 限流时频繁切换、p99 抖动。Go 1.25 起：

- 启动时**自动读取 cgroup v2 的 CPU 配额**（quota/period），按 ceil 值设置 `GOMAXPROCS`；
- 运行中如果 cgroup 配额被在线变更，`GOMAXPROCS` 也会跟着调整；
- 通过 `GODEBUG=containermaxprocs=0` 可关闭新行为，回到旧逻辑；
- 显式 `runtime.GOMAXPROCS(n)` 或环境变量 `GOMAXPROCS=n` 仍优先生效。

> Java 8u131+ 也是类似演进路径（容器感知 CPU 与堆大小）。在生产 K8s 部署中，**升级到 Go 1.25 通常能直接带来更稳定的 p99**，无需任何代码改动。

### 12.2 GC调优

```go
// GOGC：控制GC触发频率（默认100）
// GOGC=200 表示堆增长到2倍时触发GC（GC更少，内存更多）
// GOGC=50 表示堆增长到1.5倍时触发GC（GC更频繁，内存更少）
// GOGC=off 关闭GC

// GOMEMLIMIT（Go 1.19+）：设置内存软上限
// 更推荐使用GOMEMLIMIT替代GOGC调优
// GOMEMLIMIT=1GiB 设置内存上限1GB

import "runtime/debug"

func init() {
    // 代码中设置
    debug.SetGCPercent(200)
    debug.SetMemoryLimit(1 << 30)  // 1GB
}
```

### 12.3 pprof性能分析

```go
import (
    "net/http"
    _ "net/http/pprof"  // 导入即注册pprof HTTP端点
)

func main() {
    // 方式1：HTTP服务中自带pprof
    go func() {
        http.ListenAndServe(":6060", nil)
    }()
    
    // 访问 http://localhost:6060/debug/pprof/
    // 主要端点：
    // /debug/pprof/goroutine  - goroutine堆栈
    // /debug/pprof/heap       - 堆内存分配
    // /debug/pprof/profile    - CPU分析（默认30秒）
    // /debug/pprof/trace      - 执行追踪
}

// 方式2：代码中手动收集
import "runtime/pprof"

func cpuProfile() {
    f, _ := os.Create("cpu.prof")
    pprof.StartCPUProfile(f)
    defer pprof.StopCPUProfile()
    
    // 执行要分析的代码...
}

func memProfile() {
    f, _ := os.Create("mem.prof")
    defer f.Close()
    runtime.GC()  // 先触发GC
    pprof.WriteHeapProfile(f)
}

// 分析命令
// go tool pprof cpu.prof
// go tool pprof -http=:8080 cpu.prof  (Web UI)
// go tool pprof http://localhost:6060/debug/pprof/heap
```

### 12.4 逃逸分析

编译器决定变量分配在栈上还是堆上。栈分配更快（无GC开销）。

```go
// 查看逃逸分析结果
// go build -gcflags="-m" main.go

// 会逃逸到堆的情况：
func escape() *int {
    x := 42
    return &x  // x逃逸：返回了局部变量的指针
}

// 不会逃逸
func noEscape() int {
    x := 42
    return x  // x留在栈上
}

// 接口调用通常导致逃逸
func printAny(v interface{}) {
    fmt.Println(v)  // v逃逸到堆
}

// 大对象可能逃逸
func bigAlloc() {
    s := make([]byte, 1<<20)  // 1MB，可能逃逸
    _ = s
}
```

### 12.5 内存对齐

```go
import "unsafe"

// 结构体字段顺序影响内存大小
type Bad struct {
    a bool    // 1字节 + 7字节padding
    b int64   // 8字节
    c bool    // 1字节 + 7字节padding
}
// sizeof(Bad) = 24

type Good struct {
    b int64   // 8字节
    a bool    // 1字节
    c bool    // 1字节 + 6字节padding
}
// sizeof(Good) = 16

func main() {
    fmt.Println(unsafe.Sizeof(Bad{}))   // 24
    fmt.Println(unsafe.Sizeof(Good{}))  // 16
}
```

### 12.6 sync.Pool对象复用

```go
// 减少GC压力，复用临时对象
var bufferPool = sync.Pool{
    New: func() any {
        return bytes.NewBuffer(make([]byte, 0, 4096))
    },
}

func processRequest(data []byte) []byte {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        bufferPool.Put(buf)
    }()
    
    buf.Write(data)
    // 处理...
    return buf.Bytes()
}

// 实际案例：JSON编码器复用
var encoderPool = sync.Pool{
    New: func() any {
        return &bytes.Buffer{}
    },
}

func jsonEncode(v any) ([]byte, error) {
    buf := encoderPool.Get().(*bytes.Buffer)
    defer func() {
        buf.Reset()
        encoderPool.Put(buf)
    }()
    
    encoder := json.NewEncoder(buf)
    if err := encoder.Encode(v); err != nil {
        return nil, err
    }
    
    result := make([]byte, buf.Len())
    copy(result, buf.Bytes())
    return result, nil
}
```

### 12.7 字符串与[]byte高效转换

```go
import "unsafe"

// 标准转换（会复制数据）
s := "hello"
b := []byte(s)  // 分配+复制
s2 := string(b) // 分配+复制

// 零拷贝转换（unsafe，需要确保不修改数据）
// Go 1.20+ 推荐使用 unsafe.String 和 unsafe.Slice
func stringToBytes(s string) []byte {
    return unsafe.Slice(unsafe.StringData(s), len(s))
}

func bytesToString(b []byte) string {
    return unsafe.String(unsafe.SliceData(b), len(b))
}
```

### 12.8 反射（reflect）

```go
import "reflect"

type User struct {
    Name string `json:"name" validate:"required"`
    Age  int    `json:"age" validate:"gte=0"`
}

func inspectStruct(v interface{}) {
    t := reflect.TypeOf(v)
    val := reflect.ValueOf(v)

    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        value := val.Field(i)
        tag := field.Tag.Get("json")
        fmt.Printf("Field: %s, Type: %v, Value: %v, Tag: %s\n",
            field.Name, field.Type, value, tag)
    }
}

// 反射的性能代价很大（比直接调用慢10-100倍）
// 使用场景：ORM、序列化库、依赖注入框架
// 生产代码中尽量避免，用代码生成替代
```

---

## 第十三章：实战项目示例

### 13.1 实时战斗游戏服务器（WebSocket）

以下是一个简化但完整的实时战斗游戏服务器骨架：

```go
package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "sync"
    "sync/atomic"
    "time"

    "github.com/gorilla/websocket"
)

// ==================== 消息协议 ====================

type MsgType uint16

const (
    MsgLogin       MsgType = 1001
    MsgJoinRoom    MsgType = 1002
    MsgLeaveRoom   MsgType = 1003
    MsgReady       MsgType = 1004
    MsgMove        MsgType = 2001
    MsgAttack      MsgType = 2002
    MsgSkill       MsgType = 2003
    MsgGameState   MsgType = 3001
    MsgGameStart   MsgType = 3002
    MsgGameOver    MsgType = 3003
    MsgError       MsgType = 9999
)

type Message struct {
    Type MsgType         `json:"type"`
    Data json.RawMessage `json:"data"`
}

type LoginData struct {
    PlayerID int64  `json:"player_id"`
    Token    string `json:"token"`
}

type MoveData struct {
    X   float64 `json:"x"`
    Y   float64 `json:"y"`
    Dir float64 `json:"dir"`
}

type AttackData struct {
    TargetID int64 `json:"target_id"`
    SkillID  int   `json:"skill_id"`
}

type GameStateData struct {
    Frame   int           `json:"frame"`
    Players []PlayerState `json:"players"`
}

type PlayerState struct {
    ID   int64   `json:"id"`
    X    float64 `json:"x"`
    Y    float64 `json:"y"`
    HP   int     `json:"hp"`
    Dir  float64 `json:"dir"`
    Dead bool    `json:"dead"`
}

// ==================== 玩家连接 ====================

type Player struct {
    ID       int64
    Conn     *websocket.Conn
    Send     chan []byte
    Room     *Room
    X, Y     float64
    HP       int
    MaxHP    int
    Dir      float64
    Dead     bool
    Ready    bool
    mu       sync.Mutex
}

func NewPlayer(id int64, conn *websocket.Conn) *Player {
    return &Player{
        ID:    id,
        Conn:  conn,
        Send:  make(chan []byte, 256),
        HP:    100,
        MaxHP: 100,
    }
}

func (p *Player) ReadPump(server *GameServer) {
    defer func() {
        server.Disconnect(p)
        p.Conn.Close()
    }()

    p.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
    p.Conn.SetPongHandler(func(string) error {
        p.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
        return nil
    })

    for {
        _, data, err := p.Conn.ReadMessage()
        if err != nil {
            break
        }

        var msg Message
        if err := json.Unmarshal(data, &msg); err != nil {
            continue
        }
        server.HandleMessage(p, &msg)
    }
}

func (p *Player) WritePump() {
    ticker := time.NewTicker(30 * time.Second)
    defer func() {
        ticker.Stop()
        p.Conn.Close()
    }()

    for {
        select {
        case message, ok := <-p.Send:
            if !ok {
                p.Conn.WriteMessage(websocket.CloseMessage, []byte{})
                return
            }
            p.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
            p.Conn.WriteMessage(websocket.TextMessage, message)

        case <-ticker.C:
            p.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
            if err := p.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                return
            }
        }
    }
}

func (p *Player) SendMsg(msgType MsgType, data interface{}) {
    raw, _ := json.Marshal(data)
    msg := Message{Type: msgType, Data: raw}
    bytes, _ := json.Marshal(msg)
    select {
    case p.Send <- bytes:
    default:
        // 缓冲满，丢弃消息或断开连接
    }
}

// ==================== 房间管理 ====================

type RoomState int32

const (
    StateWaiting RoomState = iota
    StatePlaying
    StateFinished
)

type Room struct {
    ID         string
    Players    map[int64]*Player
    MaxPlayers int
    State      RoomState
    Frame      int
    mu         sync.RWMutex
    done       chan struct{}
}

func NewRoom(id string, maxPlayers int) *Room {
    return &Room{
        ID:         id,
        Players:    make(map[int64]*Player),
        MaxPlayers: maxPlayers,
        State:      StateWaiting,
        done:       make(chan struct{}),
    }
}

func (r *Room) Join(p *Player) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    if len(r.Players) >= r.MaxPlayers {
        return fmt.Errorf("room full")
    }
    if r.State != StateWaiting {
        return fmt.Errorf("game in progress")
    }

    r.Players[p.ID] = p
    p.Room = r
    p.X = float64(len(r.Players)) * 100
    p.Y = 300
    p.HP = p.MaxHP
    p.Dead = false
    return nil
}

func (r *Room) Leave(p *Player) {
    r.mu.Lock()
    defer r.mu.Unlock()
    delete(r.Players, p.ID)
    p.Room = nil
}

func (r *Room) StartGame() {
    r.mu.Lock()
    r.State = StatePlaying
    r.Frame = 0
    r.mu.Unlock()

    // 通知所有玩家游戏开始
    r.Broadcast(MsgGameStart, map[string]interface{}{
        "players": r.getPlayerStates(),
    })

    // 启动游戏循环 (20 ticks/second)
    go r.gameLoop()
}

func (r *Room) gameLoop() {
    ticker := time.NewTicker(50 * time.Millisecond) // 20 FPS
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            r.mu.Lock()
            r.Frame++
            r.update()
            r.mu.Unlock()

            // 每帧广播状态
            r.Broadcast(MsgGameState, GameStateData{
                Frame:   r.Frame,
                Players: r.getPlayerStates(),
            })

            // 检查游戏结束
            if r.checkGameOver() {
                r.mu.Lock()
                r.State = StateFinished
                r.mu.Unlock()
                r.Broadcast(MsgGameOver, map[string]interface{}{
                    "winner": r.getWinner(),
                })
                return
            }

        case <-r.done:
            return
        }
    }
}

func (r *Room) update() {
    // 游戏逻辑更新（碰撞检测、技能冷却等）
    for _, p := range r.Players {
        if p.Dead {
            continue
        }
        // 更新位置、状态等
    }
}

func (r *Room) checkGameOver() bool {
    alive := 0
    for _, p := range r.Players {
        if !p.Dead {
            alive++
        }
    }
    return alive <= 1
}

func (r *Room) getWinner() int64 {
    for _, p := range r.Players {
        if !p.Dead {
            return p.ID
        }
    }
    return 0
}

func (r *Room) getPlayerStates() []PlayerState {
    states := make([]PlayerState, 0, len(r.Players))
    for _, p := range r.Players {
        states = append(states, PlayerState{
            ID: p.ID, X: p.X, Y: p.Y,
            HP: p.HP, Dir: p.Dir, Dead: p.Dead,
        })
    }
    return states
}

func (r *Room) Broadcast(msgType MsgType, data interface{}) {
    raw, _ := json.Marshal(data)
    msg := Message{Type: msgType, Data: raw}
    bytes, _ := json.Marshal(msg)

    r.mu.RLock()
    defer r.mu.RUnlock()
    for _, p := range r.Players {
        select {
        case p.Send <- bytes:
        default:
        }
    }
}

// ==================== 游戏服务器 ====================

type GameServer struct {
    Players    map[int64]*Player
    Rooms      map[string]*Room
    mu         sync.RWMutex
    roomIDSeq  atomic.Int64
    upgrader   websocket.Upgrader
}

func NewGameServer() *GameServer {
    return &GameServer{
        Players: make(map[int64]*Player),
        Rooms:   make(map[string]*Room),
        upgrader: websocket.Upgrader{
            CheckOrigin: func(r *http.Request) bool { return true },
        },
    }
}

func (s *GameServer) HandleWebSocket(w http.ResponseWriter, r *http.Request) {
    conn, err := s.upgrader.Upgrade(w, r, nil)
    if err != nil {
        return
    }

    // 等待登录消息
    _, data, err := conn.ReadMessage()
    if err != nil {
        conn.Close()
        return
    }

    var msg Message
    json.Unmarshal(data, &msg)
    if msg.Type != MsgLogin {
        conn.Close()
        return
    }

    var login LoginData
    json.Unmarshal(msg.Data, &login)

    player := NewPlayer(login.PlayerID, conn)

    s.mu.Lock()
    s.Players[player.ID] = player
    s.mu.Unlock()

    go player.WritePump()
    go player.ReadPump(s)
}

func (s *GameServer) HandleMessage(p *Player, msg *Message) {
    switch msg.Type {
    case MsgJoinRoom:
        var data struct {
            RoomID string `json:"room_id"`
        }
        json.Unmarshal(msg.Data, &data)
        s.joinRoom(p, data.RoomID)

    case MsgReady:
        s.playerReady(p)

    case MsgMove:
        var data MoveData
        json.Unmarshal(msg.Data, &data)
        p.mu.Lock()
        p.X = data.X
        p.Y = data.Y
        p.Dir = data.Dir
        p.mu.Unlock()

    case MsgAttack:
        var data AttackData
        json.Unmarshal(msg.Data, &data)
        s.handleAttack(p, &data)
    }
}

func (s *GameServer) joinRoom(p *Player, roomID string) {
    s.mu.Lock()
    room, exists := s.Rooms[roomID]
    if !exists {
        room = NewRoom(roomID, 4)
        s.Rooms[roomID] = room
    }
    s.mu.Unlock()

    if err := room.Join(p); err != nil {
        p.SendMsg(MsgError, map[string]string{"error": err.Error()})
        return
    }
}

func (s *GameServer) playerReady(p *Player) {
    if p.Room == nil {
        return
    }
    p.Ready = true

    room := p.Room
    room.mu.RLock()
    allReady := len(room.Players) >= 2
    for _, player := range room.Players {
        if !player.Ready {
            allReady = false
            break
        }
    }
    room.mu.RUnlock()

    if allReady {
        room.StartGame()
    }
}

func (s *GameServer) handleAttack(attacker *Player, data *AttackData) {
    if attacker.Room == nil || attacker.Dead {
        return
    }

    room := attacker.Room
    room.mu.Lock()
    defer room.mu.Unlock()

    target, ok := room.Players[data.TargetID]
    if !ok || target.Dead {
        return
    }

    damage := 20 // 简化伤害计算
    target.HP -= damage
    if target.HP <= 0 {
        target.HP = 0
        target.Dead = true
    }
}

func (s *GameServer) Disconnect(p *Player) {
    if p.Room != nil {
        p.Room.Leave(p)
    }
    s.mu.Lock()
    delete(s.Players, p.ID)
    s.mu.Unlock()
}

func main() {
    server := NewGameServer()

    http.HandleFunc("/ws", server.HandleWebSocket)

    log.Println("Game server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### 13.2 RESTful API项目（Gin + GORM + Redis）

#### 项目结构

```
myapi/
├── cmd/
│   └── api/
│       └── main.go
├── internal/
│   ├── handler/
│   │   └── user.go
│   ├── middleware/
│   │   ├── auth.go
│   │   ├── cors.go
│   │   └── logger.go
│   ├── model/
│   │   └── user.go
│   ├── repository/
│   │   └── user.go
│   ├── service/
│   │   └── user.go
│   └── pkg/
│       ├── response/
│       │   └── response.go
│       └── errcode/
│           └── errcode.go
├── configs/
│   └── config.yaml
├── go.mod
└── Makefile
```

#### 入口文件

```go
// cmd/api/main.go
package main

import (
    "context"
    "log"
    "net/http"
    "os"
    "os/signal"
    "syscall"
    "time"

    "github.com/gin-gonic/gin"
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "github.com/redis/go-redis/v9"
)

func main() {
    // 初始化数据库
    db, err := gorm.Open(mysql.Open("user:pass@tcp(localhost:3306)/mydb?charset=utf8mb4&parseTime=True"), &gorm.Config{})
    if err != nil {
        log.Fatal(err)
    }

    // 初始化Redis
    rdb := redis.NewClient(&redis.Options{Addr: "localhost:6379"})

    // 初始化路由
    r := setupRouter(db, rdb)

    // 优雅关闭
    srv := &http.Server{Addr: ":8080", Handler: r}

    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("listen: %s\n", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    srv.Shutdown(ctx)
    log.Println("Server exited")
}

func setupRouter(db *gorm.DB, rdb *redis.Client) *gin.Engine {
    r := gin.New()
    r.Use(gin.Recovery())
    r.Use(LoggerMiddleware())
    r.Use(CORSMiddleware())

    // 依赖注入
    userRepo := NewUserRepository(db)
    userSvc := NewUserService(userRepo, rdb)
    userHandler := NewUserHandler(userSvc)

    // 路由
    api := r.Group("/api/v1")
    {
        api.POST("/users", userHandler.Create)
        api.GET("/users/:id", userHandler.GetByID)
        api.PUT("/users/:id", userHandler.Update)
        api.DELETE("/users/:id", userHandler.Delete)
        api.GET("/users", userHandler.List)
    }

    return r
}
```

#### 统一响应

```go
// internal/pkg/response/response.go
package response

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

type Response struct {
    Code    int         `json:"code"`
    Message string      `json:"message"`
    Data    interface{} `json:"data,omitempty"`
}

func Success(c *gin.Context, data interface{}) {
    c.JSON(http.StatusOK, Response{Code: 0, Message: "success", Data: data})
}

func Created(c *gin.Context, data interface{}) {
    c.JSON(http.StatusCreated, Response{Code: 0, Message: "created", Data: data})
}

func Error(c *gin.Context, httpStatus int, code int, message string) {
    c.JSON(httpStatus, Response{Code: code, Message: message})
}

func BadRequest(c *gin.Context, message string) {
    Error(c, http.StatusBadRequest, 400, message)
}

func NotFound(c *gin.Context, message string) {
    Error(c, http.StatusNotFound, 404, message)
}

func InternalError(c *gin.Context) {
    Error(c, http.StatusInternalServerError, 500, "internal server error")
}
```

#### Handler层

```go
// internal/handler/user.go
package handler

import (
    "strconv"
    "github.com/gin-gonic/gin"
)

type UserHandler struct {
    svc *UserService
}

func NewUserHandler(svc *UserService) *UserHandler {
    return &UserHandler{svc: svc}
}

type CreateUserReq struct {
    Name  string `json:"name" binding:"required,min=2,max=50"`
    Email string `json:"email" binding:"required,email"`
    Age   int    `json:"age" binding:"gte=0,lte=150"`
}

func (h *UserHandler) Create(c *gin.Context) {
    var req CreateUserReq
    if err := c.ShouldBindJSON(&req); err != nil {
        BadRequest(c, err.Error())
        return
    }

    user, err := h.svc.Create(c.Request.Context(), req.Name, req.Email, req.Age)
    if err != nil {
        InternalError(c)
        return
    }
    Created(c, user)
}

func (h *UserHandler) GetByID(c *gin.Context) {
    id, err := strconv.ParseInt(c.Param("id"), 10, 64)
    if err != nil {
        BadRequest(c, "invalid id")
        return
    }

    user, err := h.svc.GetByID(c.Request.Context(), id)
    if err != nil {
        NotFound(c, "user not found")
        return
    }
    Success(c, user)
}

func (h *UserHandler) List(c *gin.Context) {
    page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
    size, _ := strconv.Atoi(c.DefaultQuery("size", "20"))

    users, total, err := h.svc.List(c.Request.Context(), page, size)
    if err != nil {
        InternalError(c)
        return
    }
    Success(c, gin.H{"items": users, "total": total, "page": page, "size": size})
}
```

#### Service层

```go
// internal/service/user.go
package service

import (
    "context"
    "encoding/json"
    "fmt"
    "time"

    "github.com/redis/go-redis/v9"
)

type UserService struct {
    repo *UserRepository
    rdb  *redis.Client
}

func NewUserService(repo *UserRepository, rdb *redis.Client) *UserService {
    return &UserService{repo: repo, rdb: rdb}
}

func (s *UserService) GetByID(ctx context.Context, id int64) (*User, error) {
    // 先查缓存
    cacheKey := fmt.Sprintf("user:%d", id)
    cached, err := s.rdb.Get(ctx, cacheKey).Result()
    if err == nil {
        var user User
        json.Unmarshal([]byte(cached), &user)
        return &user, nil
    }

    // 缓存未命中，查数据库
    user, err := s.repo.GetByID(ctx, id)
    if err != nil {
        return nil, err
    }

    // 写入缓存
    data, _ := json.Marshal(user)
    s.rdb.Set(ctx, cacheKey, data, 10*time.Minute)

    return user, nil
}

func (s *UserService) Create(ctx context.Context, name, email string, age int) (*User, error) {
    user := &User{Name: name, Email: email, Age: age}
    return s.repo.Create(ctx, user)
}

func (s *UserService) List(ctx context.Context, page, size int) ([]User, int64, error) {
    offset := (page - 1) * size
    return s.repo.List(ctx, offset, size)
}
```

#### Repository层

```go
// internal/repository/user.go
package repository

import (
    "context"
    "gorm.io/gorm"
)

type UserRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) *UserRepository {
    return &UserRepository{db: db}
}

func (r *UserRepository) Create(ctx context.Context, user *User) (*User, error) {
    err := r.db.WithContext(ctx).Create(user).Error
    return user, err
}

func (r *UserRepository) GetByID(ctx context.Context, id int64) (*User, error) {
    var user User
    err := r.db.WithContext(ctx).First(&user, id).Error
    if err != nil {
        return nil, err
    }
    return &user, nil
}

func (r *UserRepository) List(ctx context.Context, offset, limit int) ([]User, int64, error) {
    var users []User
    var total int64

    r.db.WithContext(ctx).Model(&User{}).Count(&total)
    err := r.db.WithContext(ctx).Offset(offset).Limit(limit).Find(&users).Error
    return users, total, err
}
```

---

## 第十四章：Go面试题精选（50题）

### 基础语法（10题）

#### 题1：以下代码输出什么？

```go
func main() {
    fmt.Println("start")
    defer fmt.Println("1")
    defer fmt.Println("2")
    defer fmt.Println("3")
    fmt.Println("end")
}
```

**答案**：
```
start
end
3
2
1
```

defer按LIFO（后进先出）顺序执行，且在函数返回前执行。

---

#### 题2：slice的底层结构是什么？以下代码输出什么？

```go
func main() {
    s := make([]int, 0, 5)
    s = append(s, 1, 2, 3)
    a := s[1:3]
    a = append(a, 4)
    fmt.Println(s)
    fmt.Println(a)
}
```

**答案**：
```
[1 2 3]
[2 3 4]
```

slice底层结构包含：指针（指向底层数组）、长度（len）、容量（cap）。`a := s[1:3]`创建的切片与s共享底层数组。`a = append(a, 4)`没有超过a的容量（cap=4），所以修改的是s的底层数组的第4个位置。但`fmt.Println(s)`只打印s的前3个元素（len=3），所以看不到变化。实际上底层数组已变为`[1,2,3,4,_]`。

---

#### 题3：map是否并发安全？如何实现并发安全的map？

**答案**：Go的map**不是并发安全的**。并发读写会导致`fatal error: concurrent map read and map write`。

解决方案：
1. `sync.Mutex` 或 `sync.RWMutex` 保护map
2. `sync.Map`（适用于读多写少、key稳定的场景）
3. 分片锁（sharded map）减少锁竞争

```go
// 方案1
type SafeMap struct {
    mu sync.RWMutex
    m  map[string]interface{}
}

// 方案2
var m sync.Map
m.Store("key", "value")
val, ok := m.Load("key")
```

---

#### 题4：string是可变的吗？string和[]byte的区别？

**答案**：
- `string`是**不可变的**。对string的任何修改操作都会创建新string。
- `string`底层是`struct { ptr *byte; len int }`
- `[]byte`底层是`struct { ptr *byte; len int; cap int }`
- string到[]byte的转换会发生内存复制（除非使用unsafe）
- string可以直接比较，[]byte不能用`==`比较（需要`bytes.Equal`）

---

#### 题5：make和new的区别？

**答案**：
- `new(T)`：分配零值内存，返回`*T`指针。适用于任何类型。
- `make(T, args)`：仅用于slice、map、channel，返回初始化后的`T`（非指针）。

```go
p := new(int)          // *int，指向0
s := make([]int, 5)    // []int，长度5
m := make(map[string]int) // 已初始化的map
ch := make(chan int, 10)   // 缓冲channel
```

---

#### 题6：nil slice和empty slice的区别？

```go
var s1 []int          // nil slice: s1 == nil, len=0, cap=0
s2 := []int{}         // empty slice: s2 != nil, len=0, cap=0
s3 := make([]int, 0)  // empty slice: s3 != nil, len=0, cap=0
```

**答案**：功能上几乎等价（`append`、`len`、`range`行为一致），但`json.Marshal`时nil slice编码为`null`，empty slice编码为`[]`。

---

#### 题7：Go是值传递还是引用传递？

**答案**：**Go只有值传递**。所有参数传递都是值的复制。

但slice、map、channel看起来像引用传递，因为它们内部包含指针：
- slice复制了header（指针+len+cap），指针指向同一底层数组
- map复制了指向底层哈希表的指针
- channel复制了指向底层hchan的指针

---

#### 题8：iota的用法？

```go
const (
    a = iota  // 0
    b         // 1
    c = "hi"  // "hi"（iota仍然递增到2）
    d         // "hi"（重复上一行表达式）
    e = iota  // 4
)
```

**答案**：iota是const块中的行索引计数器，从0开始，每行递增1。跳过值不影响计数。

---

#### 题9：rune和byte的区别？

**答案**：
- `byte` = `uint8`，表示一个ASCII字符或一个字节
- `rune` = `int32`，表示一个Unicode码点（可以表示中文等多字节字符）

```go
s := "你好"
fmt.Println(len(s))           // 6（字节数，UTF-8中文占3字节）
fmt.Println(len([]rune(s)))   // 2（字符数）
fmt.Println([]byte(s))        // [228 189 160 229 165 189]
fmt.Println([]rune(s))        // [20320 22909]
```

---

#### 题10：闭包陷阱——以下代码输出什么？

```go
func main() {
    fns := make([]func(), 5)
    for i := 0; i < 5; i++ {
        fns[i] = func() {
            fmt.Println(i)
        }
    }
    for _, fn := range fns {
        fn()
    }
}
```

**答案**：
- Go 1.21 及之前：输出 5 个 `5`（闭包捕获的是变量 `i` 的引用，循环结束后 `i == 5`）。
- **Go 1.22+（截至 1.25 仍是默认行为）**：输出 `0 1 2 3 4`。`for` 循环变量在每次迭代被重新声明，闭包捕获到的是各自的副本。前提是 `go.mod` 里 `go ≥ 1.22`；旧 `go.mod` 即便用新工具链编译也仍是旧语义。

Go 1.22 之前（或被迫保留旧语义时）的修复方式：
```go
for i := 0; i < 5; i++ {
    i := i  // 创建新的局部变量
    fns[i] = func() { fmt.Println(i) }
}
```

---

### 并发编程（15题）

#### 题11：Goroutine泄露的常见原因和排查方式？

**答案**：
常见原因：
1. 向无人接收的channel发送/从无人发送的channel接收
2. 忘记关闭channel导致range永远阻塞
3. select没有default且所有case都阻塞
4. 无限循环没有退出条件
5. 互斥锁死锁

排查方式：
```go
// 运行时检测
fmt.Println(runtime.NumGoroutine())

// pprof
import _ "net/http/pprof"
// 访问 /debug/pprof/goroutine?debug=1

// 使用 goleak 测试库
import "go.uber.org/goleak"
func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m)
}
```

---

#### 题12：以下代码会死锁吗？为什么？

```go
func main() {
    ch := make(chan int)
    ch <- 1
    fmt.Println(<-ch)
}
```

**答案**：会死锁。无缓冲channel的发送操作会阻塞直到有接收者。main goroutine在`ch <- 1`处永远阻塞，没有其他goroutine来接收。

修复方式：
```go
// 方案1：用有缓冲channel
ch := make(chan int, 1)

// 方案2：用goroutine发送
go func() { ch <- 1 }()
```

---

#### 题13：请简述GMP调度模型。

**答案**：
- **G（Goroutine）**：待执行的协程，包含栈和状态信息
- **M（Machine）**：操作系统线程，实际执行G的载体
- **P（Processor）**：逻辑处理器，维护本地G运行队列，默认数量等于CPU核心数（GOMAXPROCS）

调度流程：
1. P从本地队列取G绑定到M上执行
2. 本地队列为空时，从全局队列或其他P偷取G（work stealing）
3. G阻塞时（如系统调用），M与P分离，P绑定新的M继续执行其他G（hand off）
4. Go 1.14+ 支持基于信号的抢占式调度

---

#### 题14：sync.Map适用什么场景？

**答案**：
sync.Map适用于两种场景：
1. **读多写少**：key一旦写入很少修改
2. **不同goroutine操作不同的key集合**（无竞争）

不适合频繁写入或key变化大的场景（此时普通map+RWMutex性能更好）。

sync.Map内部使用read map（无锁读）+ dirty map（加锁写）的双map结构实现。

---

#### 题15：context.WithCancel、WithTimeout、WithDeadline的区别？

**答案**：
- `WithCancel`：手动取消，调用返回的cancel函数
- `WithTimeout`：超时自动取消，传入duration
- `WithDeadline`：到达deadline时间点自动取消

```go
ctx1, cancel := context.WithCancel(parent)         // 手动cancel()
ctx2, cancel := context.WithTimeout(parent, 5*time.Second)  // 5秒后自动取消
ctx3, cancel := context.WithDeadline(parent, time.Now().Add(5*time.Second)) // 等同于上面
```

WithTimeout内部就是调用WithDeadline。三者都应该defer cancel()释放资源。

---

#### 题16：WaitGroup和Channel如何选择？

**答案**：
- **WaitGroup**：等待一组goroutine全部完成，不关心返回值。简单的"等全部做完"场景。
- **Channel**：需要goroutine之间传递数据、需要流式处理结果、需要控制并发数、需要超时控制。

```go
// WaitGroup：简单等待
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    wg.Add(1)
    go func() { defer wg.Done(); work() }()
}
wg.Wait()

// Channel：需要结果
results := make(chan Result, 10)
for i := 0; i < 10; i++ {
    go func() { results <- doWork() }()
}
for i := 0; i < 10; i++ {
    r := <-results  // 收集结果
}
```

---

#### 题17：select中有default分支的行为？

**答案**：
- **没有default**：select阻塞直到某个case就绪
- **有default**：如果所有case都没就绪，立即执行default（非阻塞）

```go
// 非阻塞接收
select {
case msg := <-ch:
    handle(msg)
default:
    // ch没有数据时立即走这里
}

// 常用于"尝试发送"
select {
case ch <- data:
    // 发送成功
default:
    // channel满了，丢弃或其他处理
}
```

---

#### 题18：Mutex和Channel如何选择？

**答案**：
Go谚语："用channel来共享内存，而不是用共享内存来通信"。但不是说channel总是更好：

- **Mutex适合**：保护共享状态（计数器、缓存map）、临界区很短
- **Channel适合**：传递数据所有权、协调goroutine生命周期、实现pipeline

经验法则：如果你觉得加锁更直观清晰，就用锁。不要为了"Go风格"强行用channel。

---

#### 题19：Goroutine的栈是如何增长的？

**答案**：
- 初始栈大小：2KB（Go 1.4+，之前是8KB）
- 增长方式：连续栈（contiguous stack）
  1. 运行时检测到栈即将溢出
  2. 分配一个2倍大小的新栈
  3. 将旧栈内容复制到新栈
  4. 修改所有指向旧栈的指针
  5. 释放旧栈
- 栈可以收缩（GC时检测，使用不到1/4时收缩）

对比Java：每个线程固定1MB栈，无法动态调整。

---

#### 题20：如何检测数据竞争？

**答案**：
```bash
go run -race main.go      # 运行时检测
go test -race ./...       # 测试时检测
go build -race -o app     # 编译带竞争检测的二进制
```

-race使用ThreadSanitizer算法，会增加5-10x的内存开销和2-20x的CPU开销。建议在CI中开启。

---

#### 题21：sync.Once的底层实现原理？

**答案**：
```go
type Once struct {
    done atomic.Uint32
    m    Mutex
}

func (o *Once) Do(f func()) {
    if o.done.Load() == 0 {  // 快速路径：已完成则直接返回
        o.doSlow(f)
    }
}

func (o *Once) doSlow(f func()) {
    o.m.Lock()
    defer o.m.Unlock()
    if o.done.Load() == 0 {  // 双重检查
        defer o.done.Store(1)
        f()
    }
}
```

核心：atomic快速路径 + mutex保证只执行一次 + 双重检查避免重复执行。

---

#### 题22：Channel的底层结构？发送和接收的流程？

**答案**：
```go
type hchan struct {
    qcount   uint      // 缓冲区中元素数量
    dataqsiz uint      // 缓冲区大小（make时指定）
    buf      unsafe.Pointer // 环形缓冲区指针
    elemsize uint16    // 元素大小
    closed   uint32    // 是否已关闭
    sendx    uint      // 发送索引
    recvx    uint      // 接收索引
    recvq    waitq     // 等待接收的goroutine队列
    sendq    waitq     // 等待发送的goroutine队列
    lock     mutex     // 锁
}
```

发送流程：
1. 加锁
2. 如果recvq有等待的接收者，直接将数据拷贝给接收者（不经过缓冲区）
3. 如果缓冲区有空间，拷贝到缓冲区
4. 否则，将当前goroutine加入sendq，gopark挂起

---

#### 题23：如何优雅关闭Channel？

**答案**：原则——**由发送者关闭channel，接收者不要关闭**。

```go
// 单生产者：直接close
func producer(ch chan<- int) {
    for i := 0; i < 10; i++ {
        ch <- i
    }
    close(ch)
}

// 多生产者：使用sync.Once或额外的done channel
func multiProducer(ch chan<- int, done <-chan struct{}) {
    for {
        select {
        case <-done:
            return
        case ch <- produce():
        }
    }
}
```

---

#### 题24：实现一个Worker Pool。

```go
func WorkerPool(jobs <-chan int, numWorkers int) <-chan int {
    results := make(chan int, len(jobs))
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }

    go func() {
        wg.Wait()
        close(results)
    }()

    return results
}
```

---

#### 题25：如何实现并发安全的单例模式？

```go
// 方法1：sync.Once（推荐）
var (
    instance *Singleton
    once     sync.Once
)

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{}
    })
    return instance
}

// 方法2：init函数（如果初始化不需要延迟）
var instance = &Singleton{}
func GetInstance() *Singleton { return instance }

// 方法3：atomic + mutex（sync.Once的底层原理）
var (
    instance *Singleton
    mu       sync.Mutex
    done     uint32
)

func GetInstance() *Singleton {
    if atomic.LoadUint32(&done) == 1 {
        return instance
    }
    mu.Lock()
    defer mu.Unlock()
    if done == 0 {
        instance = &Singleton{}
        atomic.StoreUint32(&done, 1)
    }
    return instance
}
```

---

### 内存与GC（8题）

#### 题26：什么是逃逸分析？变量在什么情况下会逃逸到堆？

**答案**：逃逸分析是编译器判断变量应该分配在栈上还是堆上的过程。

逃逸场景：
1. 返回局部变量的指针
2. 发送到channel的指针
3. 闭包引用的变量
4. interface类型传参（编译器不确定大小）
5. slice/map太大或动态增长
6. 在其他goroutine中使用的变量

```bash
go build -gcflags="-m -l" main.go  # 查看逃逸分析结果
```

---

#### 题27：结构体内存对齐规则？

**答案**：
- 每个字段的偏移量必须是其大小的整数倍
- 结构体总大小必须是最大字段大小的整数倍
- 字段按声明顺序排列

优化原则：将大字段放前面，小字段放后面，相同大小的字段放一起。

```go
// 差：24字节
type Bad struct {
    a bool   // 1 + 7 padding
    b int64  // 8
    c bool   // 1 + 7 padding
}

// 好：16字节
type Good struct {
    b int64  // 8
    a bool   // 1
    c bool   // 1 + 6 padding
}
```

---

#### 题28：GC何时触发？

**答案**：
1. **堆内存增长**：当堆大小达到上次GC后存活对象大小的(1+GOGC/100)倍
2. **定时触发**：距离上次GC超过2分钟（forcegcperiod）
3. **手动触发**：`runtime.GC()`
4. **GOMEMLIMIT触发**：接近内存软上限时更频繁GC

---

#### 题29：三色标记法的三种颜色代表什么？

**答案**：
- **白色**：未被访问的对象（GC结束后被回收）
- **灰色**：已被访问但其引用的对象未全部访问
- **黑色**：已被访问且其引用的对象都已访问（确认存活）

不变性：黑色对象不能直接引用白色对象（通过写屏障保证）。

---

#### 题30：如何调优GOGC和GOMEMLIMIT？

**答案**：
```bash
# GOGC：控制GC频率与内存之间的平衡
GOGC=100  # 默认，堆增长100%时GC
GOGC=200  # 更少GC、更多内存
GOGC=50   # 更多GC、更少内存

# GOMEMLIMIT(Go 1.19+)：推荐替代GOGC
# 设置为容器内存限制的80-90%
GOMEMLIMIT=800MiB  # 容器1GB时

# 组合使用
GOGC=off GOMEMLIMIT=800MiB  # 关闭比例触发，只靠内存上限触发
```

---

#### 题31：sync.Pool的工作原理和注意事项？

**答案**：
- sync.Pool为每个P维护一个本地池+一个共享池
- Get优先从本地池获取，其次从其他P的共享池偷取
- **GC时Pool中的对象会被全部清除**
- 不适合做连接池（对象会被GC回收），适合临时对象复用（Buffer等）

```go
var pool = sync.Pool{
    New: func() any { return &Buffer{} },
}
// Get/Put必须配对使用，Put之前要Reset对象状态
```

---

#### 题32：栈内存和堆内存的区别？

| 特性 | 栈 | 堆 |
|------|-----|-----|
| 分配速度 | 极快（移动SP指针） | 较慢（需要GC管理） |
| 释放 | 自动（函数返回） | GC回收 |
| 大小 | goroutine栈2KB-1GB | 进程级，受系统限制 |
| 访问 | 只有当前goroutine | 所有goroutine共享 |

**优化目标**：尽量让变量分配在栈上（避免逃逸）。

---

#### 题33：如何排查内存泄漏？

**答案**：
```bash
# 1. pprof查看堆分配
go tool pprof http://localhost:6060/debug/pprof/heap

# 2. 对比两次heap profile
go tool pprof -base heap1.prof heap2.prof

# 3. inuse_space vs alloc_space
# inuse_space: 当前占用（找泄漏）
# alloc_space: 总分配量（找热点）

# 4. goroutine泄漏也会导致内存泄漏
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

常见原因：goroutine泄漏、全局map/slice无限增长、time.Ticker未Stop、未关闭的连接。

---

### 接口与设计（7题）

#### 题34：接口nil判断陷阱

```go
type MyError struct{ msg string }
func (e *MyError) Error() string { return e.msg }

func getError() error {
    var err *MyError = nil
    return err  // 返回的error不是nil！
}

func main() {
    err := getError()
    fmt.Println(err == nil)  // false！
}
```

**答案**：接口包含两个字段：type和value。只有当type和value都为nil时，接口才等于nil。这里`err`的type是`*MyError`（非nil），value是nil。

修复：直接返回nil，不要返回具体类型的nil指针。

---

#### 题35：空struct（struct{}）有什么用途？

**答案**：`struct{}`大小为0，不占内存。用途：
1. **Set实现**：`map[string]struct{}`比`map[string]bool`省内存
2. **Channel信号**：`chan struct{}`仅传递信号不传数据
3. **方法接收者**：不需要状态的接口实现

```go
// Set
seen := make(map[string]struct{})
seen["a"] = struct{}{}

// 信号channel
done := make(chan struct{})
close(done)  // 通知完成
```

---

#### 题36：Go的组合（embedding）和Java的继承有什么本质区别？

**答案**：
- **Java继承**：is-a关系，有多态（动态分派），子类引用可赋给父类
- **Go组合**：has-a关系，没有多态，嵌入是语法糖（编译器自动生成转发代码）

关键区别：Go的嵌入不会让外层类型满足内层类型的接口（除非方法签名匹配）。外层类型覆盖内层方法时，不是"继承+重写"，而是方法遮蔽。

---

#### 题37：接口类型断言的性能如何？

**答案**：
- 类型断言（`i.(*ConcreteType)`）：非常快，等同于指针比较（O(1)）
- 接口转接口（`i.(AnotherInterface)`）：需要查接口方法表，有一定开销但仍很快（缓存机制）
- 类型switch：和多个if-else类型断言等价

在热路径中避免频繁的接口断言，可以在入口处断言一次后使用具体类型。

---

#### 题38：什么是函数选项模式（Functional Options）？

```go
type Server struct {
    port    int
    timeout time.Duration
    maxConn int
}

type Option func(*Server)

func WithPort(port int) Option {
    return func(s *Server) { s.port = port }
}

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func WithMaxConn(n int) Option {
    return func(s *Server) { s.maxConn = n }
}

func NewServer(opts ...Option) *Server {
    s := &Server{port: 8080, timeout: 30 * time.Second, maxConn: 100}
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// 使用
srv := NewServer(
    WithPort(9090),
    WithTimeout(10*time.Second),
)
```

**优势**：可扩展、可选参数、向后兼容、自文档化。替代Java的Builder模式。

---

#### 题39：Go中如何实现依赖注入？

**答案**：
1. **构造函数注入**（最常用）：通过NewXxx函数传入依赖
2. **接口**：依赖接口而非具体实现
3. **Wire框架**：编译时代码生成，无反射开销
4. **fx框架**（Uber）：运行时反射注入

```go
// 构造函数注入
type UserService struct {
    repo UserRepository  // 接口
    cache CacheService   // 接口
}

func NewUserService(repo UserRepository, cache CacheService) *UserService {
    return &UserService{repo: repo, cache: cache}
}
```

---

#### 题40：duck typing的优缺点？

**答案**：

优点：
- 零耦合：实现方无需导入接口所在的包
- 小接口自然涌现：消费方按需定义最小接口
- 易于mock测试
- 第三方库可以满足你的接口

缺点：
- IDE支持不如Java（不能"跳转到实现"列出所有实现者）
- 意外满足接口（方法签名碰巧匹配）
- 重构时无编译期保证（删除方法不会立刻报错，除非有赋值语句）

---

### 工程实践（10题）

#### 题41：Go Modules的版本管理规则？

**答案**：
- 遵循语义化版本（Semantic Versioning）：vMAJOR.MINOR.PATCH
- v0.x.x和v1.x.x：导入路径无需版本后缀
- v2+：导入路径必须加版本后缀（`module/v2`）
- MVS（Minimal Version Selection）：选择满足约束的最小版本
- `go.sum`记录所有直接和间接依赖的hash校验值

```go
import "github.com/example/pkg/v2"  // v2版本
```

---

#### 题42：如何优雅关闭HTTP服务？

```go
func main() {
    srv := &http.Server{Addr: ":8080", Handler: router}

    go func() {
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatal(err)
        }
    }()

    // 等待中断信号
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    // 给在途请求最多5秒完成
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("forced shutdown:", err)
    }
}
```

核心：`srv.Shutdown(ctx)`会停止接受新连接，等待在途请求完成或超时。

---

#### 题43：Go中如何做单元测试的mock？

**答案**：
1. **接口mock**（推荐）：依赖接口，测试时传入mock实现
2. **gomock/mockgen**：自动生成mock代码
3. **testify/mock**：手动写mock

```go
// 接口
type UserRepo interface {
    GetByID(ctx context.Context, id int64) (*User, error)
}

// Mock实现
type mockUserRepo struct {
    users map[int64]*User
}

func (m *mockUserRepo) GetByID(ctx context.Context, id int64) (*User, error) {
    u, ok := m.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return u, nil
}

// 测试
func TestUserService_GetByID(t *testing.T) {
    repo := &mockUserRepo{users: map[int64]*User{
        1: {ID: 1, Name: "Alice"},
    }}
    svc := NewUserService(repo)
    
    user, err := svc.GetByID(context.Background(), 1)
    assert.NoError(t, err)
    assert.Equal(t, "Alice", user.Name)
}
```

---

#### 题44：pprof的常用操作？

```bash
# CPU分析（采样30秒）
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# 内存分析
go tool pprof http://localhost:6060/debug/pprof/heap

# Goroutine堆栈
go tool pprof http://localhost:6060/debug/pprof/goroutine

# Web UI可视化
go tool pprof -http=:8081 cpu.prof

# 常用命令（交互模式）
top 10         # 前10热点
list funcName  # 查看函数逐行耗时
web            # 浏览器打开调用图
```

---

#### 题45：Go的交叉编译如何工作？

**答案**：Go编译器原生支持交叉编译，设置`GOOS`和`GOARCH`即可：

```bash
# Linux AMD64
GOOS=linux GOARCH=amd64 go build -o app-linux

# Mac ARM（Apple Silicon）
GOOS=darwin GOARCH=arm64 go build -o app-mac

# Windows
GOOS=windows GOARCH=amd64 go build -o app.exe
```

限制：使用CGO时不能交叉编译（需要`CGO_ENABLED=0`或交叉编译工具链）。

---

#### 题46：CGO有哪些注意事项？

**答案**：
1. CGO调用有较大开销（~100ns vs Go调用~1ns）
2. 跨越Go/C边界时会切换到系统栈
3. 不能交叉编译（需要目标平台的C编译器）
4. C代码中的goroutine调度不可控
5. 内存管理需要特别注意（Go GC不管C分配的内存）
6. 构建更慢、部署更复杂（需要动态库或静态链接）

建议：尽量避免CGO，纯Go方案优先。如必须使用，将CGO隔离到独立的包中。

---

#### 题47：vendor目录的作用？何时使用？

**答案**：
- `go mod vendor`将所有依赖复制到项目的vendor/目录
- `go build`会优先使用vendor中的代码

使用场景：
1. CI/CD环境网络不稳定
2. 需要修改依赖源码（临时patch）
3. 审计要求所有代码可见

不推荐场景：普通开发（Go Module Cache已经够用）。

---

#### 题48：go generate的用法？

**答案**：
```go
//go:generate stringer -type=Color
//go:generate mockgen -source=interface.go -destination=mock_interface.go
//go:generate protoc --go_out=. proto/user.proto

type Color int
const (
    Red Color = iota
    Green
    Blue
)
```

```bash
go generate ./...  # 执行所有go:generate指令
```

常见用途：生成enum的String方法、生成mock、编译protobuf、生成序列化代码。

---

#### 题49：什么是构建标签（build tags）？

**答案**：
```go
//go:build linux
// +build linux  (旧语法，Go 1.17前)

package mypackage
// 此文件只在Linux上编译
```

```go
//go:build !windows

// 此文件在非Windows平台编译
```

常用场景：平台特定代码、测试/生产分离、特性开关。

```bash
go build -tags "integration" ./...  # 包含带integration标签的文件
```

---

#### 题50：如何设计一个高并发WebSocket服务？

**答案**：

关键设计点：
1. **连接管理**：使用map存储连接，加读写锁保护
2. **读写分离**：每个连接独立的readPump和writePump goroutine
3. **缓冲channel**：writePump通过channel接收待发送消息，避免竞争
4. **心跳检测**：定时Ping/Pong检测死连接
5. **优雅断开**：超时机制+context取消
6. **消息广播**：避免在锁内做I/O操作

百万连接优化：
- 使用epoll/kqueue（如eviop、gnet库）减少goroutine数量
- 对象复用（sync.Pool）
- 减少内存分配（环形缓冲区、预分配）
- 分片锁减少竞争

```go
// 核心架构
type Hub struct {
    clients    map[*Client]struct{}
    broadcast  chan []byte
    register   chan *Client
    unregister chan *Client
}

// 每个Client两个goroutine
// readPump: conn -> hub（解码消息，路由到业务逻辑）
// writePump: hub -> conn（从channel读取消息，写入连接）
```

---

## 附录：学习资源推荐

| 资源 | 说明 |
|------|------|
| [Go官方文档](https://go.dev/doc/) | 权威参考 |
| [Go by Example](https://gobyexample.com/) | 代码示例学习 |
| [Effective Go](https://go.dev/doc/effective_go) | 官方最佳实践 |
| [Go Blog](https://go.dev/blog/) | 官方博客，深度文章 |
| [Go标准库源码](https://github.com/golang/go) | 最好的Go代码示例 |
| [uber-go/guide](https://github.com/uber-go/guide) | Uber Go编程规范 |

---

> 本教程由具有丰富 Go 和 Java 经验的工程师编写，知识点更新至 **Go 1.25（2025.08）** 及 1.26 筹划中的特性，截至 2026 年 5 月。建议按章节顺序学习，每章配合实际编码练习效果更佳；阅读时注意区分「**语言级特性**」（受 `go.mod` 中 `go x.y` 控制）与「**工具链特性**」（随 `toolchain` 更新自动获得）。
