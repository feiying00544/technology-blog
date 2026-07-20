# MySQL Common Commands and Administration

MySQL 8.0 日常使用与运维命令速查：服务与连接、库表 DDL、数据 DML、用户与权限、备份恢复、字符集、容量查询、批量建表与常见排错。

> 命令中的 `your-host` / `your_password` / `your_db` / `your_table` / `app_user` 等均为占位符，使用时替换为实际值。
> 官方文档：<https://dev.mysql.com/doc/refman/8.0/en/>

---

## 服务与连接

```bash
# Windows 服务启停
net start mysql
net stop mysql

# Linux (systemd)
systemctl start mysqld
systemctl stop mysqld

# 连接（-p 后不写密码，回车后交互式输入更安全）
mysql -uroot -p your_db
mysql -uroot -hyour-host -P3306 -p
```

进入命令行后查看运行环境信息：

```sql
status;   -- 或 \s
```

> 不要在命令行明文写密码（如 `-pyour_password`），会残留在 shell 历史与进程列表中。推荐交互式输入，或用 `mysql_config_editor set --login-path=... ` 保存后 `mysql --login-path=...`。

---

## 库操作

```sql
CREATE DATABASE db_name DEFAULT CHARACTER SET utf8mb4;
DROP DATABASE IF EXISTS db_name;
SHOW DATABASES;
USE db_name;
```

---

## 表操作（DDL）

```sql
-- 建表
CREATE TABLE mytable (
  id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(20) NOT NULL
);

-- 查看建表语句 / 表结构
SHOW CREATE TABLE mytable;
DESC mytable;                 -- 等价 DESCRIBE mytable;
SHOW COLUMNS FROM mytable;
SHOW INDEX FROM mytable;

-- 删除表
DROP TABLE IF EXISTS mytable;
```

修改表结构：

```sql
ALTER TABLE mytable ADD COLUMN age INT;                 -- 增加字段
ALTER TABLE mytable ADD COLUMN age INT AFTER username;  -- 指定位置
ALTER TABLE mytable DROP COLUMN age;                    -- 删除字段
ALTER TABLE mytable CHANGE old_name new_name VARCHAR(50);  -- 改名+改类型
ALTER TABLE mytable MODIFY username VARCHAR(50);        -- 仅改类型
ALTER TABLE mytable RENAME TO new_table;               -- 改表名
TRUNCATE TABLE mytable;                                -- 清空数据并重置自增
ALTER TABLE mytable ENGINE=InnoDB;                     -- 修改存储引擎
```

> 整数类型的显示宽度（如 `INT(11)`）自 MySQL 8.0.17 起已废弃，`INT(11)` 与 `INT` 等价，新表无需再写宽度。

---

## 数据操作（DML）

```sql
-- 插入（可一次插入多行）
INSERT INTO users (id, name) VALUES (1, 'alice'), (2, 'bob');

-- 更新
UPDATE users SET name = 'carol' WHERE id = 1;

-- 删除
DELETE FROM users WHERE id = 3;

-- 查询与排序
SELECT * FROM users ORDER BY id DESC;                  -- desc 倒序，asc 正序
SELECT data, uid FROM users WHERE uid IN (123, 234);   -- 多值匹配
```

多表关联查询示例：

```sql
-- articles.userid 关联 users.id
SELECT a.id, a.content, u.*
FROM users u
JOIN articles a ON a.userid = u.id
WHERE u.id = 10
ORDER BY a.id DESC;
```

> 外键约束仅 InnoDB 支持；MySQL 各引擎均不支持 `CHECK` 约束的说法已过时——MySQL 8.0.16 起 `CHECK` 约束已被真正实现并强制生效。

---

## 用户与权限

MySQL 8.0 起，**`GRANT` 不再自动创建用户**（旧的 `GRANT ... IDENTIFIED BY` 语法与 `NO_AUTO_CREATE_USER` 模式均已移除），必须先 `CREATE USER` 再 `GRANT`。

```sql
-- 1. 创建用户（默认认证插件为 caching_sha2_password）
CREATE USER 'app_user'@'10.0.0.%' IDENTIFIED BY 'your_password';

-- 2. 授权
GRANT SELECT, INSERT, UPDATE, DELETE ON your_db.* TO 'app_user'@'10.0.0.%';

-- 只读账户示例
CREATE USER 'readonly_user'@'%' IDENTIFIED BY 'your_password';
GRANT SELECT ON *.* TO 'readonly_user'@'%';

-- 3. 刷新权限
FLUSH PRIVILEGES;
```

查看与撤销：

```sql
SHOW GRANTS FOR 'app_user'@'10.0.0.%';
SELECT user, host FROM mysql.user;           -- 查看所有用户
REVOKE INSERT ON your_db.* FROM 'app_user'@'10.0.0.%';
DROP USER 'app_user'@'10.0.0.%';             -- 删除用户（不要直接 DELETE FROM mysql.user）
```

修改 / 重置密码（MySQL 8.0）：

```sql
-- 修改指定用户密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';

-- 置空密码
ALTER USER 'root'@'localhost' IDENTIFIED BY '';
```

> - MySQL 8.0 已**移除 `PASSWORD()` 函数**，旧写法 `SET PASSWORD ... = PASSWORD('...')` 不再可用；直接用 `ALTER USER ... IDENTIFIED BY '...'`。
> - 默认认证插件是 `caching_sha2_password`。若旧客户端只支持 `mysql_native_password`，可显式指定 `IDENTIFIED WITH mysql_native_password BY '...'`；但该插件已在 8.0.34 标记为**废弃**，8.4 起默认不再加载，新系统应尽量迁移到 `caching_sha2_password`。

---

## 备份与恢复（mysqldump）

```bash
# 备份单库（结构+数据）
mysqldump -uroot -p your_db > your_db.sql

# 备份多库
mysqldump -uroot -p --databases db1 db2 > multi.sql

# 备份全部库
mysqldump -uroot -p -A > all.sql

# 仅导出建表结构（不含数据）
mysqldump -uroot -p --no-data --databases your_db > schema.sql

# 按条件导出单表
mysqldump -uroot -p your_db your_table --where="update_time >= '2024-01-01'" > part.sql
```

恢复：

```bash
# 系统命令行
mysql -uroot -p your_db < your_db.sql      # 恢复到指定库
mysql -uroot -p < all.sql                  # 备份含多库时无需指定库
```

```sql
-- MySQL 命令行内恢复
USE your_db;
SOURCE /path/to/your_db.sql;
```

---

## 字符集与乱码

MySQL 8.0 默认字符集为 **`utf8mb4`**（默认排序规则 `utf8mb4_0900_ai_ci`），应统一使用 `utf8mb4` 以完整支持中文、emoji 等 4 字节字符。

```sql
-- 查看字符集相关变量
SHOW VARIABLES LIKE '%char%';
SHOW VARIABLES LIKE 'character_set_server';

-- 查看/修改库、表字符集
SELECT default_character_set_name FROM information_schema.SCHEMATA WHERE schema_name = 'your_db';
ALTER DATABASE your_db CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
ALTER TABLE your_table CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

> 排查乱码从 server / client / database / connection / results 各层字符集是否一致入手；连接层可用 `SET NAMES utf8mb4;` 统一。注意：`utf8` 在 MySQL 中是 `utf8mb3` 的别名（仅 3 字节，已废弃），务必使用 `utf8mb4`。

---

## 查看系统信息

```sql
SELECT VERSION();                         -- 版本号
SHOW VARIABLES;                           -- 系统变量
SHOW VARIABLES LIKE 'max_connections';    -- 某个变量
SHOW STATUS;                              -- 运行状态
SHOW STATUS LIKE 'Threads%';              -- 线程/连接状态
SHOW PROCESSLIST;                         -- 当前会话/查询
SHOW ENGINES;                             -- 可用存储引擎及默认引擎
SHOW VARIABLES LIKE '%log%';              -- 日志相关（含 binlog 格式）
SHOW VARIABLES LIKE '%time_zone%';        -- 时区
```

连接数管理：

```sql
SHOW VARIABLES LIKE 'max_connections';        -- 最大连接数
SHOW STATUS LIKE 'Max_used_connections';      -- 历史最大已用连接数
SHOW STATUS LIKE 'Threads_connected';         -- 当前连接数
SET GLOBAL max_connections = 300;             -- 运行时调整（重启失效，需写配置文件持久化）
```

> `SHOW ENGINES`（原笔记误写为 `show engies`）、`SHOW WARNINGS`、`SHOW PRIVILEGES` 等仍可用；而 `SHOW INNODB STATUS` 旧写法已由 `SHOW ENGINE INNODB STATUS` 取代，`SHOW LOGS`（BDB 引擎）已随 BDB 移除而失效。

---

## 查看容量大小

通过 `information_schema.TABLES` 统计库/表的数据与索引大小：

```sql
-- 查看某库总大小
SELECT CONCAT(ROUND(SUM(DATA_LENGTH) / 1024 / 1024, 2), 'MB') AS data_size
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'your_db';

-- 查看某表数据与索引大小
SELECT
  CONCAT(ROUND(SUM(DATA_LENGTH) / 1024 / 1024, 2), 'MB')  AS data_size,
  CONCAT(ROUND(SUM(INDEX_LENGTH) / 1024 / 1024, 2), 'MB') AS index_size,
  CONCAT(ROUND(SUM(DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2), 'MB') AS total_size
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'your_db' AND TABLE_NAME = 'your_table';
```

按内容长度统计某列大小（二进制 / 文本）：

```sql
-- 二进制字节数
SELECT LENGTH(data) AS binary_size FROM your_table WHERE id = 1;
-- 字符数
SELECT CHAR_LENGTH(data) AS character_count FROM your_table WHERE id = 1;
-- 整列合计（MB）
SELECT CONCAT(ROUND(SUM(LENGTH(data)) / 1024 / 1024, 2), 'M') AS column_size FROM your_table;
```

查看/修改自增值：

```sql
SELECT AUTO_INCREMENT FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'your_db' AND TABLE_NAME = 'your_table';

ALTER TABLE your_table AUTO_INCREMENT = 10000000;
```

查看某表字段结构：

```sql
SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = 'your_db' AND TABLE_NAME = 'your_table'
ORDER BY ORDINAL_POSITION;
```

---

## 常用统计查询

```sql
-- 平均每个 uid 下的 id 行数
SELECT AVG(cnt) AS avg_rows_per_uid
FROM (SELECT uid, COUNT(id) AS cnt FROM your_table GROUP BY uid) AS t;

-- 去重统计
SELECT COUNT(DISTINCT uid) AS distinct_uid_count FROM your_table;

-- 某主键分组下的最小/最大行数
SELECT MIN(cnt) AS min_cnt, MAX(cnt) AS max_cnt
FROM (SELECT uid, COUNT(id) AS cnt FROM your_table GROUP BY uid) AS t;
```

---

## 存储过程批量建表

需要批量创建结构相同的分表时，可用存储过程循环生成：

```sql
DROP PROCEDURE IF EXISTS `create_tables`;
DELIMITER $$
CREATE PROCEDURE create_tables()
BEGIN
  DECLARE i INT DEFAULT 0;
  DECLARE createSql VARCHAR(2560);
  WHILE i < 50 DO
    SET createSql = CONCAT(
      'CREATE TABLE IF NOT EXISTS your_table_', i, ' (',
      '`uid` BIGINT UNSIGNED NOT NULL,',
      '`union_key` INT NOT NULL,',
      '`value` BLOB NOT NULL,',
      '`version` MEDIUMINT UNSIGNED NOT NULL,',
      'PRIMARY KEY (`uid`, `union_key`)',
      ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'
    );
    SET @sql = createSql;
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    SET i = i + 1;
  END WHILE;
END $$
DELIMITER ;

-- 执行
CALL `create_tables`();

-- 用完删除
DROP PROCEDURE IF EXISTS `create_tables`;
```

---

## 从 MySQL 5.x 升级到 8.0 的常见排错

### sql_mode 变更

```sql
SHOW GLOBAL VARIABLES LIKE 'sql_mode';
```

- **`NO_AUTO_CREATE_USER` 已在 8.0 移除**：任何脚本里显式设置含该值的 `sql_mode` 都会报错，需删除它。
- MySQL 8.0 默认 `sql_mode` 为：
  `ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION`

### 日期默认值 `0000-00-00` 报错

严格模式（`NO_ZERO_DATE` / `NO_ZERO_IN_DATE`）下，把日期/时间列默认值设为 `'0000-00-00'` 会报 `Invalid default value` 错误。推荐做法：改用 `NULL` 或 `CURRENT_TIMESTAMP` 等合法默认值，而不是去关闭严格模式。

### 索引前缀 767 字节限制（已过时，无需处理）

MySQL 5.6 曾出现 `Specified key was too long; max key length is 767 bytes`，需开启 `innodb_large_prefix` 并设 `ROW_FORMAT=DYNAMIC`。

> **MySQL 8.0 中这些已无需处理**：`innodb_large_prefix`、`innodb_file_format`、`innodb_file_format_max` 等变量已被**移除**；InnoDB 默认行格式即 `DYNAMIC`，索引键前缀上限为 3072 字节。旧文档中开启这些开关的步骤在 8.0 上会因“未知变量”而失败，直接忽略即可。

---

## 参考资料

- [CREATE USER — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/create-user.html)
- [GRANT — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/grant.html)
- [ALTER USER / SET PASSWORD — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/alter-user.html)
- [Caching SHA-2 Pluggable Authentication — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/caching-sha2-pluggable-authentication.html)
- [Server SQL Modes — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html)
- [Character Sets and Collations (utf8mb4) — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/charset.html)
- [The utf8mb3 Character Set (Deprecated Alias of utf8) — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf8mb3.html)
- [mysqldump — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html)
- [CHECK Constraints — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html)
- [Features Removed in MySQL 8.0 (What Is New)](https://dev.mysql.com/doc/refman/8.0/en/mysql-nutshell.html#mysql-nutshell-removals)
- [Upgrading from MySQL 5.7 to 8.0](https://dev.mysql.com/doc/refman/8.0/en/upgrading-from-previous-series.html)

---

> 知识截止 2026-07-20，命令与行为以 MySQL 8.0 官方文档为准。
