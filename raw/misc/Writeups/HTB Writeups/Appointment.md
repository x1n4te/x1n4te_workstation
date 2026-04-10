[[VERY EASY]] [[SQLi]] [[Linux]] [[SQLi]] [[Starting Point]]
#completed 
# FIRST LOOK
NMAP scan points to a http port open, uses apache as its web tech. Only has a login form when on the detail scan.

# EXPLOIT
SQLi is one of the easiest but most trickiest injection depending on the security. In this case it's easy, as the login form is not validated as much. `SQL.QUERY(f"SELECT * FROM users WHERE username = userinput, password = userinput2)` If we put a comment out after userinput, we do not need to have password. Just use the payload `admin ' #` then any password, then we got the flag.

e3d0796d002a446c0e622226f42e9672

# QUESTIONS
- What does the acronym SQL stand for?
- What is one of the most common type of SQL vulnerabilities?
- What is the 2021 OWASP Top 10 classification for this vulnerability?
- What does Nmap report as the service and version that are running on port 80 of the target?
- What is the standard port used for the HTTPS protocol?
- What is a folder called in web-application terminology?
- What is the HTTP response code is given for 'Not Found' errors?
- Gobuster is one tool used to brute force directories on a webserver. What switch do we use with Gobuster to specify we're looking to discover directories, and not subdomains?
- What single character can be used to comment out the rest of a line in MySQL?
- If user input is not handled carefully, it could be interpreted as a comment. Use a comment to login as admin without knowing the password. What is the first word on the webpage returned?
