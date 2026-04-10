Default Port: `27017`
## Basic Commands
```mysql
show dbs                           -- List databases.
use <db>                           -- Switch context.
show collections                   -- List tables/collections.
db.<collection>.find().pretty()    -- Read data.
```
## Tooling
```bash
# mongosh - Interactive shell.
mongosh mongodb://$IP:27017
# mongodump - Database backup/export.
mongodump --host $IP --port 27017 --out /tmp/
```
## Automation
```js
[!TIP] Automation Snippet
db.getMongo().getDBNames().forEach(function(d){
	print("DB: " + d);
	db.getSiblingDB(d).getCollectionNames().forEach(function(c){
		print("  Coll: " + c);
	});
});
```
