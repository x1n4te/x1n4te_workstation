
---

date: 2025-12-27
status: #completed
platform: [[HTB]] [[Starting Point]]
difficulty: [[VERY EASY]]
tags: [[Starting Point]] [[mysql]]

---
# First Look
According to my nmap scan there is only one open TCP port which is mySQL, it is open on port 3306. mySQL is an open-source relational database management system (RDBMS) that is frequently used for it's ease of use and power. Based from the detailed scan report using `-sC` and `-sV`, it is a mariaDB version —5.5.5-10.3.27-MariaDB-0+deb10u— there is also details regarding an auth plugin name called mysql_native_password. This might be pointing me to use the native password, but after researching about it, this is just a legacy auth method that uses the remnants of SHA-1 to verify user passwords. I can maybe get in via this vector, but let us see. 

# Exploit
Let's try to log in via [[mariaDB]] -u root -h $IP to see if there is no authentication for root since root is the admin user of mariaDB instances. It gave me an error message sayings that `TLS/SSL error`, i added `--ssl=0` to the tags. It worked, after this we just enumerate the vectors using SQL commands, such as select databases, use table, and SELECT * FROM TABLE;

# Lessons Learned
There are three default schemas in the database, information_schema, mysql, performance_schema. These three schemas are key default system schemas that utilizes technology to keep the database fast and easier to manage. info schema is a read-only catalog that provides details regarding all databases including tables, columns and other objects, basically gives us metadata about the system. mysql is for user privileges, credentials and ACL. Lastly is performance_schema, this schema as in its name provides the performance details about the mariaDB server.

# Questions
- During our scan, which port do we find serving MySQL?
- What community-developed MySQL version is the target running?
- When using the MySQL command line client, what switch do we need to use in order to specify a login username?
- Which username allows us to log into this MariaDB instance without providing a password?
- In SQL, what symbol can we use to specify within the query that we want to display everything inside a table?
- In SQL, what symbol do we need to end each query with?

# Further Improvements
Instead of `SELECT * FROM ...;` for every table, use information_schema directly to map the entire server in one go. This will only get the tables or databases that are not in information_schema,mysql, and performance_schema.

```mariadb
SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema', 'mysql', 'performance_schema');
```

The SSL=0 tag is only used because of the version of the mariaDB server, but most of the time this is not needed anymore since most services support the modern TLS handshake.