
---

date: 2025-12-27
status: #completed 
platform: [[HTB]] [[Starting Point]]
difficulty: [[VERY EASY]]
tags: [[Linux]] [[ftp]] 

---
# First Look
Found two open ports, 21 and 80. the default protocol for port 21 is FTP, while 80 is for HTTP. FTP version is vsFTPD 3.0.3 and it is allowing anonymous login (FTP code 230), while the HTTP is an Apache instance namely the version is Apache httpd 2.4.41. The web page is a company web page advertising their services, ran directory busting just in case there is any hidden directory. There is a login.php in the dashboard, doesn't seem to be exploitable since there is no verbose error message when using SQLi. I think we need to go through FTP first to input credentials or get credentials. Let's probe further. It is in the FTP server we can get our credentials needed or put credentials, but in this case lets just get credentials.

# Exploit
Login via anonymous since we found out from the nmap scan it allows anonymous logins, from there list down files and transfer to local machine. Two files, username file and a password file. use admin and all the passwords to see if which one is the match, and we are in! The dashboard contains a server admin dashboard, but it also has the flag in it.

# Questions
- What Nmap scanning switch employs the use of default scripts during a scan?
- What service version is found to be running on port 21?
- What FTP code is returned to us for the "Anonymous FTP login allowed" message?
- After connecting to the FTP server using the ftp client, what username do we provide when prompted to log in anonymously?
- After connecting to the FTP server anonymously, what command can we use to download the files we find on the FTP server?
- What is one of the higher-privilege sounding usernames in 'allowed.userlist' that we download from the FTP server?
- What switch can we use with Gobuster to specify we are looking for specific filetypes?
- Which PHP file can we identify with directory brute force that will provide the opportunity to authenticate to the web service?
# Lessons Learned
I found out how much FTP can be used for potential threats. This configuration can lead to data leakage and a way to map out the infrastructure.

Directory busting also should be looked into by the security ops, since it reveals attack vectors. I couldn't have not found out about it if dashboard is not accessible via tools. 

The vsFTPD 3.0.3 always has a misconfig vulnerability. Always check if a service is running as a standalone daemon or through inetd, as this can change how it handles connections and logging.

# Further Improvements
Use this command to get a faster way to dump the ftp server.

```bash
# recursively dumps the server. much faster for combing an entire instance.
wget -r ftp://anonymous@$IP/ 
```
