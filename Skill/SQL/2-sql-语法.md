# SQL 语法

参考：[https://www.w3school.com.cn/sql/index.asp](https://www.w3school.com.cn/sql/index.asp)

**SQL 是用于访问和处理数据库的标准的计算机语言**

- SQL 指结构化查询语言
- SQL 使我们有能力访问数据库
- SQL 是一种 ANSI 的标准计算机语言（ANSI，美国国家标准化组织）

SQL 语句如下列形式：

```sql
SELECT * FROM tbl_table;
```

- SQL 对大小写不敏感
- 分号 是分隔每条 SQL 语句的标准方法，可在对服务器的相同请求中执行一条以上的语句

## 1、DML 和 DDL 两部分

**查询和更新指令** 构成了 SQL 的 DML 部分

| 语法        | 描述                 |
| ----------- | -------------------- |
| SELECT      | 获取数据             |
| UPDATE      | 更新数据库表中的数据 |
| DELETE      | 删除数据             |
| INSERT INTO | 插入数据             |

SQL 的数据定义语言 (DDL) 部分使我们有 **能力创建或删除表格**。我们也可以定义索引（键），规定表之间的链接，以及施加表间的约束。

| 语法            | 描述                 |
| --------------- | -------------------- |
| CREATE DATABASE | 创建数据库           |
| ALTER DATABASE  | 修改数据库           |
| CREATE TABLE    | 创建表               |
| ALTER TABLE     | 变更（改变）数据库表 |
| DROP TABLE      | 删除表               |
| CREATE INDEX    | 创建索引（搜索键）   |
| DROP INDEX      | 删除索引             |

## 2、SELECT 语句

```sql
SELECT * FROM 表名称
SELECT 列名称1,列名称2,列名称3 FROM 表名称
```

## 3、SELECT DISTINCT 语句

在表中可能会包含重复值，关键词 DISTINCT 用于返回唯一不同的值。

```sql
SELECT DISTINCT 列名称 FROM 表名称
```

## 4、WHERE 子句

将 WHERE 子句添加到 SELECT 语句后，按条件的从表中选取数据

```sql
SELECT 列名称 FROM 表名称 WHERE 列 运算符 值

SELECT * FROM Persons WHERE FirstName='Bush'
SELECT * FROM Persons WHERE Year>1965
```



| 运算符                 | 描述           |
| :--------------------- | :------------- |
| =                      | 等于           |
| <> 或 !=               | 不等于         |
| >                      | 大于           |
| <                      | 小于           |
| >=                     | 大于等于       |
| <=                     | 小于等于       |
| BETWEEN                | 在某个范围内   |
| LIKE                   | 搜索某种模式   |
| IN (value1,value2,...) | 在指定集合中搜 |
