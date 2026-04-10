Default Port: 6379
## Basic Commands

```bash
# when in redis-cli
INFO        # Display server info
SELECT 0    # Switch to a specific database
KEYS *      # List down keys
GET "flag"  # Retrieves value of the key
TYPE "flag" # Identify data type
```

## Tooling
```bash
# redis-cli - interactive shell
redis-cli -h $IP # if no password set
redis-cli -h $IP --scan --pattern '*' # scan for keys without entering shell.
```

## Automation