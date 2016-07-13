## URL检查不严格被绕过的几种情况

1. 只检查了URL中是否有合法的域名地址，绕过方式很简单，直接用：`http://evil.com/?http://victim.com`即可。
2. 前缀校验不严格，前缀应该以`/`结尾的，但没有，绕过：`http://victim.com@evil.com/`或者`http://victim.com.evil.com`
3. 使用`?`绕过检查，在 http://wooyun.org/bugs/wooyun-2016-0178241 中学到的，`http://evil.com?.victim.com`会被浏览器识别为`http://evil.com/?.victim.com`
4. From: http://www.slideshare.net/fransrosen/the-secret-life-of-a-bug-bounty-hunter-frans-rosn-security-fest-2016
  * https://www.victim.com/account/logout?redirect_url=https://example.com\@www.victim.com
  * https://www.linkedin.com/uas/login?session_redirect=https://example.com%252f@www.linkedin.com%2Fsettings
  * https://vimeo.com/log_in?redirect=/%09/example.com
  * https://test6473.zendesk.com/access/login?return_to=//example.com:%252525252f@test6473.zendesk.com/x
  * https://trello.com/login?returnUrl=/\example.com
