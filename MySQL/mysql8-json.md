# MySQL 8 JSON Usage

MySQL 8.0 的原生 `JSON` 数据类型用法：存储字符集、部分更新（partial update）机制、常用 JSON 函数与多值索引。

> JSON 官方文档：<https://dev.mysql.com/doc/refman/8.0/en/json.html>
> JSON 部分更新：<https://dev.mysql.com/doc/refman/8.0/en/json.html#json-partial-updates>

---

## JSON 与字符集

MySQL 在 JSON 上下文中统一使用 **`utf8mb4` 字符集、`utf8mb4_bin` 排序规则**处理字符串。其他字符集的字符串会按需转换为 `utf8mb4`；由于 `ascii` 和 `utf8mb3` 是 `utf8mb4` 的子集，这两者无需转换。

`JSON` 类型相比在 `VARCHAR`/`TEXT` 里存 JSON 文本的优势：

- 写入时自动校验 JSON 合法性，非法值直接报错。
- 以优化的二进制格式存储，读取时无需重新解析文本，访问子元素更快。

---

## JSON 部分更新（Partial Update）

默认情况下，更新 JSON 列会重写整个列值。满足特定条件时，InnoDB 可只对变更部分做**原地部分更新**，减少写放大与 binlog 体积。

必须同时满足以下条件才会触发部分更新：

- 列必须声明为 `JSON` 类型。
- 只能使用 `JSON_SET()`、`JSON_REPLACE()` 或 `JSON_REMOVE()` 三个函数进行更新。
- 新值长度必须**小于等于**原值长度；若前置操作已释放出空间，也可利用该空间（用 `JSON_STORAGE_FREE()` 查看已释放空间）。
- 只能替换已存在的 array/object 元素，**不能向 array/object 中新增元素**。

建表示例：

```sql
CREATE TABLE `user_data` (
  `uid` BIGINT UNSIGNED NOT NULL,
  `data` JSON,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

若希望 binlog 也以“部分更新”形式记录 JSON 变更（进一步减小 binlog），需设置：

```sql
SET binlog_row_value_options = PARTIAL_JSON;
SET binlog_row_image = MINIMAL;
```

> 相关辅助函数：`JSON_STORAGE_SIZE()` 查看 JSON 列当前占用的存储字节数，`JSON_STORAGE_FREE()` 查看部分更新后释放出的空间。JSON 列大小仍受 `max_allowed_packet` 限制。

---

## 常用 JSON 函数

| 分类 | 函数 | 说明 |
|------|------|------|
| 创建 | `JSON_OBJECT(k, v, ...)` | 构造 JSON 对象 |
| 创建 | `JSON_ARRAY(v, ...)` | 构造 JSON 数组 |
| 查询 | `JSON_EXTRACT(doc, path)` / `->` | 按路径取值；`col->'$.a'` 是简写 |
| 查询 | `col->>'$.a'` | 取值并去掉外层引号（`JSON_UNQUOTE(JSON_EXTRACT(...))`） |
| 查询 | `JSON_CONTAINS(doc, val[, path])` | 是否包含指定值 |
| 查询 | `JSON_CONTAINS_PATH(doc, 'one'\|'all', path...)` | 是否存在指定路径 |
| 查询 | `JSON_KEYS(doc[, path])` | 返回对象的键数组 |
| 查询 | `JSON_LENGTH(doc[, path])` | 元素个数 |
| 修改 | `JSON_SET(doc, path, val, ...)` | 存在则更新、不存在则插入 |
| 修改 | `JSON_INSERT(doc, path, val, ...)` | 仅在路径不存在时插入 |
| 修改 | `JSON_REPLACE(doc, path, val, ...)` | 仅在路径存在时替换 |
| 修改 | `JSON_REMOVE(doc, path, ...)` | 删除指定路径元素 |
| 修改 | `JSON_MERGE_PATCH(a, b)` | 按 RFC 7396 合并（同名键覆盖） |
| 修改 | `JSON_MERGE_PRESERVE(a, b)` | 合并并保留同名键（合并为数组） |
| 校验 | `JSON_VALID(str)` | 是否为合法 JSON |
| 校验 | `JSON_TYPE(val)` | 返回 JSON 值类型 |
| 表化 | `JSON_TABLE(doc, path COLUMNS(...))` | 将 JSON 展开为关系表参与 SQL 查询 |

示例：

```sql
-- 读取嵌套字段
SELECT data->>'$.profile.name' AS name FROM user_data WHERE uid = 1;

-- 更新已存在的字段（可触发部分更新）
UPDATE user_data SET data = JSON_SET(data, '$.level', 30) WHERE uid = 1;

-- 条件查询：data.tags 数组是否包含 "vip"
SELECT uid FROM user_data WHERE JSON_CONTAINS(data->'$.tags', '"vip"');
```

---

## 多值索引（Multi-Valued Index）

MySQL 8.0.17 起支持在 JSON 数组上创建**多值索引**：一条记录的数组中每个元素都可对应一个索引项，适合加速 `MEMBER OF()`、`JSON_CONTAINS()`、`JSON_OVERLAPS()` 等数组成员查询。

```sql
CREATE TABLE customers (
  id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
  custinfo JSON,
  -- CAST(... AS UNSIGNED ARRAY) 声明为多值索引
  INDEX idx_zips ((CAST(custinfo->'$.zipcode' AS UNSIGNED ARRAY)))
) ENGINE=InnoDB;

-- 可利用多值索引的查询
SELECT * FROM customers WHERE 94507 MEMBER OF (custinfo->'$.zipcode');
SELECT * FROM customers WHERE JSON_CONTAINS(custinfo->'$.zipcode', CAST('[94507,94582]' AS JSON));
```

> 多值索引只能用于以上数组成员类查询，不能用于范围扫描或排序。

---

## 参考资料

- [JSON Data Type — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/json.html)
- [Partial Updates of JSON Values — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-partial-updates)
- [JSON Functions — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/json-functions.html)
- [Functions That Modify JSON Values — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/json-modification-functions.html)
- [Multi-Valued Indexes — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/create-index.html#create-index-multi-valued)
- [binlog_row_value_options (PARTIAL_JSON) — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_row_value_options)
- [The utf8mb4 Character Set — MySQL 8.0](https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-utf8mb4.html)

---

> 知识截止 2026-07-20，内容以 MySQL 8.0 官方文档为准。
