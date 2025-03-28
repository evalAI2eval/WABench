## Dataset Example
The following is a simple labeled dataset example with benign and malicious web logs in json format
```
[
    {"log": "192.168.1.1 - - [10/Mar/2025:10:00:00 +0000] \"GET /index.html HTTP/1.1\" 200", "label": "benign"},
    {"log": "192.168.1.2 - - [10/Mar/2025:10:05:00 +0000] \"GET /login?user=admin&pass=123456 HTTP/1.1\" 200", "label": "benign"},
    {"log": "192.168.1.3 - - [10/Mar/2025:10:10:00 +0000] \"GET /search?q=<script>alert(1)</script> HTTP/1.1\" 200", "label": "malicious"},
    {"log": "192.168.1.4 - - [10/Mar/2025:10:15:00 +0000] \"GET /admin.php' OR '1'='1 HTTP/1.1\" 200", "label": "malicious"}
]
```
For example we have the following:- 
- Benign Logs: Normal browsing requests.
- Malicious Logs: SQL injection and XSS attacks like the third log above, we have ```(<script>alert(1)</script)``` which is indicator of XSS attack (XSS is a common web attack).

We can collect logs from the following public datasets
- CICIDS2017 (contains web attacks)
- OWASP ZAP logs
- DARPA Cyber Grand Challenge datasets
