[[VERY EASY]] [[Linux]] [[Starting Point]] [[rsync]]
#completed 
# FIRST LOOK
rsync is the protocol that is going to be tackled in the machine. it's default port is in 873.

```
PORT    STATE SERVICE VERSION
873/tcp open  rsync   (protocol version 31)
```

rsync is a protocol that synchronizes the files and directories between system, you can also list down files in this.

# EXPLOIT
First list down directories in the rsync by using the cli command rsync. `rsync --list-only $IP::`, this command will first start with the root directory, and it will check what are the files or directories it is there. After that to go deeper use it again and if you find a file that is interesting you can use `rsync $IP::directory/tofile wheretoputfile/filename` 

# QUESTIONS
- What is the default port for rsync?
- How many TCP ports are open on the remote host?
- What is the protocol version used by rsync on the remote machine?
- What is the most common command name on Linux to interact with rsync?
- What credentials do you have to pass to rsync in order to use anonymous authentication? anonymous:anonymous, anonymous, None, rsync:rsync

