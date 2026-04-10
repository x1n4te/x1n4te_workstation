12/11/25 | 10:13 AM - 11:32 AM
[[THM]] [[SIEM]]
#completed 
https://10-49-149-208.reverse-proxy.cell-prod-ap-south-1b.vm.tryhackme.com/

Same as the previous room, i will not provide Phases and Instructions.

This is more on the usage of "Splunk" which is a SIEM, it monitors data from networking devices or devices in general. This is useful as an IT, since this would make your workflow easier. This is because you can visualize attacks or devices who are creating events specified from your rulebook. Mostly, SOC Analysts use these type of tools.

The instance in the room is Splunk Enterprise running via a reverse proxy in the ip address 10.49.149.208. There is four current apps installed in the dashboard, which are Search and Reporting, Python Upgrade Readiness App, Splunk Essentials for Cloud and Enterprise 8.2, Splunk Secure Gateway. In the room we are going to be using the search and reporting to filter through events to find anomalies or threats in the logs.

There are two datasets from the sourcetype, one is web_traffic and the other is firewall_logs. The firewall logs shows the traffic being allowed or block, while the web_traffic is the connection between the user and web server.

The room prompts us to do our initial triage, initial triage is trying to find a threat from an ocean of data, so we need to prioritize issues we find and classify them based on their severity. This is also done in SOCs and Incident Response Teams (IRT).

Lets filter through the sourcetype and find anomalies, when the first event in the logs load when we filter through the web_traffic we already see the first attack that was done. There was a webshell runner that was ran in our web server. There is also an sqlmap that attacks using SQLi. 

But we need to visualize first every event that has happened and check for trends and anomalies. After visualizing and finding that October 10 - October 14, there was a spike of web_traffic. Knowing this information we should continue to crack down on the anomalies.

Splunk has a bar in the right with interesting fields that might help you find anomalies, in our case we check the user_agent and find that automated SQL Injection, sqlmap, and webshell runner was one of the user_agents. There is also wget, curl, and zgrab, these are tools that attackers use that they can manipulate their cookies to mask their identity. Next one is the client_ip, which is not diverse there was a thousand events created by 198.51.100.55 eating up 51.434% of the results. Lastly is the path, lets see if someone used path traversal or IDOR or any attacks using the directory. We can see there are attacks which uses SQLi in our web fields, two time-based blind SQLi attacks one using the search.php function and the other item.php function.

With the current information we saw on the sourcetype, most of the user_agent consists of mozilla, chrome, safari and firefox. by filtering these logs out, we can check if there are weird logs from non-standard user_agents.

```
index=main sourcetype=web_traffic user_agent!=*Mozilla* user_agent!=*Chrome* user_agent!=*Safari* user_agent!=*Firefox*

sourcetype=web_traffic user_agent!=*Mozilla* user_agent!=*Chrome* user_agent!=*Safari* user_agent!=*Firefox* | stats count by client_ip | sort -count | head 5

sourcetype=web_traffic client_ip="198.51.100.55" AND path IN ("/.env", "/*phpinfo*", "/.git*") | table _time, path, user_agent, status

sourcetype=web_traffic client_ip="198.51.100.55" AND path="*..*" OR path="*redirect*"

sourcetype=web_traffic client_ip="198.51.100.55" AND path="*..\/..\/*" OR path="*redirect*" | stats count by path

sourcetype=web_traffic client_ip="198.51.100.55" AND user_agent IN ("*sqlmap*", "*Havij*") | table _time, path, status

sourcetype=web_traffic client_ip="198.51.100.55" AND path IN ("*backup.zip*", "*logs.tar.gz*") | table _time path, user_agent

sourcetype=web_traffic client_ip="198.51.100.55" AND path IN ("*bunnylock.bin*", "*shell.php?cmd=*") | table _time, path, user_agent, status

sourcetype=firewall_logs src_ip="10.10.1.5" AND dest_ip="198.51.100.55" AND action="ALLOWED" | table _time, action, protocol, src_ip, dest_ip, dest_port, reason

sourcetype=firewall_logs src_ip="10.10.1.5" AND dest_ip="198.51.100.55" AND action="ALLOWED" | stats sum(bytes_transferred) by src_ip
```

tbc -- tinamad ako huhu