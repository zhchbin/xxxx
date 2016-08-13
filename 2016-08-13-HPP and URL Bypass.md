## HTTP Parameter Pollution

From https://hackerone.com/reports/114169

For example:

> https://www.digits.com/login?consumer_key=9I4iINIyd0R01qEPEwT9IC6RE&host=https%3A%2F%2Fwww.periscope.tv&host=https%3A%2F%2Fattacker.com

The first host (host=https://www.periscope.tv) is validated but not the second one. After authentication the second host (host=https://attacker.com) is used as the transfer origin.

## URL Bypass
From https://hackerone.com/reports/108113

However, it is discovered that when outputting a non-ASCII character in the header, it will get converted to a question mark (?). This happens after the validation. Thus, attacker can bypass the validation by putting his/her own domain followed by a non-ASCII character in the authority part.

Here's how it works:

Input:

```
https://attacker.com%ff@www.periscope.tv
--------\  authority   /\   hostname   /
The URL is parsed and passes the validation because the hostname matches the registered domain.
```

Output:
```
https://attacker.com?@www.periscope.tv
--------\ hostname /-\     query     /
```
Since the URL is outputted in the location header, `%ff` which is non-ASCII is converted. Now suddenly the hostname becomes attacker.com and everything after the question mark becomes the query part. Finally the victim will be redirected to attacker's site with victim's account's OAuth credential.
