Process of discovering and mapping all the valid subdomains with in a specific domain name.

# Tooling
```bash
# passive
## quick and dirty scan
subfinder -d example.com
## clean scan
subfinder -d example.com -silent -o subdomains.txt

# active
## massive bruteforce
puredns bruteforce /path/to/wordlist.txt example.com -r resolvers.txt
## validate cleanscan results
puredns resolve subdomains.txt -r resolvers.txt

# hidden
## internal/vhost discovery
ffuf -w /path/to/wordlist.txt -u http://example.com -H "Host: FUZZ.example.com" -fs x

# combine attack
subfinder -d example.com -silent | puredns resolve -r resolvers.txt | httpx -title -status-code
```
