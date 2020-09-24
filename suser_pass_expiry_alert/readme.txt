Welcome to Password expiry alert !

This tool help System Admin to get email alert when
user login password is about to expire within
15 Days (You can change days to get alert).
OR already expired

Required Software:
1. Bash (4.2.46) and above
2. Python 3.6.9
3. Postfix 2.10.1

(Testing done in above mention versions)

Installation:
Untar the file under /home/<user> directory

e.g. $ tar zxf suser_pass_expiry.tgz

Or Copy all files from GitHub


Conguration:
1. input/serverlist -> server name/IP on each line
2. python/emessage.py -> EmailTo, EmailFrom parameter
3. shell/pass_expiry_alert.sh -> Script file location
   in 'cd' command

Pre-rquisite:
1. SSH Password less authentication to all servers
   mentioned in 'serverlist' file
2. Vanila Postfix running on locahost

Execution:
A] Manual:
   $ sh shell/pass_expiry_alert.sh

B] Cron Job:
   Below cron job entry will execute script every 
   Sunday for mentioned servers

   0 1 * * sun /bin/sh /home/snarhe/suser_pass_expiry/pass_expiry_alert.sh

Output:
Email received for indivisual server.

#EOF

