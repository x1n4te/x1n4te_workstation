
---

date: 2025-12-28
status: #completed 
platform: [[HTB]] [[Starting Point]]
difficulty: [[VERY EASY]]
tags: [[Linux]] [[feroxbuster]] [[Sub-domain]] [[aws-cli]] [[Reverse Shell]] [[Shell-Injection]]

---
# First Look
There are two open ports based from a quick port scan from nmap, the open ports are: 22 and 80. These two tcp protocols which are ssh and http. the SSH version is `OpenSSH 7.6p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)` while the http version is `Apache httpd 2.4.29 ((Ubuntu))`. The apache instance is a band page where you can buy tickets for their tour and the bands information. In the contact section there is a domain name, we can use virtual host discovery to check the domain. After enumeration we found out that there is a subdomain named s3. s3 sounded familiar as past challenges have presented it, it was an amazon s3, which is an object storage service from AWS. When checking other files that does not exist it says that there is no bucket for this certain file, so it is a Amazon S3 service.

# Exploit
The exploit itself revolved around transferring files into the S3 service, by using aws-cli. This tool gives us four commands to work with this service, which are `ls` `cp` `rm` `mb`, there is another one but it is not needed since it is `presign`. By using the aws-cli to connect to the endpoint we can list down what is in that endpoint and what it connects to, in this case s3.thetoppers.htb connects to the toppers.htb. Since we have already access to the s3.thetoppers.htb and we did not see any files, maybe it is in the toppers.htb, so to go further down the rabbit hole we would need to use a reverse shell to get in the toppers.htb, since we can input files by using cp into the toppers.htb. Create a .sh file that connects our bash to the bash of the server, but first we need to create a php function that will allows us to use commands via the URL parameter. When that is done, we move that file into thetoppers.htb via the aws-cli. This way we can create a http server in our local machine and host the .sh file which will be a reverse shell payload. With the php file we curl our .sh file from our local machine so that it triggers in their system. Then we already have a way to enumerate files inside. The flag was seen in /var/www/flag.txt.
# Questions
- How many TCP ports are open?
- What is the domain of the email address provided in the "Contact" section of the website?
- In the absence of a DNS server, which Linux file can we use to resolve hostnames to IP addresses in order to be able to access the websites that point to those hostnames?
- Which sub-domain is discovered during further enumeration?
- Which service is running on the discovered sub-domain?
- Which command line utility can be used to interact with the service running on the discovered sub-domain?
- Which command is used to set up the AWS CLI installation?
- What is the command used by the above utility to list all of the S3 buckets?
- This server is configured to run files written in what web scripting language?

# Further Improvements
- When inside a main scenario, use a less noisy way to enumerate files. But since it is not a real scenario we use linpeas by also serving this in our http server and curling the file.
- Further improve aws-cli knowledge base.