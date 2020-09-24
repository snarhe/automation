###########################################################################
#Name : html_template.sh                                                  #
#Version : 1.0                                                            #
#Description : Create a HTML file with server name,			  #
#              User name  & Expiry date         			  #
#Author : Sunil Narhe                                                     #
#Author Email : s.narhe@yahoo.in                                #
#URL :                                                                    #
#                                                                         #
#Requirement :                                                            #
#    1. Bash                                                              #
#    2. Input file as partial html report                                 #
#                                                                         #
#Usage : sh template.sh html_part_$server.html                            #
#                                                                         #
#Initial Draft : 24th Sep 2020                                            #
###########################################################################

#!/bin/bash

SCRIPT_PATH="/home/snarhe/suser_pass_expiry_alert"

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
table { width:50%;margin-left:5px; margin-bottom:20px;}
</style>
</head>

<body>
    <p>Dear System Admin,<br /> <br />Below user's password expired or will expire soon.<br />
        <table><tr><th>Server</th> <th>User Name</th> <th>Expire On</th></tr>
"
Values=`cat $1`

HTML_END="</table>
<p>Please connect to respective user's.<br/>If you have any difuculties to do, please contact server team.</p>
<p><br/><br/> <br />
Regards,<br/>
Unix Team.<br/>
Email: ITServicesServerTeam@allscripts.com</p>
</body>
</html>
"
echo $HTML_Header > $SCRIPT_PATH/html/server.html
echo $Values >> $SCRIPT_PATH/html/server.html
echo $HTML_END >> $SCRIPT_PATH/html/server.html
