10:51 AM - 12:22 PM
Machine name: Lo-Fi
IP Address: 10.49.175.193
[[Shell-Injection]]
#completed 

> [!NOTE] Description
> Want to hear some lo-fi beats, to relax or study to? We've got you covered!
> **Access this challenge** by deploying both the vulnerable machine by pressing the green "Start Machine" button located within this task, and the TryHackMe AttackBox by pressing the  "Start AttackBox" button located at the top-right of the page. Navigate to the following URL using the AttackBox: [http://10.49.175.193](http://10.49.175.193/) and find the flag in the **root of the filesystem.**

## PHASE 1: Reconnaisance 

I started by analyzing the technology stack to identify potential attack vectors. Since the challenge description hints at a webpage, I prioritized web exploitation over a standard port scan.

```
http://10.49.175.193 [200 OK] Apache[2.2.22], Bootstrap[4.5.0], Country[RESERVED][ZZ], Frame, HTML5, HTTPServer[Ubuntu Linux][Apache/2.2.22 (Ubuntu)], IP[10.49.175.193], Title[Lo-Fi Music], YouTube
```

The server is running an older version of Apache (2.2.22) and uses PHP. This suggests we should look for vulnerabilities specific to PHP web apps, such as Local File Inclusion (LFI).

## PHASE 2: Enumeration

```
200      GET      128l      230w     4162c http://10.49.175.193/
200      GET      128l      230w     4162c http://10.49.175.193/index.php
200      GET        5l       17w      284c http://10.49.175.193/game.php
200      GET        5l       17w      286c http://10.49.175.193/coffee.php
200      GET        5l       17w      285c http://10.49.175.193/lo-fi.php
```

I used two different scans for this, a directory scan and a extension scan. The directory scan checks if there is directories we can access, but it seems that the only accessible directory is the index directory. With this information i determined that the web server is indeed apache as it is using .php as the files.


## PHASE 3: Exploitation

Now lets try tampering with the web content itself.![[Screenshot_20251208_114457.png]]

Tried using search for just in case it has any SQLi attack vectors. so lets check with a simple checker such as ' or 1=1 -- -'. Seems that it doesn't work. so lets proceed with the path file inclusion. 

![[Screenshot_20251208_115329.png]]

Given the challenge hints and the PHP structure, I suspected LFI. I looked for parameters in the URL that fetched files and attempted to traverse the directory.

![[Screenshot_20251208_115703.png]]

Seems like there is no user account, but if i tried it with /root/.bash_history it detects me and doesn't give me permission to view. One of the things i can do here is to try to find a way to get in the root directory. LFI seems hard if i dont have any way to list down files, ill try to use fuzz.

NOTE TO SELF: FIRST TRY SIMPLE ../../../../flag.txt

It was in the base directory...

![[Screenshot_20251208_122141.png]]

Man.

## Solution

Overthinking the process, i thought i should get root access directly onto the system so i used Fuzz to check the root directory so I can access more files. But read the description better next time, as it states that the flag was in the "root of the file system.". it was just `../../../../flag.txt` which was so simple.

**flag{e4478e0eab69bd642b8238765dcb7d18}**

#### USED COMMANDS:
```
whatweb http://$IP > web/whatweb.txt
nmap -p- --min-rate 1000 -T4 $IP -oN nmap/initial_ports
```