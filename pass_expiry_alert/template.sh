###########################################################################
#Name : template.sh	                          	                          #
#Version : 1.0                                                            #
#Description : Create a HTML file with server name & Expiry date          #
#Author : Sunil Narhe                                                     #
#Author Email : s.narhe@yahoo.in		                                  #
#URL :                                                                    #
#                                                                         #
#Requirement :                                                            #
#    1. Bash                                                              #
#    2. Input parameter as Server Name                                    #
#    3. Input parameter as Expiry Date                                    #
#                                                                         #
#Usage : sh template.sh Server1 'Dec 15, 2020'                            #
#                                                                         #
#Initial Draft : 9th Sep 2020                                             #
###########################################################################

#!/bin/bash

#HTML formation
HTML_Header="<html>
<head>
<style>
body { background-color:#E5E4E2;
        font-family:"sans-serif";
        font-size:10pt; }
td, th { border:0px solid black;
         border-collapse:collapse;
         white-space:pre; }
th { color:black;
     background-color:lightblue; }
table, tr, td, th { padding: 2px; margin: 0px ;white-space:pre; }
tr:nth-child(odd) {background-color: lightgray}
table { width:25%;margin-left:5px; margin-bottom:20px;}
</style>
</head>

<body>
    <p>Dear User,<br /> <br />Your password for below server will expire soon.<br />
        <table><tr><th>Server</th> <th>Expire On</th></tr>
"
Values="<tr><td>$1</td><td>$2</td></tr>"

HTML_END="</table>
<p>Please reset yor password before it expires.<br/>If you have any difuculties to do, please contact server team.</p>
<p><br/><br/> <br />
Regards,<br/>
Unix Team.<br/>
Email: ITServicesServerTeam@locahost.com</p>
</body>
</html>
"
echo $HTML_Header > server.html
echo $Values >> server.html
echo $HTML_END >> server.html
