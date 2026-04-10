[[VERY EASY]] [[Linux]] [[Starting Point]] [[Path Traversal]]
#completed 
# First Look
Based from my NMAP scan which is:


```
> nmap -p- --min-rate 1000 -T4 $IP
Starting Nmap 7.98 ( https://nmap.org ) at 2025-12-26 18:41 +0800
Nmap scan report for 10.129.12.227 (10.129.12.227)
Host is up (0.24s latency).
Not shown: 65534 closed tcp ports (conn-refused)
PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 75.18 seconds
```

This is a web application machine, based from the first question it's going to be path traversal. The platform says i should use gobuster, but since I'm more knowledgeable in feroxbuster i used the command `feroxbuster -u http://$IP -x php`.

# EXPLOIT
In the feroxbuster output, we can see two detected directories. w3.css and admin.php.

```
200      GET       25l       69w      612c http://10.129.12.227/
200      GET      384l      774w    29679c http://10.129.12.227/w3.css
200      GET       31l       66w      999c http://10.129.12.227/admin.php
```

admin.php has a login form that i can exploit, but first try easy passwords. admin | admin is a credential in the system we can log in. Just stumbled upon it when i was trying common credentials. Flag was in the home page "6483bee07c1c1d57f14e5b0717503c73".

# Questions
- Directory Brute-forcing is a technique used to check a lot of paths on a web server to find hidden pages. Which is another name for this? (i) Local File Inclusion, (ii) dir busting, (iii) hash cracking.
- What switch do we use for nmap's scan to specify that we want to perform version detection
- What does Nmap report is the service identified as running on port 80/tcp?
- What server name and version of service is running on port 80/tcp?
- What switch do we use to specify to Gobuster we want to perform dir busting specifically?
- When using gobuster to dir bust, what switch do we add to make sure it finds PHP pages?
- What page is found during our dir busting activities?
- What is the HTTP status code reported by Gobuster for the discovered page?
