[[VERY EASY]] [[Windows]] [[Starting Point]] [[RDP]]
#completed 
# NMAP SCAN RESULT
```
Starting Nmap 7.98 ( https://nmap.org ) at 2025-12-26 17:58 +0800
Warning: 10.129.1.13 giving up on port because retransmission cap hit (6).
Nmap scan report for 10.129.1.13 (10.129.1.13)
Host is up (0.24s latency).
Not shown: 65496 closed tcp ports (conn-refused)
PORT      STATE    SERVICE
135/tcp   open     msrpc
139/tcp   open     netbios-ssn
445/tcp   open     microsoft-ds
1318/tcp  filtered krb5gatekeeper
3389/tcp  open     ms-wbt-server
3436/tcp  filtered gc-config
5985/tcp  open     wsman
8748/tcp  filtered unknown
10068/tcp filtered unknown
12445/tcp filtered unknown
16836/tcp filtered unknown
22802/tcp filtered unknown
25583/tcp filtered unknown
28769/tcp filtered unknown
31818/tcp filtered unknown
35429/tcp filtered unknown
36664/tcp filtered unknown
40184/tcp filtered unknown
41782/tcp filtered unknown
42825/tcp filtered unknown
43115/tcp filtered unknown
43580/tcp filtered unknown
47001/tcp open     winrm
47355/tcp filtered unknown
49664/tcp open     unknown
49665/tcp open     unknown
49666/tcp open     unknown
49667/tcp open     unknown
49668/tcp open     unknown
49669/tcp open     unknown
49670/tcp open     unknown
49671/tcp open     unknown
50317/tcp filtered unknown
55201/tcp filtered unknown
55402/tcp filtered unknown
56916/tcp filtered unknown
61911/tcp filtered unknown
64457/tcp filtered unknown
65354/tcp filtered unknown

Nmap done: 1 IP address (1 host up) scanned in 81.86 seconds
```

# First Look
This section is being guided with the questions down below.

The first question is regarding about Remote Desktop Protocol. There are numerous ports opened but some services are unknown, but ill create a table for each port just in case it comes in handy.

| Port Number | Service Name   | State    | Description                     |
| ----------- | -------------- | -------- | ------------------------------- |
| 135         | msrpc          | open     | Microsoft Remote Procedure Call |
| 139         | netbios-ssn    | open     |                                 |
| 445         | microsoft-ds   | open     |                                 |
| 1318        | krb5gatekeeper | filtered |                                 |
| 3389        | ms-wbt-server  | open     | This is for the RDP connection. |
| 3436        | gc-config      | filter   |                                 |
| 5985        | wsman          | open     |                                 |
| 47001       | winrm          | open     |                                 |
The questions in this machine is all about RDP. So let's focus on port 3389, this is used for Microsoft's Remote Desktop Protocol (RDP), allowing users to connect to a machine and control it via a GUI. Using xfreerdp3 and using administrator as the username we can access this machine.

# EXPLOIT
I used xfreerdp3 to connect to this machine, i used the command `xfreerdp3 /v:$IP /u:Administrator`. Flag was in the desktop.

# Questions
- What does the 3-letter acronym RDP stand for?

- What is a 3-letter acronym that refers to interaction with the host through a command line interface?

- What about graphical user interface interactions?

- What is the name of an old remote access tool that came without encryption by default and listens on TCP port 23?

- What is the name of the service running on port 3389 TCP?

- What is the switch used to specify the target host's IP address when using xfreerdp?

- What username successfully returns a desktop projection to us with a blank password?

