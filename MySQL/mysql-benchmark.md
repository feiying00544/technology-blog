# MySQL Benchmarking with mysqlslap and sysbench

MySQL 压力测试常用的两款工具：官方自带的 `mysqlslap` 与第三方的 `sysbench`，覆盖从快速自动压测到贴近 OLTP 真实负载的场景。

> mysqlslap 官方文档：<https://dev.mysql.com/doc/refman/8.0/en/mysqlslap.html>
> sysbench 项目地址：<https://github.com/akopytov/sysbench>

---

## 工具选型

| 维度 | mysqlslap | sysbench |
|------|-----------|----------|
| 来源 | MySQL 客户端包自带 | 独立开源项目，需单独安装 |
| 负载模型 | 自动生成 SQL 或自定义 SQL | Lua 脚本，内置 OLTP 读写模型 |
| 适用场景 | 快速验证并发/引擎表现 | 贴近生产的 OLTP 基准与横向对比 |
| 可扩展性 | 较弱 | 强（可自写 Lua 脚本） |

> 命令中出现的 `your-host` / `your_password` / `your_db` 等均为占位符，使用时替换为实际环境值。为安全起见，不要在命令行明文写入密码；可用交互式 `-p` 提示输入，或使用 `mysql_config_editor` / `--login-path`。

---

## mysqlslap

`mysqlslap` 随 MySQL Community Server 一起提供，用于模拟多客户端并发访问，输出各次迭代的耗时统计。

### 自动生成 SQL 压测

```bash
mysqlslap --host=your-host --user=root -p \
  --concurrency=1 \
  --iterations=200 \
  --auto-generate-sql \
  --auto-generate-sql-add-autoincrement \
  --auto-generate-sql-load-type=mixed \
  --engine=innodb \
  --number-of-queries=50 \
  -V
```

### 常用参数

| 参数 | 说明 |
|------|------|
| `--version, -V` | 显示版本信息并退出 |
| `--auto-generate-sql, -a` | 未提供 SQL 时自动生成测试语句 |
| `--auto-generate-sql-add-autoincrement` | 为自动生成的表添加 `AUTO_INCREMENT` 列 |
| `--auto-generate-sql-load-type=type` | 负载类型：`read`(扫描表)、`write`(插入)、`key`(读主键)、`update`(更新主键)、`mixed`(一半插入一半查询，默认) |
| `--concurrency=N, -c` | 并发客户端数量 |
| `--engine=engine_name, -e` | 建表使用的存储引擎 |
| `--host=host_name, -h` | 连接的 MySQL 主机 |
| `--port=port_num, -P` | TCP/IP 连接端口 |
| `--iterations=N, -i` | 测试运行的次数 |
| `--number-of-queries=N` | 限制每个客户端大致执行的查询数 |
| `--password[=password], -p` | 连接账户的密码（建议不带值，交互式输入） |

### 使用自建库/表/语句压测

通过 `--create` 指定建表脚本、`--query` 指定测试语句，可对真实结构进行压测：

```bash
mysqlslap --host=your-host --user=root -p \
  --concurrency=1 \
  --iterations=200 \
  --engine=innodb \
  --number-of-queries=50 \
  --create=create.sql \
  --query=test.sql
```

`create.sql` 示例（建库建表）：

```sql
DROP SCHEMA IF EXISTS `mysqlslap`;
CREATE SCHEMA `mysqlslap` DEFAULT CHARACTER SET utf8mb4;
USE mysqlslap;
SET default_storage_engine = `innodb`;
CREATE TABLE `t1` (
  id SERIAL,
  intcol1 INT,
  charcol1 VARCHAR(128)
) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;
```

`test.sql` 示例（混合插入/查询语句，每行一条）：

```sql
INSERT INTO t1 VALUES (NULL, 1804289383, 'mxvtvmC9127qJNm06sGB8R92q2j7vTiiITRDGXM9ZLzkdekbWtmXKwZ2qG1llkRw5m9DHOFilEREk3q7oce8O3BEJC0woJsm6uzFAE');
SELECT intcol1, charcol1 FROM t1 WHERE id = 1;
INSERT INTO t1 VALUES (NULL, 822890675, '97RGHZ65mNzkSrYT3zWoSbg9cNePQr1bzSk81qDgE4Oanw3rnPfGsBHSbnu1evTdFDe83ro9w4jjteQg4yoo9xHck3WNqzs54W5zEm');
SELECT intcol1, charcol1 FROM t1 WHERE id = 2;
```

> 说明：原始示例使用 `latin1` 与 `INT(32)` 写法。MySQL 8.0 起整数类型的显示宽度已废弃（`INT(32)` 等价于 `INT`），且默认字符集为 `utf8mb4`，本文已按 8.0 习惯改写。

---

## sysbench

`sysbench` 是脚本化的数据库/系统基准测试工具，OLTP 测试通过 Lua 脚本（位于 `/usr/share/sysbench/`）驱动，能较真实地模拟读写混合负载。

### 测试流程

```mermaid
flowchart LR
  A[创建测试数据库] --> B[prepare 准备表与数据]
  B --> C[run 执行读写测试]
  C --> D[采集 TPS/QPS/延迟]
  D --> E[cleanup 清理测试表]
```

### 1. 创建测试数据库

```bash
mysql -uroot -hyour-host -p \
  --execute="CREATE DATABASE sysbench_benchmark DEFAULT CHARACTER SET utf8mb4;"
```

### 2. prepare 准备测试表与数据

`--tables` 指定测试表数量，`--table_size` 指定每表行数；`prepare` 表示这是造数阶段：

```bash
sysbench --mysql-host=your-host --mysql-port=3306 \
  --mysql-user=root --mysql-password=your_password \
  /usr/share/sysbench/oltp_common.lua \
  --tables=10 --table_size=100000 \
  --mysql_storage_engine=innodb \
  --mysql-db=sysbench_benchmark \
  --threads=32 prepare
```

### 3. run 执行读写测试

用 `oltp_read_write.lua` 做读写混合测试；此外还有只读、只写、删除、批量插入等脚本，替换对应 Lua 文件即可：

```bash
sysbench --mysql-host=your-host --mysql-port=3306 \
  --mysql-user=root --mysql-password=your_password \
  /usr/share/sysbench/oltp_read_write.lua \
  --tables=10 --table_size=100000 \
  --mysql_storage_engine=innodb \
  --mysql-db=sysbench_benchmark \
  --threads=1 --events=50 run
```

### 4. cleanup 清理测试表

```bash
sysbench --mysql-host=your-host --mysql-port=3306 \
  --mysql-user=root --mysql-password=your_password \
  /usr/share/sysbench/oltp_common.lua \
  --tables=10 --threads=32 \
  --mysql-db=sysbench_benchmark cleanup
```

### 常用通用参数

以下中括号内为默认值：

| 参数 | 说明 |
|------|------|
| `--threads=N` | 指定线程数 `[1]` |
| `--events=N` | 限制最大请求数，0 表示不限制 `[0]` |
| `--time=N` | 限制最长执行时间（秒），0 表示不限制 `[10]`；与 `--events` 二选一 |
| `--rate=N` | 平均事务处理速率，0 表示不限制 `[0]` |
| `--report-interval=N` | 每隔 N 秒报告一次结果，0 表示禁用 `[0]` |
| `--config-file=FILENAME` | 从文件读取命令行选项 |
| `--db-ps-mode=STRING` | 是否使用 prepare 模式语句 `{auto, disable}` `[auto]` |

MySQL 相关参数：

| 参数 | 说明 |
|------|------|
| `--mysql-host=[LIST,...]` | MySQL server host `[localhost]` |
| `--mysql-port=[LIST,...]` | MySQL server port `[3306]` |
| `--mysql-socket=[LIST,...]` | MySQL socket |
| `--mysql-user=STRING` | MySQL user `[sbtest]` |
| `--mysql-password=STRING` | MySQL password `[]` |
| `--mysql-db=STRING` | MySQL database name `[sbtest]` |
| `--mysql-ignore-errors=[LIST,...]` | 要忽略的错误码，可为 `all` `[1213,1020,1205]` |

OLTP 脚本参数（`sysbench oltp_common.lua help` 查看）：

| 参数 | 说明 |
|------|------|
| `--auto_inc[=on\|off]` | 主键使用 `AUTO_INCREMENT` 列 `[on]` |
| `--create_secondary[=on\|off]` | 除主键外再建二级索引 `[on]` |
| `--point_selects=N` | 每事务点查 SELECT 数 `[10]` |
| `--range_selects[=on\|off]` | 启用/禁用所有范围 SELECT `[on]` |
| `--index_updates=N` | 每事务索引 UPDATE 数 `[1]` |
| `--non_index_updates=N` | 每事务非索引 UPDATE 数 `[1]` |
| `--delete_inserts=N` | 每事务 DELETE/INSERT 组合数 `[1]` |
| `--table_size=N` | 每表行数 `[10000]` |
| `--tables=N` | 表数量 `[1]` |
| `--skip_trx[=on\|off]` | 不显式开启事务，全部在 AUTOCOMMIT 下执行 `[off]` |

### 封装测试脚本

将不同负载模式（读写/只读/只写/更新）参数化，方便对多实例做横向对比：

```bash
#!/bin/bash

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -thread|--param1)         threadNum="$2"; shift; shift ;;
    -singleQueryNum|--param2) singleThreadQueryNum="$2"; shift; shift ;;
    -mode|--param3)           testMode="$2"; shift; shift ;;
    -limitMode|--param4)      limit="$2"; shift; shift ;;
    -num|--param5)            limitNum="$2"; shift; shift ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Check required arguments
if [ -z "$threadNum" ] || [ -z "$singleThreadQueryNum" ] || [ -z "$testMode" ] || [ -z "$limit" ] || [ -z "$limitNum" ]; then
  echo "Usage: $0 -thread <n1> -singleQueryNum <n2> -mode <rw|r|w|u> -limitMode <time|events> -num <n3>"
  exit 1
fi

# Map test mode to Lua script
case "$testMode" in
  "rw") testModeValue="/usr/share/sysbench/oltp_read_write.lua" ;;
  "r")  testModeValue="/usr/share/sysbench/oltp_read_only.lua" ;;
  "w")  testModeValue="/usr/share/sysbench/oltp_write_only.lua" ;;
  "u")  testModeValue="/usr/share/sysbench/oltp_update_index.lua" ;;
  *)    testModeValue="/usr/share/sysbench/oltp_read_write.lua" ;;
esac

result1=$threadNum
result2=$((singleThreadQueryNum * limitNum * result1))

# Replace with real target(s)
hostA=your-host-a
hostB=your-host-b
port=3306
user=root
psd=your_password
tableSize=1000000
tableNum=1

event="--events=$result2"
timeM="--time=$limitNum"
customDate=$(date +"%Y-%m-%d-%H-%M-%S")

case "$limit" in
  "time") limitM=$timeM ;;
  *)      limitM=$event ;;
esac

commands=(
  "sysbench --mysql-host=$hostA --mysql-port=$port --mysql-user=$user --mysql-password=$psd $testModeValue --tables=$tableNum --table_size=$tableSize --mysql_storage_engine=innodb --mysql-db=sysbench_benchmark --threads=$result1 $limitM run > log/tmp.hostA.log.$customDate"
  "sysbench --mysql-host=$hostB --mysql-port=$port --mysql-user=$user --mysql-password=$psd $testModeValue --tables=$tableNum --table_size=$tableSize --mysql_storage_engine=innodb --mysql-db=sysbench_benchmark --threads=$result1 $limitM run > log/tmp.hostB.log.$customDate"
)

for command in "${commands[@]}"; do
  echo "$command"
  eval "$command"
done
```

---

## 参考资料

- [mysqlslap — MySQL 8.0 官方文档](https://dev.mysql.com/doc/refman/8.0/en/mysqlslap.html)
- [mysqlslap Options — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysqlslap.html#mysqlslap-options)
- [akopytov/sysbench — GitHub](https://github.com/akopytov/sysbench)
- [sysbench Manual (README) — GitHub](https://github.com/akopytov/sysbench/blob/master/README.md)
- [Sysbench 使用指南 — 阿里云](https://www.alibabacloud.com/help/zh/polardb/polardb-for-xscale/sysbench-user-guide)

---

> 知识截止 2026-07-20，工具用法以 mysqlslap 官方文档与 sysbench 项目 README 为准。
