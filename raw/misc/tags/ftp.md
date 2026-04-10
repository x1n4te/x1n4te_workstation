Default Port: 21
## Basic Commands
```bash
ftp $IP
# when inside
dir # list down files and directories
get <file> # get file from the ftp server to transfer to your local machine
```

## Tooling
```bash
# lftp > ftp
lftp -u anonymous, $IP

#silent recursive dump
wget -r ftp://anonymous:anonymous@$IP/

# to check for specific vulnerabilties or detailed info before connecting
nmap --script ftp-anon,ftp-bounce,ftp-syst -p 21 $IP

# manual brute forcing if anon login is disabled but have a potential username
hydra -l admin -P /wordlist/directory/file.txt ftp://$IP
```

## Automation
```python
# wala pa hehe
```
