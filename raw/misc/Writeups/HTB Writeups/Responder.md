
---

date: 2025-12-27
status: #completed 
platform: [[HTB]] [[Starting Point]]
difficulty: [[VERY EASY]]
tags: [[Windows]] [[Directory Traversal]] [[RFI]] [[responder-utility]] [[john-the-ripper]]

---
# First Look
NMAP scan to check all open ports, then -sC -sV those open ports to maximize efficiency. There are three open ports, these are: 80, 5985. 80 is an Apache instance which is a Apache httpd 2.4.52 ((Win64) OpenSSL/1.1.1m PHP/8.1.1), 5985 is wsman which is a protocol for managing IT Infrastructure. When accessing the web page, it gives us a dns resolution. I think we have to put it in our /etc/ file where it can access that specific domain name, the domain name is unika.htb. Since it is an Apache instance, it uses PHP so lets try to find information on unika.htb. Also there is a URL Parameter when switching to another language.
# Exploit
To fully understand what happened, we go step by step. The server uses virtual hosting, which redirects IP-based requests to unikha.htb domain. So I inputted the IP address and the domain in my etc/hosts. Then use directory busting on the website, there we found a .php file called index.php with a URL parameter variable, this seems to change the language of the page. If there is a URL Parameter we first do some Directory Traversal, since this is a windows instance we used `../../../../../../windows/system32/drivers/etc/hosts` since the question is pointing towards this path, but if we do encounter a problem that doesn't lead us anywhere we first try to check these paths. 
```powershell
C:\Windows\win.ini
C:\Windows\system32\drivers\etc\hosts
C:\xampp\apache\logs\access.log # this is included because we can do log poisoning if this is in the problem
C:\Users\<known-username>\Desktop\user.txt
C:\Windows\System32\config\SAM
```
After that we try Remote File Inclusion where the server tries to connect to another IP, which in this case would be our machine. We run responder to create a fake SMB server, basically waiting for LLMNR or NBT-NS. He lies to the one who sent the request and says that he is the file server they are looking for, with that they try to authenticate with the fake server and we catch the handshake. There is a catch, windows does not send plain-text credentials, it hashes it using a Challenge-Response mechanism which is NTLMv2-SSP. Since have got this hash, we need to crack this using John The Ripper. After cracking it with John The Ripper, we got the credentials of administrator user. After that we need a powershell instance that we can connect to the machine with, in this case we used Evil-WinRM since we are in a linux environment. By connecting in the Evil-WinRM we could enumerate files and directories until we find the flag.txt

# Questions
- When visiting the web service using the IP address, what is the domain that we are being redirected to?
- Which scripting language is being used on the server to generate webpages?
- What is the name of the URL parameter which is used to load different language versions of the webpage?
- Which of the following values for the `page` parameter would be an example of exploiting a Local File Include (LFI) vulnerability: "french.html", "//10.10.14.6/somefile", "../../../../../../../../windows/system32/drivers/etc/hosts", "minikatz.exe"
- Which of the following values for the `page` parameter would be an example of exploiting a Remote File Include (RFI) vulnerability: "french.html", "//10.10.14.6/somefile", "../../../../../../../../windows/system32/drivers/etc/hosts", "minikatz.exe"
- What does NTLM stand for?
- Which flag do we use in the Responder utility to specify the network interface?
- There are several tools that take a NetNTLMv2 challenge/response and try millions of passwords to see if any of them generate the same response. One such tool is often referred to as `john`, but the full name is what?.
- What is the password for the administrator user?
- We'll use a Windows service (i.e. running on the box) to remotely access the Responder machine using the password we recovered. What port TCP does it listen on?

# Lessons Learned
- wsman has two ports, 5985 for unencrypted 5986 for encrypted.
- windows is hard.
- NTLM hash is stored locally on windows, you only find these via post-exploit.
- NetNTLMv2 Hash is sent over the network during a handshake, these are captured using responder and crack the hash with JtR

# Further Improvements
- Workflow was too slow, was not adaptive to the windows environment and my tools are not ready.