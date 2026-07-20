# Dockerfile Guide

Dockerfile 常用指令说明、完整示例与镜像构建最佳实践。

> 官方参考：<https://docs.docker.com/reference/dockerfile/>

---

## 常用指令一览

| 指令 | 作用 |
|------|------|
| `FROM` | 指定基础镜像，必须是第一条指令 |
| `USER` | 指定后续指令及容器运行时使用的用户 |
| `EXPOSE` | 声明容器监听的端口（仅声明，不自动发布） |
| `ENV` | 设置环境变量 |
| `WORKDIR` | 设置工作目录，后续相对路径以此为基准 |
| `ADD` | 拷贝文件，支持远程 URL 与自动解压 tar |
| `COPY` | 拷贝本地文件（`ADD` 的简化、推荐版本） |
| `RUN` | 构建阶段执行命令，每条生成一个镜像层 |
| `CMD` | 容器启动时的默认命令，可被 `docker run` 参数覆盖 |
| `ENTRYPOINT` | 容器启动入口，通常与 `CMD` 搭配传参 |
| `ARG` | 构建期变量，仅在 build 阶段可用 |
| `LABEL` | 为镜像添加元数据（作者、版本、仓库地址等） |
| `HEALTHCHECK` | 声明容器健康检查命令 |

> `ADD` 与 `COPY` 的取舍：需要远程下载或自动解压时用 `ADD`，其余场景一律优先 `COPY`，语义更清晰、行为更可控。

## 完整示例

```dockerfile
FROM rockylinux:9

# Run the following instructions as the root user
USER root

# Exposed ports (declaration only)
EXPOSE 20086
EXPOSE 8010
EXPOSE 80
EXPOSE 443

# Environment variables
ENV GRADLE_HOME=/opt/local/gradle-1.12
ENV PATH=${GRADLE_HOME}/bin:${PATH}
ENV TZ=Asia/Shanghai

# Switch working directory to /opt
WORKDIR /opt

# Copy remote/local files (ADD supports URLs and tar extraction)
ADD https://example.com/abc.tar.xz /opt/local/abc.tar.xz
ADD shellScripts /opt/local/shellScripts
ADD gradle-1.12 /opt/local/gradle-1.12

# Prefer COPY for plain local file copies
COPY jetty-9.4.32 ./jetty
COPY nginx-1.18.0.tar.gz ./

# Chain commands with && to reduce image layers
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' > /etc/timezone \
    && tar zxvf nginx-1.18.0.tar.gz \
    && rm -f nginx-1.18.0.tar.gz \
    && dnf -y install gcc-c++ zlib zlib-devel openssl openssl-devel pcre pcre-devel \
    && cd nginx-1.18.0 \
    && ./configure --prefix=/opt/nginx --with-http_ssl_module \
    && make && make install

# Keep the container running in the foreground so it does not exit
CMD ["/bin/sh", "-c", "/opt/nginx/sbin/nginx && tail -f /dev/null"]
```

> **基础镜像提示：** 原示例使用 `centos` 基础镜像，CentOS 官方镜像已随发行版 EOL 停止更新。示例改用 `rockylinux:9`，同类可选 `almalinux:9`、`debian:12-slim`、`ubuntu:24.04` 等长期维护镜像。RHEL 系将包管理器从 `yum` 换为 `dnf`。

## 最佳实践

- **合并 `RUN` 层**：多条命令用 `&&` 串联为一条 `RUN`，并在同层清理临时文件（如解压后 `rm` 源码包），减少镜像层数与体积。
- **善用构建缓存**：把变动最少的指令（安装依赖）放前面，变动频繁的指令（拷贝源码）放后面，最大化利用层缓存。
- **使用 `.dockerignore`**：排除 `.git`、构建产物、日志等，缩小构建上下文、加快构建并避免泄漏敏感文件。
- **`ADD` 与 `COPY` 分场景**：远程下载/解压用 `ADD`，普通拷贝用 `COPY`。
- **`ENV` 建议使用 `KEY=VALUE` 形式**：无空格等号写法在多变量场景下更明确，也符合当前推荐语法。
- **`CMD`/`ENTRYPOINT` 优先 exec 形式**（JSON 数组），可正确传递信号、避免多包一层 shell。
- **最小权限**：非必要不以 root 运行业务进程，可用 `USER` 切换到普通用户。

## 常用进阶写法

### `ENTRYPOINT` + `CMD` 组合

把固定启动程序放在 `ENTRYPOINT`，把默认参数放在 `CMD`，运行时可仅覆盖参数：

```dockerfile
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]
```

```bash
# 使用默认 CMD
docker run my-nginx:latest

# 仅覆盖 CMD 参数（ENTRYPOINT 保持不变）
docker run my-nginx:latest -g "daemon off;"
```

### `ARG` 参数化构建

```dockerfile
ARG APP_VERSION=1.0.0
FROM nginx:1.27
LABEL org.opencontainers.image.version=$APP_VERSION
```

```bash
docker build -t my-nginx:1.1.0 --build-arg APP_VERSION=1.1.0 .
```

### 多阶段构建（推荐）

把编译环境与运行环境分离，显著降低最终镜像体积与攻击面：

```dockerfile
FROM golang:1.23 AS builder
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o app ./cmd/app

FROM debian:12-slim
WORKDIR /app
COPY --from=builder /src/app /app/app
EXPOSE 8080
ENTRYPOINT ["/app/app"]
```

### `HEALTHCHECK` 健康检查

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8080/health || exit 1
```

---

## 常用构建命令

```bash
# 使用默认 Dockerfile
docker build -t myapp:latest .

# 指定 Dockerfile 与构建上下文
docker build -f Dockerfile.prod -t myapp:prod .

# 关闭缓存重建
docker build --no-cache -t myapp:latest .

# BuildKit（本地构建提速）
DOCKER_BUILDKIT=1 docker build -t myapp:latest .

# buildx 多架构构建并推送
docker buildx build --platform linux/amd64,linux/arm64 \
  -t registry.example.com/team/myapp:1.0.0 \
  --push .
```

---

> 知识截止 2026-07-20，指令语义以 Docker 官方 Dockerfile reference 为准。
