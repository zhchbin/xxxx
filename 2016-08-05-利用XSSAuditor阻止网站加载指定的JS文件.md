当`X-XSS-Protection: 1`的时候，我们可以通过在请求参数中填入一些会在网页中出现的代码，使得过滤器以为这是个XSS攻击，然后阻止该文件的执行，导致指定的网页不加载特定的JS文件，例如：

http://www.qq.com/?%3Cscript%20type=%22text/javascript%22%20src=%22http://mat1.gtimg.com/www/asset/lib/jquery/jquery/jquery-1.11.1.min.js%22%3E%3C/script%3E

![](http://ww3.sinaimg.cn/large/7184df6bgw1f6iw4i8mvaj20yy0lhgxo.jpg)
