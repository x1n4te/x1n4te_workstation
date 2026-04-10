# Basic Commands
```sql
psql -h localhost -p 5433 -U christine -d database_name

SELECT datname FROM pg_database;

SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';

SELECT * FROM table_name;

```