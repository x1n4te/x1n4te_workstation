12/12/25 | 11:50 AM - 12:40 PM
[[Walkthrough]] [[THM]] [[AI]]
#completed 
AoC2025 Day 4 ----- AI Showcase
`10.48.180.164`

As technology advances, so does humans. I like to think that AI is our next evolution, its a scary thought but it is happening all around us, we are autonomous so we have the upper hand, but when the next innovation allows us to have autonomous AI with free thinking on what should happen. It's sky net all over again. Let's not think about that first, let's see how AI is being utilized in cybersecurity.

The room showcases how AI is being utilized as a defensive measure and an offensive measure. So going through the stages we can get how a red team AI is being used, as well as in blue team, but it doesn't just end there — It is also being used in Software Development.

First lets do a quick scan on the machine, seeing that in the stage 2 it says that there is a web application open in the room. After a quick scan we can see that there are 4 open ports which are 20, 80, 3000, 5000. For a detailed version ill put it down underneath. 

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 d6:c3:92:16:7d:c7:65:7f:f4:db:cc:69:05:83:62:ec (ECDSA)
|_  256 43:6b:43:9c:8a:fc:31:79:5d:7c:fa:e3:15:d1:e8:f8 (ED25519)
80/tcp   open  http    nginx 1.24.0 (Ubuntu)
|_http-title: Van SolveIT
|_http-cors: HEAD GET POST PUT DELETE PATCH
|_http-server-header: nginx/1.24.0 (Ubuntu)
3000/tcp open  http    Node.js Express framework
|_http-cors: HEAD GET POST PUT DELETE PATCH
|_http-title: Van SolveIT
5000/tcp open  http    Apache httpd 2.4.65 ((Debian))
|_http-title: TBFC
|_http-server-header: Apache/2.4.65 (Debian)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

To validate the nmap results, lets check the what web for each ports.

```
http://10.48.180.164 [200 OK] Bootstrap, Country[RESERVED][ZZ], HTML5, HTTPServer[Ubuntu Linux][nginx/1.24.0 (Ubuntu)], IP[10.48.180.164], Script, Title[Van SolveIT], UncommonHeaders[access-control-allow-origin], X-Powered-By[Express], nginx[1.24.0]

http://10.48.180.164:3000 [200 OK] Bootstrap, Country[RESERVED][ZZ], HTML5, IP[10.48.180.164], Script, Title[Van SolveIT], UncommonHeaders[access-control-allow-origin], X-Powered-By[Express]

http://10.48.180.164:5000 [200 OK] Apache[2.4.65], Bootstrap, Country[RESERVED][ZZ], HTML5, HTTPServer[Debian Linux][Apache/2.4.65 (Debian)], IP[10.48.180.164], PHP[8.1.33], PasswordField[password], Script, Title[TBFC], X-Powered-By[PHP/8.1.33]
```

So lets start utilizing the red team assistant to attack the web server which would be utilizing python scripts. I created my own prompt in the AI in the room, but it seems that its hardwired to first tell me what to ask. Even without AI, this room is easy to do, since it is just a SQLi payload on the "secure" login auth page, this payload will work.
[[SQLi]] : alice ' or 1 = 1 -- -'

