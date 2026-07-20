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

---

> 知识截止 2026-07-20，指令语义以 Docker 官方 Dockerfile reference 为准。
