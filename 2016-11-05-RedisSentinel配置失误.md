在配置Redis Sentinel的时候，出现了一个现象：同时启动程序和redis-sentinel，能够正常连接，
但过了30秒后再启动程序连接redis-sentinel，就会报：`MasterNotFound/SlaveNotFound`的错误，
同时日志中出现以下的错误：

```bash
[16036] 02 Nov 16:24:14.048 # Sentinel runid is 5e67e92ea843190baa6b2acea31ead4796fe2e92
[16036] 02 Nov 16:33:17.585 # +sdown master mymaster 127.0.0.1 6379
```

原因：redis-sentinel会定期Ping Redis服务器，但由于我很久之前配置的时候傻逼了，在redis上配置了
密码，但忘记配置redis-sentinel访问redis的密码。但由于配置时间过去太久，找问题的时候就没想到是这个，
浪费了些时间。
