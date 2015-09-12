## 反射型漏洞

直接把URL的输出在iframe的src中，对，没有过滤。这个问题我都不想记了。

```
URL：http://www.xxxxx.net/yun/index.php?m=Index&c=Content&a=index&cid=21&aid=3
```

页面HTML中出现了：

```html
<iframe frameborder="0" id="comment" scrolling="no" style="padding: 0px;margin: 0px;" width="100%"
  src="http://www.xxxxx.net/yun/index.php?g=Addons&m=Comment&c=Comment&mid=1&cid=21&aid=3"></iframe>
```

Payload:

```
URL: http://www.xxxxx.net/yun/index.php?m=Index&c=Content&a=index&mid=1&cid=21aaa&aid=3%22%20onmouseover=%22alert%281%29
```

这个会被`Chrome`的xss过滤器拦截，在其他浏览器下可以。
