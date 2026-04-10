
---

date: 2026-01-18 
status: #on-going 
platform: [[HTB]]
difficulty: [[EASY]]
tags: [[Windows]]

---
# Tool Reports
[[nmap]] -sV -sC $IP
```bash
PORT     STATE SERVICE  VERSION
80/tcp   open  http     Microsoft IIS httpd 10.0
|_http-server-header: Microsoft-IIS/10.0
|_http-title: Did not follow redirect to http://eighteen.htb/
1433/tcp open  ms-sql-s Microsoft SQL Server 2022 16.00.1000.00; RTM
|_ssl-date: 2026-01-18T11:26:10+00:00; +7h01m41s from scanner time.
| ms-sql-ntlm-info: 
|   10.129.239.178:1433: 
|     Target_Name: EIGHTEEN
|     NetBIOS_Domain_Name: EIGHTEEN
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: eighteen.htb
|     DNS_Computer_Name: DC01.eighteen.htb
|     DNS_Tree_Name: eighteen.htb
|_    Product_Version: 10.0.26100
| ms-sql-info: 
|   10.129.239.178:1433: 
|     Version: 
|       name: Microsoft SQL Server 2022 RTM
|       number: 16.00.1000.00
|       Product: Microsoft SQL Server 2022
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2026-01-18T11:19:45
|_Not valid after:  2056-01-18T11:19:45
5985/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_clock-skew: mean: 7h01m41s, deviation: 0s, median: 7h01m40s
```

[[whatweb]] http://eighteen.htb
```txt
http://eighteen.htb/ [200 OK] Country[RESERVED][ZZ], HTML5, HTTPServer[Microsoft-IIS/10.0], IP[10.129.239.178], Microsoft-IIS[10.0], Title[Welcome - eighteen.htb]
```

[[nikto]] -host http://eighteen.htb/ -Tuning 6
```txt
- Nikto v2.5.0
---------------------------------------------------------------------------
+ Target IP:          10.129.239.178
+ Target Hostname:    eighteen.htb
+ Target Port:        80
+ Start Time:         2026-01-18 12:30:06 (GMT8)
---------------------------------------------------------------------------
+ Server: Microsoft-IIS/10.0
+ /: The anti-clickjacking X-Frame-Options header is not present. See: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options
+ /: The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type. See: https://www.netsparker.com/web-vulnerability-scanner/vulnerabilities/missing-content-type-header/
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ OPTIONS: Allowed HTTP Methods: HEAD, GET, OPTIONS .
+ 534 requests: 0 error(s) and 3 item(s) reported on remote host
+ End Time:           2026-01-18 12:33:04 (GMT8) (178 seconds)
```

[[ffuf]] -u http://eighteen.htb/FUZZ -fc 403,404 -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words-lowercase.txt
```
admin                   [Status: 302, Size: 199, Words: 18, Lines: 6, Duration: 3023ms]
logout                  [Status: 302, Size: 189, Words: 18, Lines: 6, Duration: 2781ms]
register                [Status: 200, Size: 2421, Words: 762, Lines: 76, Duration: 3121ms]
login                   [Status: 200, Size: 1961, Words: 602, Lines: 66, Duration: 3582ms]
.                       [Status: 200, Size: 2253, Words: 674, Lines: 74, Duration: 371ms]
dashboard               [Status: 302, Size: 199, Words: 18, Lines: 6, Duration: 411ms]
features                [Status: 200, Size: 2822, Words: 849, Lines: 88, Duration: 408ms]
```

[[mssqlclient.py]] kevin:'iNa2we6haRj2gaw!'@10.129.239.178
``` bash
Impacket v0.13.0.dev0 - Copyright Fortra, LLC and its affiliated companies 

[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(DC01): Line 1: Changed database context to 'master'.
[*] INFO(DC01): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server 2022 RTM (16.0.1000)
[!] Press help for extra shell commands
SQL (kevin  guest@master)> 
```

```
SQL (appdev  appdev@financial_planner)> SELECT * FROM users;
  id   full_name   username   email                password_hash                                                                                            is_admin   created_at   
----   ---------   --------   ------------------   ------------------------------------------------------------------------------------------------------   --------   ----------   
1002   admin       admin      admin@eighteen.htb   pbkdf2:sha256:600000$AMtzteQIG7yAbZIa$0673ad90a0b4afb19d662336f0fce3a9edd0b7b19193717be28ce4d66c887133          1   2025-10-29 05:39:03
```

[[Windows]]

sliver (LOVELY_BEEF) > sharpview Get-DomainGroup

[*] sharpview output:
[Get-DomainSearcher] search base: LDAP://DC=eighteen,DC=htb
[Get-DomainGroup] filter string: (&(objectCategory=group))
objectsid                      : {S-1-5-32-544}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 0deaf45a-100b-4177-a85b-faafc2b12fae
name                           : Administrators
distinguishedname              : CN=Administrators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Administrators
member                         : {CN=Domain Admins,CN=Users,DC=eighteen,DC=htb, CN=Enterprise Admins,CN=Users,DC=eighteen,DC=htb, CN=Administrator,CN=Users,DC=eighteen,DC=htb}
cn                             : {Administrators}
objectclass                    : {top, group}
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
usnchanged                     : 12801
description                    : Administrators have complete and unrestricted access to the computer/domain
instancetype                   : 4
usncreated                     : 8199
admincount                     : 1
iscriticalsystemobject         : True
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-32-545}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : a0be2901-29e3-45ae-bd4b-bee5a5c1a53c
name                           : Users
distinguishedname              : CN=Users,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Users
member                         : {CN=Domain Users,CN=Users,DC=eighteen,DC=htb, CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=eighteen,DC=htb, CN=S-1-5-4,CN=ForeignSecurityPrincipals,DC=eighteen,DC=htb}
cn                             : {Users}
objectclass                    : {top, group}
usnchanged                     : 12381
description                    : Users are prevented from making accidental or intentional system-wide changes and can run most applications
instancetype                   : 4
usncreated                     : 8202
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-546}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 3b46e08d-a637-407a-86f1-8ca7cadeb596
name                           : Guests
distinguishedname              : CN=Guests,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Guests
member                         : {CN=Domain Guests,CN=Users,DC=eighteen,DC=htb, CN=Guest,CN=Users,DC=eighteen,DC=htb}
cn                             : {Guests}
objectclass                    : {top, group}
usnchanged                     : 12383
description                    : Guests have the same access as members of the Users group by default, except for the Guest account which is further restricted
instancetype                   : 4
usncreated                     : 8208
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-550}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 98f04bf5-7cb7-441e-9c6f-5263eb5c9ae4
name                           : Print Operators
distinguishedname              : CN=Print Operators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Print Operators
cn                             : {Print Operators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12803
instancetype                   : 4
usncreated                     : 8211
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
description                    : Members can administer printers installed on domain controllers
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-32-551}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : a06358f5-6dca-4825-8b9e-bc6c88c66022
name                           : Backup Operators
distinguishedname              : CN=Backup Operators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Backup Operators
cn                             : {Backup Operators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12805
instancetype                   : 4
usncreated                     : 8212
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
description                    : Backup Operators can override security restrictions for the sole purpose of backing up or restoring files
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-32-552}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 5b931a51-10b4-458d-8dfa-a38a19f834a0
name                           : Replicator
distinguishedname              : CN=Replicator,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Replicator
cn                             : {Replicator}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12799
instancetype                   : 4
usncreated                     : 8213
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
description                    : Supports file replication in a domain
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-32-555}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 1bb0f403-af91-4cde-b9f7-8e5837523d9a
name                           : Remote Desktop Users
distinguishedname              : CN=Remote Desktop Users,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Remote Desktop Users
cn                             : {Remote Desktop Users}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8214
instancetype                   : 4
usncreated                     : 8214
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members in this group are granted the right to logon remotely
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-556}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : a0b5a05b-463f-40bf-af95-223c931713ce
name                           : Network Configuration Operators
distinguishedname              : CN=Network Configuration Operators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Network Configuration Operators
cn                             : {Network Configuration Operators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8215
instancetype                   : 4
usncreated                     : 8215
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members in this group can have some administrative privileges to manage configuration of networking features
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-558}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 1ab50e2b-1117-44b4-b8b5-3d3d5585f33b
name                           : Performance Monitor Users
distinguishedname              : CN=Performance Monitor Users,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Performance Monitor Users
cn                             : {Performance Monitor Users}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8216
instancetype                   : 4
usncreated                     : 8216
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group can access performance counter data locally and remotely
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-559}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : e70e17a7-9c61-4ee6-9a3c-83ed618aa131
name                           : Performance Log Users
distinguishedname              : CN=Performance Log Users,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Performance Log Users
cn                             : {Performance Log Users}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8217
instancetype                   : 4
usncreated                     : 8217
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group may schedule logging of performance counters, enable trace providers, and collect event traces both locally and via remote access to this computer
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-562}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : a90592ed-ee82-4ce1-bbcc-859e6fc39f5a
name                           : Distributed COM Users
distinguishedname              : CN=Distributed COM Users,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Distributed COM Users
cn                             : {Distributed COM Users}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8218
instancetype                   : 4
usncreated                     : 8218
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members are allowed to launch, activate and use Distributed COM objects on this machine.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-568}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 4e6106f0-89ff-4bc2-abfa-ef37d8a9c689
name                           : IIS_IUSRS
distinguishedname              : CN=IIS_IUSRS,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 10/27/2025 11:18:51 PM
samaccountname                 : IIS_IUSRS
cn                             : {IIS_IUSRS}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 69718
instancetype                   : 4
usncreated                     : 8219
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Built-in group used by Internet Information Services.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-569}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : ef15ebc2-fb76-4bac-bc27-0fc65ad63633
name                           : Cryptographic Operators
distinguishedname              : CN=Cryptographic Operators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Cryptographic Operators
cn                             : {Cryptographic Operators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8223
instancetype                   : 4
usncreated                     : 8223
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members are authorized to perform cryptographic operations.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-573}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 27bdb60c-8e01-4266-9252-9e188018aa34
name                           : Event Log Readers
distinguishedname              : CN=Event Log Readers,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Event Log Readers
cn                             : {Event Log Readers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8224
instancetype                   : 4
usncreated                     : 8224
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group can read event logs from local machine
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-574}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : be0c6fe4-12f9-471f-aee0-d184de7ddb5c
name                           : Certificate Service DCOM Access
distinguishedname              : CN=Certificate Service DCOM Access,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Certificate Service DCOM Access
cn                             : {Certificate Service DCOM Access}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8225
instancetype                   : 4
usncreated                     : 8225
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group are allowed to connect to Certification Authorities in the enterprise
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-575}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 8a800a43-66b0-48de-a79b-7947071ad747
name                           : RDS Remote Access Servers
distinguishedname              : CN=RDS Remote Access Servers,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : RDS Remote Access Servers
cn                             : {RDS Remote Access Servers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8226
instancetype                   : 4
usncreated                     : 8226
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Servers in this group enable users of RemoteApp programs and personal virtual desktops access to these resources. In Internet-facing deployments, these servers are typically deployed in an edge network. This group needs to be populated on servers running RD Connection Broker. RD Gateway servers and RD Web Access servers used in the deployment need to be in this group.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-576}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 314b9c6f-7c58-4ed6-877e-66e23c7f6480
name                           : RDS Endpoint Servers
distinguishedname              : CN=RDS Endpoint Servers,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : RDS Endpoint Servers
cn                             : {RDS Endpoint Servers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8227
instancetype                   : 4
usncreated                     : 8227
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Servers in this group run virtual machines and host sessions where users RemoteApp programs and personal virtual desktops run. This group needs to be populated on servers running RD Connection Broker. RD Session Host servers and RD Virtualization Host servers used in the deployment need to be in this group.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-577}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : a22b3b9a-d76e-4019-83c8-463e662c4338
name                           : RDS Management Servers
distinguishedname              : CN=RDS Management Servers,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : RDS Management Servers
cn                             : {RDS Management Servers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8228
instancetype                   : 4
usncreated                     : 8228
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Servers in this group can perform routine administrative actions on servers running Remote Desktop Services. This group needs to be populated on all servers in a Remote Desktop Services deployment. The servers running the RDS Central Management service must be included in this group.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-578}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 61497249-21ef-4feb-9c4b-639f73cb9d80
name                           : Hyper-V Administrators
distinguishedname              : CN=Hyper-V Administrators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Hyper-V Administrators
cn                             : {Hyper-V Administrators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8229
instancetype                   : 4
usncreated                     : 8229
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group have complete and unrestricted access to all features of Hyper-V.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-579}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 84f24416-af5f-408e-b3d2-bf1bdae6bfa8
name                           : Access Control Assistance Operators
distinguishedname              : CN=Access Control Assistance Operators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Access Control Assistance Operators
cn                             : {Access Control Assistance Operators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8230
instancetype                   : 4
usncreated                     : 8230
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group can remotely query authorization attributes and permissions for resources on this computer.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-580}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : a0d4aa93-bb13-4655-ba25-30e3c44f2386
name                           : Remote Management Users
distinguishedname              : CN=Remote Management Users,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 10/28/2025 12:21:04 AM
samaccountname                 : Remote Management Users
member                         : {CN=IT,OU=Staff,DC=eighteen,DC=htb}
cn                             : {Remote Management Users}
objectclass                    : {top, group}
usnchanged                     : 69765
description                    : Members of this group can access WMI resources over management protocols (such as WS-Management via the Windows Remote Management service). This applies only to WMI namespaces that grant access to the user.
instancetype                   : 4
usncreated                     : 8231
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-582}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 9910b3d5-408d-4d2d-86f3-820dc7df5706
name                           : Storage Replica Administrators
distinguishedname              : CN=Storage Replica Administrators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Storage Replica Administrators
cn                             : {Storage Replica Administrators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8232
instancetype                   : 4
usncreated                     : 8232
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group have complete and unrestricted access to all features of Storage Replica.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-585}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 09973bb0-0bcb-430a-92b1-e4a5d91de8f5
name                           : OpenSSH Users
distinguishedname              : CN=OpenSSH Users,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : OpenSSH Users
cn                             : {OpenSSH Users}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 8233
instancetype                   : 4
usncreated                     : 8233
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group may connect to this computer using SSH.
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-515}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 6cdda33e-8887-4a9c-add6-aee165052799
name                           : Domain Computers
distinguishedname              : CN=Domain Computers,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Domain Computers
cn                             : {Domain Computers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12332
instancetype                   : 4
usncreated                     : 12330
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : All workstations and servers joined to the domain
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-516}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 84cc3acb-2858-477e-9dc0-d259cb847f97
name                           : Domain Controllers
distinguishedname              : CN=Domain Controllers,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Domain Controllers
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb}
cn                             : {Domain Controllers}
objectclass                    : {top, group}
usnchanged                     : 12809
description                    : All domain controllers in the domain
instancetype                   : 4
usncreated                     : 12333
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-518}
grouptype                      : UNIVERSAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : cf5ccdae-4866-4356-b4d6-845501d7d250
name                           : Schema Admins
distinguishedname              : CN=Schema Admins,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Schema Admins
member                         : {CN=Administrator,CN=Users,DC=eighteen,DC=htb}
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb}
cn                             : {Schema Admins}
objectclass                    : {top, group}
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
usnchanged                     : 12794
description                    : Designated administrators of the schema
instancetype                   : 4
usncreated                     : 12336
admincount                     : 1
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-519}
grouptype                      : UNIVERSAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : ef4e9a46-4cab-4836-8f9b-ef79f6782f01
name                           : Enterprise Admins
distinguishedname              : CN=Enterprise Admins,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Enterprise Admins
member                         : {CN=Administrator,CN=Users,DC=eighteen,DC=htb}
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb, CN=Administrators,CN=Builtin,DC=eighteen,DC=htb}
cn                             : {Enterprise Admins}
objectclass                    : {top, group}
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
usnchanged                     : 12789
description                    : Designated administrators of the enterprise
instancetype                   : 4
usncreated                     : 12339
admincount                     : 1
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-517}
grouptype                      : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 660e3c0c-0c24-4b84-9f02-a521bee8b063
name                           : Cert Publishers
distinguishedname              : CN=Cert Publishers,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Cert Publishers
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb}
cn                             : {Cert Publishers}
objectclass                    : {top, group}
usnchanged                     : 12344
description                    : Members of this group are permitted to publish certificates to the directory
instancetype                   : 4
usncreated                     : 12342
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-512}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 85d0d583-c900-4c38-ae76-8eb2f92cafbd
name                           : Domain Admins
distinguishedname              : CN=Domain Admins,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 10/27/2025 5:59:37 PM
samaccountname                 : Domain Admins
member                         : {CN=Administrator,CN=Users,DC=eighteen,DC=htb}
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb, CN=Administrators,CN=Builtin,DC=eighteen,DC=htb}
cn                             : {Domain Admins}
objectclass                    : {top, group}
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
usnchanged                     : 49215
description                    : Designated administrators of the domain
instancetype                   : 4
usncreated                     : 12345
admincount                     : 1
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-513}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 643dc754-bb2c-4876-a4bb-9ecd27391f59
name                           : Domain Users
distinguishedname              : CN=Domain Users,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Domain Users
memberof                       : {CN=Users,CN=Builtin,DC=eighteen,DC=htb}
cn                             : {Domain Users}
objectclass                    : {top, group}
usnchanged                     : 12350
description                    : All domain users
instancetype                   : 4
usncreated                     : 12348
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-514}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : b19394c6-997b-43b9-9ebe-b084b2804448
name                           : Domain Guests
distinguishedname              : CN=Domain Guests,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Domain Guests
memberof                       : {CN=Guests,CN=Builtin,DC=eighteen,DC=htb}
cn                             : {Domain Guests}
objectclass                    : {top, group}
usnchanged                     : 12353
description                    : All domain guests
instancetype                   : 4
usncreated                     : 12351
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-520}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 060290c2-40e9-437a-bd3e-a8ab99a2ca17
name                           : Group Policy Creator Owners
distinguishedname              : CN=Group Policy Creator Owners,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Group Policy Creator Owners
member                         : {CN=Administrator,CN=Users,DC=eighteen,DC=htb}
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb}
cn                             : {Group Policy Creator Owners}
objectclass                    : {top, group}
usnchanged                     : 12391
description                    : Members in this group can modify group policy for the domain
instancetype                   : 4
usncreated                     : 12354
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-553}
grouptype                      : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : bbd5a892-aaae-4d9f-bcf8-93c30872968c
name                           : RAS and IAS Servers
distinguishedname              : CN=RAS and IAS Servers,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : RAS and IAS Servers
cn                             : {RAS and IAS Servers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12359
instancetype                   : 4
usncreated                     : 12357
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Servers in this group can access remote access properties of users
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-549}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 812a8c02-73bf-4d52-b1db-4c25414726b8
name                           : Server Operators
distinguishedname              : CN=Server Operators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Server Operators
cn                             : {Server Operators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12797
instancetype                   : 4
usncreated                     : 12360
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
description                    : Members can administer domain servers
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-32-548}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 273c2101-e4de-45fe-80a4-da914f1a2a53
name                           : Account Operators
distinguishedname              : CN=Account Operators,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Account Operators
cn                             : {Account Operators}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12796
instancetype                   : 4
usncreated                     : 12363
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
description                    : Members can administer domain user and group accounts
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-32-554}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 6715ba33-5e3e-4d03-91a2-993dc5838802
name                           : Pre-Windows 2000 Compatible Access
distinguishedname              : CN=Pre-Windows 2000 Compatible Access,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Pre-Windows 2000 Compatible Access
member                         : {CN=S-1-5-11,CN=ForeignSecurityPrincipals,DC=eighteen,DC=htb}
cn                             : {Pre-Windows 2000 Compatible Access}
objectclass                    : {top, group}
usnchanged                     : 12393
description                    : A backward compatibility group which allows read access on all users and groups in the domain
instancetype                   : 4
usncreated                     : 12366
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-557}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 7af119d8-2832-47db-b433-400de1488198
name                           : Incoming Forest Trust Builders
distinguishedname              : CN=Incoming Forest Trust Builders,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Incoming Forest Trust Builders
cn                             : {Incoming Forest Trust Builders}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12371
instancetype                   : 4
usncreated                     : 12369
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group can create incoming, one-way trusts to this forest
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-560}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : c770503d-eff3-4403-8c18-533f710e3ade
name                           : Windows Authorization Access Group
distinguishedname              : CN=Windows Authorization Access Group,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Windows Authorization Access Group
member                         : {CN=S-1-5-9,CN=ForeignSecurityPrincipals,DC=eighteen,DC=htb}
cn                             : {Windows Authorization Access Group}
objectclass                    : {top, group}
usnchanged                     : 12396
description                    : Members of this group have access to the computed tokenGroupsGlobalAndUniversal attribute on User objects
instancetype                   : 4
usncreated                     : 12372
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-32-561}
grouptype                      : CREATED_BY_SYSTEM, DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : 390d83da-d7f7-4dfa-aee6-89532df001a1
name                           : Terminal Server License Servers
distinguishedname              : CN=Terminal Server License Servers,CN=Builtin,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Terminal Server License Servers
cn                             : {Terminal Server License Servers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12377
instancetype                   : 4
usncreated                     : 12375
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group can update user accounts in Active Directory with information about license issuance, for the purpose of tracking and reporting TS Per User CAL usage
systemflags                    : -1946157056
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-571}
grouptype                      : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : bd19b3e2-7dfd-4c82-83cc-d667b164eafc
name                           : Allowed RODC Password Replication Group
distinguishedname              : CN=Allowed RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Allowed RODC Password Replication Group
cn                             : {Allowed RODC Password Replication Group}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12404
instancetype                   : 4
usncreated                     : 12402
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members in this group can have their passwords replicated to all read-only domain controllers in the domain
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-572}
grouptype                      : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : ba6bb2cd-f9ba-46b6-a0c2-53fab5e037d1
name                           : Denied RODC Password Replication Group
distinguishedname              : CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Denied RODC Password Replication Group
member                         : {CN=Read-only Domain Controllers,CN=Users,DC=eighteen,DC=htb, CN=Group Policy Creator Owners,CN=Users,DC=eighteen,DC=htb, CN=Domain Admins,CN=Users,DC=eighteen,DC=htb, CN=Cert Publishers,CN=Users,DC=eighteen,DC=htb, CN=Enterprise Admins,CN=Users,DC=eighteen,DC=htb, CN=Schema Admins,CN=Users,DC=eighteen,DC=htb, CN=Domain Controllers,CN=Users,DC=eighteen,DC=htb, CN=krbtgt,CN=Users,DC=eighteen,DC=htb}
cn                             : {Denied RODC Password Replication Group}
objectclass                    : {top, group}
usnchanged                     : 12433
description                    : Members in this group cannot have their passwords replicated to any read-only domain controllers in the domain
instancetype                   : 4
usncreated                     : 12405
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-521}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : dcfd3d9a-cb56-41ed-a758-15db6614e6f9
name                           : Read-only Domain Controllers
distinguishedname              : CN=Read-only Domain Controllers,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Read-only Domain Controllers
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb}
cn                             : {Read-only Domain Controllers}
objectclass                    : {top, group}
usnchanged                     : 12808
description                    : Members of this group are Read-Only Domain Controllers in the domain
instancetype                   : 4
usncreated                     : 12419
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
iscriticalsystemobject         : True
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-498}
grouptype                      : UNIVERSAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 87433ac3-26fe-4108-9228-1995d35f99d2
name                           : Enterprise Read-only Domain Controllers
distinguishedname              : CN=Enterprise Read-only Domain Controllers,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Enterprise Read-only Domain Controllers
cn                             : {Enterprise Read-only Domain Controllers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12431
instancetype                   : 4
usncreated                     : 12429
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group are Read-Only Domain Controllers in the enterprise
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-522}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 97c4c1f1-5f8c-4190-be9d-b1ee9323aac6
name                           : Cloneable Domain Controllers
distinguishedname              : CN=Cloneable Domain Controllers,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Cloneable Domain Controllers
cn                             : {Cloneable Domain Controllers}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12442
instancetype                   : 4
usncreated                     : 12440
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group that are domain controllers may be cloned.
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-525}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : ca0b2a30-35a6-44ea-981a-5eb6f4f3de13
name                           : Protected Users
distinguishedname              : CN=Protected Users,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Protected Users
cn                             : {Protected Users}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12447
instancetype                   : 4
usncreated                     : 12445
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members of this group are afforded additional protections against authentication security threats. See http://go.microsoft.com/fwlink/?LinkId=298939 for more information.
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-526}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 06d1f3d1-95be-4270-bad8-817a11869fd1
name                           : Key Admins
distinguishedname              : CN=Key Admins,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Key Admins
cn                             : {Key Admins}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12795
instancetype                   : 4
usncreated                     : 12450
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
description                    : Members of this group can perform administrative actions on key objects within the domain.
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-527}
grouptype                      : UNIVERSAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : a8aac46a-0b54-461f-b28f-a98d9f32c7cd
name                           : Enterprise Key Admins
distinguishedname              : CN=Enterprise Key Admins,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : Enterprise Key Admins
cn                             : {Enterprise Key Admins}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12790
instancetype                   : 4
usncreated                     : 12453
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
admincount                     : 1
description                    : Members of this group can perform administrative actions on key objects within the forest.
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-528}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 9142440e-0351-4aec-8b78-274d9c0ec00b
name                           : Forest Trust Accounts
distinguishedname              : CN=Forest Trust Accounts,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : Forest Trust Accounts
cn                             : {Forest Trust Accounts}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12471
instancetype                   : 4
usncreated                     : 12469
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : All forest trust accounts in the forest.
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-529}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 64d358d9-986e-448c-a157-67fd30b23236
name                           : External Trust Accounts
distinguishedname              : CN=External Trust Accounts,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:39 AM
whenchanged                    : 9/11/2025 8:16:39 AM
samaccountname                 : External Trust Accounts
cn                             : {External Trust Accounts}
objectclass                    : {top, group}
iscriticalsystemobject         : True
usnchanged                     : 12474
instancetype                   : 4
usncreated                     : 12472
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : All external trust accounts in the domain.
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1101}
grouptype                      : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : fd119ca4-4833-43aa-b90c-8ee74544cc08
name                           : DnsAdmins
distinguishedname              : CN=DnsAdmins,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:17:18 AM
whenchanged                    : 9/11/2025 8:17:18 AM
samaccountname                 : DnsAdmins
cn                             : {DnsAdmins}
objectclass                    : {top, group}
usnchanged                     : 12499
instancetype                   : 4
usncreated                     : 12497
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : DNS Administrators Group
dscorepropagationdata          : 1/1/1601 12:00:00 AM

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1102}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : af3eb122-70ba-4660-bb33-c4c8bbe44ac9
name                           : DnsUpdateProxy
distinguishedname              : CN=DnsUpdateProxy,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:17:18 AM
whenchanged                    : 9/11/2025 8:17:18 AM
samaccountname                 : DnsUpdateProxy
cn                             : {DnsUpdateProxy}
objectclass                    : {top, group}
usnchanged                     : 12502
instancetype                   : 4
usncreated                     : 12502
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : DNS clients who are permitted to perform dynamic updates on behalf of some other clients (such as DHCP servers).
dscorepropagationdata          : 1/1/1601 12:00:00 AM

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1602}
grouptype                      : DOMAIN_LOCAL_SCOPE, SECURITY
samaccounttype                 : ALIAS_OBJECT
objectguid                     : b6f03bf6-bd40-42a4-93cb-e7c0ffbfae39
name                           : SQLServer2005SQLBrowserUser$DC01
distinguishedname              : CN=SQLServer2005SQLBrowserUser$DC01,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 8:30:00 AM
whenchanged                    : 9/12/2025 8:30:00 AM
samaccountname                 : SQLServer2005SQLBrowserUser$DC01
cn                             : {SQLServer2005SQLBrowserUser$DC01}
objectclass                    : {top, group}
usnchanged                     : 16446
instancetype                   : 4
usncreated                     : 16443
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Members in the group have the required access and privileges to be assigned as the log on account for the associated instance of SQL Server Browser.
dscorepropagationdata          : 1/1/1601 12:00:00 AM

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1603}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : c6b4db4c-3593-4028-a428-d0d475e3eb00
name                           : HR
distinguishedname              : CN=HR,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:30 AM
whenchanged                    : 9/12/2025 10:16:31 AM
samaccountname                 : HR
member                         : {CN=alice.jones,OU=Staff,DC=eighteen,DC=htb, CN=jane.smith,OU=Staff,DC=eighteen,DC=htb, CN=jamie.dunn,OU=Staff,DC=eighteen,DC=htb}
cn                             : {HR}
objectclass                    : {top, group}
usnchanged                     : 32836
instancetype                   : 4
usncreated                     : 32800
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1604}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 4c6e0707-6cd2-458f-b003-8fe8e289350a
name                           : IT
distinguishedname              : CN=IT,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:30 AM
whenchanged                    : 9/12/2025 10:16:31 AM
samaccountname                 : IT
member                         : {CN=bob.brown,OU=Staff,DC=eighteen,DC=htb, CN=adam.scott,OU=Staff,DC=eighteen,DC=htb}
memberof                       : {CN=Remote Management Users,CN=Builtin,DC=eighteen,DC=htb}
cn                             : {IT}
objectclass                    : {top, group}
usnchanged                     : 32854
instancetype                   : 4
usncreated                     : 32804
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1605}
grouptype                      : GLOBAL_SCOPE, SECURITY
samaccounttype                 : GROUP_OBJECT
objectguid                     : 96560d4a-fd5b-4c9e-ba63-c02450bb0f70
name                           : Finance
distinguishedname              : CN=Finance,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:31 AM
whenchanged                    : 9/12/2025 10:16:32 AM
samaccountname                 : Finance
member                         : {CN=dave.green,OU=Staff,DC=eighteen,DC=htb, CN=carol.white,OU=Staff,DC=eighteen,DC=htb}
cn                             : {Finance}
objectclass                    : {top, group}
usnchanged                     : 32872
instancetype                   : 4
usncreated                     : 32808
objectcategory                 : CN=Group,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}



sliver (LOVELY_BEEF) > sharpview Get-DomainUser

[*] sharpview output:
[Get-DomainSearcher] search base: LDAP://DC=eighteen,DC=htb
[Get-DomainUser] filter string: (&(samAccountType=805306368))
objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-500}
samaccounttype                 : USER_OBJECT
objectguid                     : 111a3da4-cbd8-49fd-a3fd-c973c51bbe2b
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : 12/31/1600 4:00:00 PM
lastlogon                      : 1/20/2026 3:24:42 AM
lastlogontimestamp             : 1/20/2026 12:53:00 AM
pwdlastset                     : 10/27/2025 10:58:18 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 11/6/2025 4:56:09 PM
name                           : Administrator
distinguishedname              : CN=Administrator,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 1/20/2026 8:53:00 AM
samaccountname                 : Administrator
memberof                       : {CN=Group Policy Creator Owners,CN=Users,DC=eighteen,DC=htb, CN=Domain Admins,CN=Users,DC=eighteen,DC=htb, CN=Enterprise Admins,CN=Users,DC=eighteen,DC=htb, CN=Schema Admins,CN=Users,DC=eighteen,DC=htb, CN=Administrators,CN=Builtin,DC=eighteen,DC=htb}
cn                             : {Administrator}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 314
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Built-in account for administering the computer/domain
usnchanged                     : 167993
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 8196
countrycode                    : 0
primarygroupid                 : 513
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 6:12:16 PM}
logonhours                     : {255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255}
admincount                     : 1
iscriticalsystemobject         : True

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-501}
samaccounttype                 : USER_OBJECT
objectguid                     : ef70386d-00f1-4cc7-8bae-1f13ebf5cd22
useraccountcontrol             : ACCOUNTDISABLE, PASSWD_NOTREQD, NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
pwdlastset                     : 12/31/1600 4:00:00 PM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : Guest
distinguishedname              : CN=Guest,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:15:59 AM
whenchanged                    : 9/11/2025 8:15:59 AM
samaccountname                 : Guest
memberof                       : {CN=Guests,CN=Builtin,DC=eighteen,DC=htb}
cn                             : {Guest}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Built-in account for guest access to the computer/domain
usnchanged                     : 8197
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 8197
countrycode                    : 0
primarygroupid                 : 514
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}
iscriticalsystemobject         : True

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-502}
samaccounttype                 : USER_OBJECT
objectguid                     : 80c9ab1a-e23f-41dd-8acd-63fa226a730c
useraccountcontrol             : ACCOUNTDISABLE, NORMAL_ACCOUNT
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
pwdlastset                     : 9/11/2025 1:16:38 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : krbtgt
distinguishedname              : CN=krbtgt,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:38 AM
whenchanged                    : 9/11/2025 8:31:48 AM
samaccountname                 : krbtgt
memberof                       : {CN=Denied RODC Password Replication Group,CN=Users,DC=eighteen,DC=htb}
cn                             : {krbtgt}
objectclass                    : {top, person, organizationalPerson, user}
ServicePrincipalName           : kadmin/changepw
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
description                    : Key Distribution Center Service Account
usnchanged                     : 12806
instancetype                   : 4
showinadvancedviewonly         : True
badpwdcount                    : 0
usncreated                     : 12324
countrycode                    : 0
primarygroupid                 : 513
dscorepropagationdata          : {9/11/2025 8:31:48 AM, 9/11/2025 8:16:39 AM, 1/1/1601 12:04:16 AM}
msds-supportedencryptiontypes  : 0
admincount                     : 1
iscriticalsystemobject         : True

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1601}
samaccounttype                 : USER_OBJECT
objectguid                     : fb510665-a923-4566-98ad-30cc5b726cad
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 1/20/2026 12:54:21 AM
lastlogontimestamp             : 1/20/2026 12:54:21 AM
pwdlastset                     : 9/13/2025 2:54:06 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 10/27/2025 6:03:46 PM
name                           : mssqlsvc
distinguishedname              : CN=mssqlsvc,CN=Users,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 8:20:36 AM
whenchanged                    : 1/20/2026 8:54:21 AM
samaccountname                 : mssqlsvc
cn                             : {mssqlsvc}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 109
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
usnchanged                     : 168022
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 16409
dscorepropagationdata          : 1/1/1601 12:00:00 AM
countrycode                    : 0
primarygroupid                 : 513

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1606}
samaccounttype                 : USER_OBJECT
objectguid                     : 876baebc-742e-4f76-a7ff-1b4c71e67c73
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
pwdlastset                     : 9/12/2025 3:16:31 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : jamie.dunn
distinguishedname              : CN=jamie.dunn,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:31 AM
whenchanged                    : 9/12/2025 10:27:37 AM
samaccountname                 : jamie.dunn
memberof                       : {CN=HR,OU=Staff,DC=eighteen,DC=htb}
cn                             : {jamie.dunn}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}
usnchanged                     : 32882
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 32812
countrycode                    : 0
primarygroupid                 : 513
userprincipalname              : jamie.dunn@eighteen.htb

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1607}
samaccounttype                 : USER_OBJECT
objectguid                     : 55644c11-81b9-4717-aca9-5f19f1b87cc7
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
pwdlastset                     : 9/12/2025 3:16:31 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : jane.smith
distinguishedname              : CN=jane.smith,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:31 AM
whenchanged                    : 9/12/2025 10:16:31 AM
samaccountname                 : jane.smith
memberof                       : {CN=HR,OU=Staff,DC=eighteen,DC=htb}
cn                             : {jane.smith}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}
usnchanged                     : 32825
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 32821
countrycode                    : 0
primarygroupid                 : 513
userprincipalname              : jane.smith@eighteen.htb

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1608}
samaccounttype                 : USER_OBJECT
objectguid                     : 5d37fd8d-9f2c-4a81-9814-fdb950d80fe1
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
pwdlastset                     : 9/12/2025 3:16:31 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : alice.jones
distinguishedname              : CN=alice.jones,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:31 AM
whenchanged                    : 9/12/2025 10:16:31 AM
samaccountname                 : alice.jones
memberof                       : {CN=HR,OU=Staff,DC=eighteen,DC=htb}
cn                             : {alice.jones}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}
usnchanged                     : 32834
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 32830
countrycode                    : 0
primarygroupid                 : 513
userprincipalname              : alice.jones@eighteen.htb

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1609}
samaccounttype                 : USER_OBJECT
objectguid                     : 24666d54-7f68-4311-a007-a73a04ba2386
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 10/27/2025 12:55:28 PM
lastlogontimestamp             : 1/20/2026 2:42:21 AM
pwdlastset                     : 10/29/2025 5:42:11 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 9/13/2025 1:08:51 AM
name                           : adam.scott
distinguishedname              : CN=adam.scott,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:31 AM
whenchanged                    : 1/20/2026 10:42:21 AM
samaccountname                 : adam.scott
memberof                       : {CN=IT,OU=Staff,DC=eighteen,DC=htb}
cn                             : {adam.scott}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 9
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}
usnchanged                     : 168065
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 32839
countrycode                    : 0
primarygroupid                 : 513
userprincipalname              : adam.scott@eighteen.htb

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1610}
samaccounttype                 : USER_OBJECT
objectguid                     : f70f2db2-c24e-4fe7-9e15-a38c64c8a156
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
lastlogontimestamp             : 9/12/2025 3:31:09 AM
pwdlastset                     : 9/12/2025 3:16:31 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : bob.brown
distinguishedname              : CN=bob.brown,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:31 AM
whenchanged                    : 9/12/2025 10:31:09 AM
samaccountname                 : bob.brown
memberof                       : {CN=IT,OU=Staff,DC=eighteen,DC=htb}
cn                             : {bob.brown}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}
usnchanged                     : 32883
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 32848
countrycode                    : 0
primarygroupid                 : 513
userprincipalname              : bob.brown@eighteen.htb

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1611}
samaccounttype                 : USER_OBJECT
objectguid                     : e80eab64-4740-426d-8205-d8cbdd7591b9
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
lastlogontimestamp             : 9/12/2025 3:34:46 AM
pwdlastset                     : 9/12/2025 3:16:31 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : carol.white
distinguishedname              : CN=carol.white,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:31 AM
whenchanged                    : 9/12/2025 10:34:46 AM
samaccountname                 : carol.white
memberof                       : {CN=Finance,OU=Staff,DC=eighteen,DC=htb}
cn                             : {carol.white}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}
usnchanged                     : 32884
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 32857
countrycode                    : 0
primarygroupid                 : 513
userprincipalname              : carol.white@eighteen.htb

objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1612}
samaccounttype                 : USER_OBJECT
objectguid                     : e2815072-7a77-4499-b90b-3210e0879f67
useraccountcontrol             : NORMAL_ACCOUNT, DONT_EXPIRE_PASSWORD
accountexpires                 : NEVER
lastlogon                      : 12/31/1600 4:00:00 PM
pwdlastset                     : 9/12/2025 3:16:32 AM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : dave.green
distinguishedname              : CN=dave.green,OU=Staff,DC=eighteen,DC=htb
whencreated                    : 9/12/2025 10:16:32 AM
whenchanged                    : 9/12/2025 10:16:32 AM
samaccountname                 : dave.green
memberof                       : {CN=Finance,OU=Staff,DC=eighteen,DC=htb}
cn                             : {dave.green}
objectclass                    : {top, person, organizationalPerson, user}
logoncount                     : 0
codepage                       : 0
objectcategory                 : CN=Person,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
dscorepropagationdata          : {9/12/2025 10:37:16 AM, 1/1/1601 12:00:00 AM}
usnchanged                     : 32870
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 32866
countrycode                    : 0
primarygroupid                 : 513
userprincipalname              : dave.green@eighteen.htb



sliver (LOVELY_BEEF) > sharpview Get-DomainComputer

[*] sharpview output:
[Get-DomainSearcher] search base: LDAP://DC=eighteen,DC=htb
[Get-DomainComputer] Get-DomainComputer filter string: (&(samAccountType=805306369))
objectsid                      : {S-1-5-21-1152179935-589108180-1989892463-1000}
samaccounttype                 : MACHINE_ACCOUNT
objectguid                     : ae22be1e-6b77-4291-99e5-99d6c0bd1e7e
useraccountcontrol             : SERVER_TRUST_ACCOUNT, TRUSTED_FOR_DELEGATION
accountexpires                 : NEVER
lastlogon                      : 1/20/2026 12:52:51 AM
lastlogontimestamp             : 1/20/2026 12:52:47 AM
pwdlastset                     : 10/27/2025 1:10:26 PM
lastlogoff                     : 12/31/1600 4:00:00 PM
badPasswordTime                : 12/31/1600 4:00:00 PM
name                           : DC01
distinguishedname              : CN=DC01,OU=Domain Controllers,DC=eighteen,DC=htb
whencreated                    : 9/11/2025 8:16:38 AM
whenchanged                    : 1/20/2026 8:52:47 AM
samaccountname                 : DC01$
cn                             : {DC01}
objectclass                    : {top, person, organizationalPerson, user, computer}
ServicePrincipalName           : Dfsr-12F9A27C-BF97-4787-9364-D31B6C55EB04/DC01.eighteen.htb
dnshostname                    : DC01.eighteen.htb
ridsetreferences               : CN=RID Set,CN=DC01,OU=Domain Controllers,DC=eighteen,DC=htb
logoncount                     : 94
codepage                       : 0
objectcategory                 : CN=Computer,CN=Schema,CN=Configuration,DC=eighteen,DC=htb
msdfsr-computerreferencebl     : CN=DC01,CN=Topology,CN=Domain System Volume,CN=DFSR-GlobalSettings,CN=System,DC=eighteen,DC=htb
iscriticalsystemobject         : True
operatingsystem                : Windows Server 2025 Datacenter
usnchanged                     : 167987
instancetype                   : 4
badpwdcount                    : 0
usncreated                     : 12293
msds-generationid              : {79, 232, 79, 122, 81, 49, 164, 139}
localpolicyflags               : 0
countrycode                    : 0
primarygroupid                 : 516
operatingsystemversion         : 10.0 (26100)
dscorepropagationdata          : {9/11/2025 8:16:39 AM, 1/1/1601 12:00:01 AM}
msds-supportedencryptiontypes  : 28
serverreferencebl              : CN=DC01,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=eighteen,DC=htb
# Exploit

# Questions

# Further Improvements
