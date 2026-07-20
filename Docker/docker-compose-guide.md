# Docker Compose Guide

Docker Compose V2 的安装方式与常用命令说明。

> 官方文档：<https://docs.docker.com/compose/>
> 版本列表：<https://github.com/docker/compose/releases>

---

## 版本说明

Docker Compose 已从 V1 演进到 **V2**：

| 版本 | 形态 | 调用方式 | 状态 |
|------|------|----------|------|
| V1 | 独立 Python 二进制 `docker-compose` | `docker-compose ...` | 已 EOL，停止维护 |
| V2 | Go 编写的 Docker CLI 插件 | `docker compose ...`（无连字符） | 当前版本，官方推荐 |

> 若通过 [Docker 安装文档](docker-installation-and-commands.md) 安装时已包含 `docker-compose-plugin`，则 Compose V2 已就绪，无需再单独安装，直接 `docker compose version` 验证即可。

## 安装 Compose V2 插件

### 方式一：包管理器（推荐）

随 Docker Engine 一起安装：

```bash
# RHEL 系
yum install -y docker-compose-plugin

# Ubuntu
apt-get install -y docker-compose-plugin
```

### 方式二：手动安装为 CLI 插件

适用于无法用包管理器的环境。将二进制放入 Docker CLI 插件目录：

```bash
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
  -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

> 上例使用 `latest` 获取最新版本；如需固定版本，将 `latest/download` 替换为 `download/v2.x.y`。安装到 `$HOME/.docker/cli-plugins` 仅对当前用户生效；如需全局生效，可放到 `/usr/local/lib/docker/cli-plugins`。

### 验证

```bash
docker compose version
```

### 卸载

```bash
# 包管理器安装的
yum remove docker-compose-plugin      # 或 apt-get remove docker-compose-plugin
# 手动安装的
rm $DOCKER_CONFIG/cli-plugins/docker-compose
```

---

## 常用命令

### 启动服务

```bash
docker compose up          # 前台启动所有服务
docker compose up -d       # 后台启动所有服务
```

`up` 常用选项：

| 选项 | 说明 |
|------|------|
| `-d` | 后台运行服务容器 |
| `--no-deps` | 不启动所链接的依赖服务 |
| `--force-recreate` | 强制重建容器（与 `--no-recreate` 互斥） |
| `--no-recreate` | 容器已存在则不重建（与 `--force-recreate` 互斥） |
| `--no-build` | 不自动构建缺失的镜像 |
| `--build` | 启动前先构建镜像 |
| `--abort-on-container-exit` | 任一容器停止则停止全部（不可与 `-d` 同用） |
| `-t, --timeout TIMEOUT` | 停止容器的超时时间（默认 10s） |
| `--remove-orphans` | 删除 compose 文件中未定义的孤儿容器 |
| `--scale SERVICE=NUM` | 设置服务的容器副本数，覆盖文件中的配置 |

### 指定文件与项目名

`-f` 指定 compose 文件（默认 `docker-compose.yml`，可多次指定）；`-p` 指定项目名（默认取当前目录名）：

```bash
docker compose -f docker-compose.yml -p server up -d
```

### 其他常用命令

```bash
docker compose ps          # 查看服务状态
docker compose logs -f     # 跟踪日志
docker compose logs -f --tail=200 <service>  # 仅看某服务最近日志
docker compose stop        # 停止服务（不删除容器）
docker compose start       # 启动已存在但停止的服务容器
docker compose restart     # 重启服务
docker compose down        # 停止并删除容器、网络
docker compose down -v     # 同时删除数据卷（谨慎）
docker compose pull        # 拉取镜像
docker compose build       # 构建镜像
docker compose images      # 查看 compose 管理的镜像
docker compose rm -f       # 删除已停止的服务容器
docker compose exec <service> sh   # 进入运行中的服务容器
docker compose run --rm <service> sh  # 临时运行一次性命令并自动删除容器
docker compose config      # 渲染并校验最终配置（含变量替换）
docker compose events      # 查看实时事件流
```

> **注意：** V2 中所有命令均为 `docker compose`（空格）。旧文档中的 `docker-compose`（连字符）仅在保留了 V1 二进制或安装了兼容 wrapper 时可用；新环境请统一使用 V2 写法。

---

## 进阶用法

### 使用 Profiles 按环境启停服务

`profile` 可把调试/可选组件从默认启动集合中分离：

```yaml
services:
  app:
    image: myapp:latest
  phpmyadmin:
    image: phpmyadmin:latest
    profiles: ["debug"]
```

```bash
# 默认只启动无 profile 的服务（这里是 app）
docker compose up -d

# 显式启用 debug profile
docker compose --profile debug up -d
```

### 多 Compose 文件合并

常见做法是 `base + override`：

```bash
docker compose -f compose.yaml -f compose.prod.yaml config
docker compose -f compose.yaml -f compose.prod.yaml up -d
```

后面的文件会覆盖前面的同名字段，适合按环境切换镜像 tag、资源限制、端口等差异配置。

---

## compose 文件版本提示

Compose Specification 已不再要求顶层 `version:` 字段（V2 会忽略该字段并可能给出告警）。新编写的 `compose.yaml` / `docker-compose.yml` 可直接以 `services:` 开头，无需 `version: '3'` 之类声明。

---

> 知识截止 2026-07-20，安装方式与命令以 Docker Compose 官方文档为准。
