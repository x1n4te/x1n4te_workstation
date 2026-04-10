
---

date: 2025-12-29
status: #completed 
platform: [[HTB]] [[Starting Point]]
difficulty: [[VERY EASY]]
tags: [[Linux]] [[ftp]] [[SSH]] [[Postgre-SQL]]

---
# First Look
There are two open ports, which is port 21, and 22. 21 is FTP and 22 is SSH. I think the challenge is here to find credentials via the FTP sever then ssh into the machine. The version of FTP is vsftpd 3.0.3 and then the SSH version is OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0). The ftp has a folder called mail_backup, this folder has two files which are a pdf regarding password policy and an email to new comers. Using critical thinking skills there is a password set for each new account but if this was not changed after logging in, we have a vulnerability. In the email there is a list of email accounts, we use the name of these email accounts such as "christine" and try the set password which is "funnel123#!#". This got us in the SSH, from here we can list down files and services running on the server. By listing down services that is being listed in local ports we can see that postgresql is running in 5432. The issue is we cant access it, yet.

# Exploit
The exploit here is to create a local port forwarding via SSH, this is done by using `ssh -L 5433:localhost:5432 christine@$IP` by using this command we are issuing our local port to access the port of the remote machine and forward traffic from our port to that port so we can access it. This can also be done dynamically, it means that I can only specify a local port then turns it into a SOCKS proxy. The SOCKS proxy can send traffic to local port 1080, then the SSH server decides which service it is meant for. This is done by `ssh -D 1080 user@ssh_server`. After that just login the postgreSQL with the same credentials and enumerate all databases and tables of the database and select the flag.

# Questions
- How many TCP ports are open?
- What is the name of the directory that is available on the FTP server?
- What is the default account password that every new member on the "Funnel" team should change as soon as possible?
- Which user has not changed their default password yet?
- Which service is running on TCP port 5432 and listens only on localhost?
- Since you can't access the previously mentioned service from the local machine, you will have to create a tunnel and connect to it from your machine. What is the correct type of tunneling to use? remote port forwarding or local port forwarding?
- What is the name of the database that holds the flag?
- Could you use a dynamic tunnel instead of local port forwarding? Yes or No.

# Further Improvements
- Familiarize commands from different SQL because i don't know how to select databases from the sql shell, i had to go out to select a database.
