# JDK Multi-Version Switch on Windows

Windows 上同时安装并快速切换多个 JDK 版本（以 JDK 11 + JDK 25 为例）。

---

## 背景

日常开发中经常需要在不同 JDK 版本间切换：老项目维护用 LTS 版本（如 JDK 11），新项目或新特性探索用最新版本（如 JDK 25）。本文介绍一种**无额外工具依赖**的轻量方案——通过批处理脚本在当前终端窗口快速切换。

## 方案概览

| 方案 | 优点 | 缺点 |
|------|------|------|
| 批处理脚本切换（本文） | 简单透明、零依赖 | 仅当前终端生效 |
| jabba | 跨平台 JDK 版本管理器 | 需额外安装，Windows 支持一般 |
| IDE 内置配置 | 项目级隔离，互不影响 | 仅对 IDE 内构建有效 |

## 第一步：安装多个 JDK

以 Azul Zulu 发行版为例（也可选 Eclipse Temurin、Oracle OpenJDK）：

1. 前往 [Azul Downloads](https://www.azul.com/downloads/#zulu)
2. 分别下载 JDK 11 和 JDK 25 的 Windows x86 64-bit `.msi` 安装包
3. 安装时使用默认路径，安装完成后目录结构如下：

```
C:\Program Files\Zulu\
├── zulu-11\
└── zulu-25\
```

> **重要：** 安装第二个 JDK 时，**取消勾选 "Set JAVA_HOME variable"**。否则安装程序会覆盖系统 `JAVA_HOME`，破坏已有版本的默认配置。

## 第二步：创建切换脚本

在 `C:\scripts\` 目录下创建两个批处理文件：

**jdk11.cmd**

```cmd
@echo off
set "JAVA_HOME=C:\Program Files\Zulu\zulu-11"
set "PATH=%JAVA_HOME%\bin;%PATH%"
echo Switched to JDK 11
java -version
```

**jdk25.cmd**

```cmd
@echo off
set "JAVA_HOME=C:\Program Files\Zulu\zulu-25"
set "PATH=%JAVA_HOME%\bin;%PATH%"
echo Switched to JDK 25
java -version
```

> 脚本通过修改当前终端的 `JAVA_HOME` 和 `PATH` 环境变量实现切换，**不影响其他已打开的终端窗口**。

## 第三步：将脚本目录加入系统 PATH

1. 右键「此电脑」→ 属性 → 高级系统设置 → 环境变量
2. 在「系统变量」中找到 `Path`，点击编辑
3. 新增一行：`C:\scripts\`
4. 确定保存，**重新打开终端**使设置生效

## 第四步：设置全局默认版本

系统环境变量中的 `JAVA_HOME` 决定默认 JDK 版本。根据日常使用频率设置：

- 大多数项目用 JDK 11 → 保持 `JAVA_HOME=C:\Program Files\Zulu\zulu-11`
- 需要 JDK 25 时在终端执行 `jdk25` 临时切换

## 使用方式

打开任意终端窗口：

```cmd
C:\> jdk11
Switched to JDK 11
openjdk version "11.0.28" 2025-07-15 LTS
...

C:\> jdk25
Switched to JDK 25
openjdk version "25" 2025-09-16
...
```

## IDE 配置（补充）

即使不切换全局 `JAVA_HOME`，也可以在 IDE 中为不同项目配置不同 JDK：

**IntelliJ IDEA：**

1. File → Project Structure → SDKs → 点击 `+` 添加两个 JDK 路径
2. 每个项目的 Project SDK 选择对应版本
3. Gradle/Maven 的构建 JDK 可在 Settings → Build, Execution, Deployment → Build Tools 中单独指定

**VS Code（Java Extension Pack）：**

在 `settings.json` 中配置：

```json
{
  "java.configuration.runtimes": [
    {
      "name": "JavaSE-11",
      "path": "C:\\Program Files\\Zulu\\zulu-11",
      "default": true
    },
    {
      "name": "JavaSE-25",
      "path": "C:\\Program Files\\Zulu\\zulu-25"
    }
  ]
}
```

## 扩展：添加更多版本

如需管理 3 个以上版本，按相同模式添加脚本即可：

```cmd
@echo off
set "JAVA_HOME=C:\Program Files\Zulu\zulu-17"
set "PATH=%JAVA_HOME%\bin;%PATH%"
echo Switched to JDK 17
java -version
```

保存为 `C:\scripts\jdk17.cmd`，无需其他配置即可使用。
