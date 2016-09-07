```bash
$ curl -i "https://httpbin.org/redirect-to?url=http://%2577%2577%2577%252E%256D%2569%2563%2572%256F%2573%256F%2566%2574%252E%2563%256F%256D/test"

HTTP/1.1 302 FOUND
Location: http://%77%77%77%2E%6D%69%63%72%6F%73%6F%66%74%2E%63%6F%6D/test
```

* Redirected URL for Internet Explorer: http://www.microsoft.com9crosoft.com/test
* Redirected URL for other browsers: http://www.microsoft.com/test

From: http://blog.innerht.ml/internet-explorer-has-a-url-problem/
