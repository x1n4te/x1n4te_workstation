[[SQLi]] [[root-me]]
#completed 

Always probe around first with login forms, the most simplest test you can do is to use ', this is because it will throw a random ' into the SQL query to the database and if the website is showing verbose error messages, this can lead to a glimpse into the back end logic of the login form. Let's say it said "ERROR: no such user/password" in the error message, so we can suspect that the sql query that was in the backend logic was `SELECT * FROM users WHERE username = '[INPUT]' AND password = '[INPUT]'`. 

By injecting a username such as `' OR 1=1 --`, it resulted to the query logic looking like this. `SELECT * FROM users WHERE username = '' OR 1=1 -- ' AND password = ''`.  This query logic disregarded the password since we commented out the latter parts of the query, and resulted into logging in because we used a boolean statement that always results to true, since OR 1=1 always results to true. Now we just have to append the name of the account in the beginning so we can login as the user you want to be.

Related Payloads that can ex-filtrate more data with just the login form.

```
payloads = [
    "' OR 1=1 --",
    "admin' --",
    "admin' OR '1'='1",
    "' OR 1=1 LIMIT 1 OFFSET 1 --",
    "admin' AND 1=1 --",
    "' UNION SELECT 'admin', 'password' --"
]
```



z