## Flask MongoDB数据库连接

在使用Flask进行MongoDB数据库的操作的时候，总觉得没有写检查数据库连接是否存在，如果连接不上，则尝试重连的操作，但线上的服务总能保持住连接，一直没细看。

今天尝试了一下，如果支持关闭MongoDB的服务，会出现什么情况？

```bash
$ sudo lsof -i:27017
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
uwsgi   2929 www-data   13u  IPv4  19497      0t0  TCP flask-app.dev.env:35686->flask-app.dev.env:27017 (ESTABLISHED)
uwsgi   2938 www-data    6u  IPv4  20577      0t0  TCP flask-app.dev.env:35689->flask-app.dev.env:27017 (ESTABLISHED)
uwsgi   2939 www-data    6u  IPv4  20419      0t0  TCP flask-app.dev.env:35688->flask-app.dev.env:27017 (ESTABLISHED)
mongod  3328  mongodb    9u  IPv4  19377      0t0  TCP flask-app.dev.env:27017 (LISTEN)
mongod  3328  mongodb   12u  IPv4  19498      0t0  TCP flask-app.dev.env:27017->flask-app.dev.env:35686 (ESTABLISHED)
mongod  3328  mongodb   13u  IPv4  20420      0t0  TCP flask-app.dev.env:27017->flask-app.dev.env:35688 (ESTABLISHED)
mongod  3328  mongodb   16u  IPv4  20578      0t0  TCP flask-app.dev.env:27017->flask-app.dev.env:35689 (ESTABLISHED)
```

目前每个uwsgi进程都连接着MongodDB的服务器。停止MongoDB服务，发现Socket连接进入了`CLOSE_WAIT`的状态。此时Web服务器出现了500。

```bash
$ sudo service mongodb stop 
mongodb stop/waiting
$ sudo lsof -i:27017
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
uwsgi   2938 www-data    6u  IPv4  20577      0t0  TCP flask-app.dev.env:35689->flask-app.dev.env:27017 (CLOSE_WAIT)
uwsgi   2939 www-data    6u  IPv4  20419      0t0  TCP flask-app.dev.env:35688->flask-app.dev.env:27017 (CLOSE_WAIT)
```

重新启动MongoDB，不做其他操作。

```bash
$ sudo service mongodb start 
mongodb start/running, process 4103
$ sudo lsof -i:27017
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
uwsgi   2938 www-data    6u  IPv4  20577      0t0  TCP flask-app.dev.env:35689->flask-app.dev.env:27017 (CLOSE_WAIT)
uwsgi   2939 www-data    6u  IPv4  20419      0t0  TCP flask-app.dev.env:35688->flask-app.dev.env:27017 (CLOSE_WAIT)
mongod  4103  mongodb    9u  IPv4  24443      0t0  TCP flask-app.dev.env:27017 (LISTEN)
```

可以看到，连接还是没有建立。尝试访问相应的Web服务，发现服务慢慢恢复正常。

```bash
$ sudo lsof -i:27017
COMMAND  PID     USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
uwsgi   2929 www-data   13u  IPv4  24558      0t0  TCP flask-app.dev.env:35707->flask-app.dev.env:27017 (ESTABLISHED)
uwsgi   2938 www-data    6u  IPv4  24745      0t0  TCP flask-app.dev.env:35709->flask-app.dev.env:27017 (ESTABLISHED)
uwsgi   2939 www-data    6u  IPv4  24636      0t0  TCP flask-app.dev.env:35708->flask-app.dev.env:27017 (ESTABLISHED)
mongod  4103  mongodb    9u  IPv4  24443      0t0  TCP flask-app.dev.env:27017 (LISTEN)
mongod  4103  mongodb   12u  IPv4  24559      0t0  TCP flask-app.dev.env:27017->flask-app.dev.env:35707 (ESTABLISHED)
mongod  4103  mongodb   13u  IPv4  24637      0t0  TCP flask-app.dev.env:27017->flask-app.dev.env:35708 (ESTABLISHED)
mongod  4103  mongodb   16u  IPv4  24746      0t0  TCP flask-app.dev.env:27017->flask-app.dev.env:35709 (ESTABLISHED)
```

Web服务还是能恢复的。但是，在后续尝试的过程中发现，如果在有持续访问的情况下，连接状态会进入`CLOSE_WAIT`状态，并且很难重新连接上，HTTP请求大量504，重启uwsgi进程才能恢复回正常。

另外，补充一个连接池的文档：http://api.mongodb.com/python/current/faq.html#how-does-connection-pooling-work-in-pymongo

尝试解决这个问题，发现是uwsgi的日志中存在以下信息：
```
/home/vagrant/env/local/lib/python2.7/site-packages/pymongo/topology.py:143: UserWarning: MongoClient opened before fork. Create MongoClient with connect=False, or create client after forking. See PyMongo's documentation for details: http://api.mongodb.org/python/current/faq.html#using-pymongo-with-multiprocessing>
  "MongoClient opened before fork. Create MongoClient "
```

发现原来是uwsgi在启动子进程前，`MongoClient`就已经创建，而文档中要求这种情况下需要使用`connect=False`选项，然而Flask-MongoEngine并没有处理这个配置。https://github.com/MongoEngine/flask-mongoengine/issues/266 这就是坑。
