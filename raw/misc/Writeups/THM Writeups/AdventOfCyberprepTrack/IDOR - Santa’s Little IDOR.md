AOC2025-IDOR-V9@10.49.190.192
12/13/2025 | 9:53 AM - 
[[IDOR]] [[Walkthrough]] [[THM]] [[Burpsuite]]
#completed 

> [!NOTE] Credentials
> Username: niels
> Password: TryHackMe#2025
> http://10.49.190.192

Phase 1: Reconnaissance
There are two open ports, ssh and nginx web server (22, 80). 
```
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   256 a2:75:6b:ff:9c:37:25:1d:33:b7:c3:6d:47:2e:a0:f8 (ECDSA)
|_  256 f0:38:56:47:0a:02:87:72:c5:a2:19:6e:e2:08:42:de (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-title: New chat
|_http-server-header: nginx/1.24.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

I haven't really understood how i should start with this type of vulnerability, but it says in the challenge that i should check the network tab to see the request that comes in when the page loads. When i check whenever to do this, my key indication is the directory with the PHP function or a variable passing in the directory. But it seems that this way is also an efficient way since maybe it uses its variables instantly, which in this case is, because whenever i view the page source and not inspect it, it just shows me a bare bones source code, whenever i inspect it it is much more populated. Looking at the network tab you can see two requests made by the web server. ![[Screenshot_20251213_101220.png]]

You can already see the user_id being used in the function, so lets try to change this and maybe we can get the admin id which is usually the first user id. 

This room is a bit tricky, since it there are different ways to attack this vulnerability. First is just the ID, but that seems counterproductive, since this will not show the full details of the id since it is still being authenticated by the system so it wont show the childs. Use the base64 encode to get all details with the usage of burpsuite intruder that repeats 1-30.