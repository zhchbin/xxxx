## Supervisor日常使用

1. 添加了配置文件，如何更新？

  ```bash
  $ sudo supervisorctl reread
  $ sudo supervisorctl update
  ```

2. 重启某个服务

  ```bash
  $ sudo supervisorctl restart xxxx
  ```

3. 重启所有程序

  ```bash
  $ sudo supervisorctl reload
  ```

4. 一个配置运行多个进程

  ```
  process_name = %(program_name)s_%(process_num)02d
  numprocs = 2
  ```
