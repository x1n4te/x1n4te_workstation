# Basic Commands
```bash
# command for is service version detection and default script scan.
nmap -sV -sC $IP

# all tcp port scan
nmap -p- $IP 

# all tcp port scan with aggresive timing template
nmap -T 4 -p- $IP

# nmap froce to send packets a min speed of at least that many packets per second
nmap --min-rate <number> -p- $IP
```
