"""
Name : monitoring_file_input.py
Version : 1.0
Description : Monitor Linux servers CPU, Memory, Disk, Yum Logs and Failed Logins
Author : Sunil Narhe
Author Email : s.narhe@yahoo.in
URL :

Requirement :
    1. Python 3.6
    2. pip 3
    3. paramiko, smtplib

Usage : python monitoring.py -f server_list.txt

Sub script: graph_memory.py (To generate graph images for Memory
"""

#!/usr/bin/python
import argparse
import paramiko
from time import strftime
import os
import smtplib
from csv import writer

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

USER = 'root'
PORT = 22
Log_Date = strftime("%b %d")
DT = strftime("%Y_%m_%d_%H_%M")
FileName = "monitoring_{}.html".format(DT)
strTo = "sunil.narhe@virtumentor.in"
strFrom = "root@root.com"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--inputfile', help='Input FileName which contain Host Name/IP per line', required=True)
    arguments = parser.parse_args()
    InputFile = arguments.inputfile
    return InputFile

InputFile = get_args()

def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

HTML_Header = """<html>
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
table { width:100%;margin-left:5px; margin-bottom:20px;}
</style>
</head>

<body>
    <p>Hello Team,<br /> <br />Please find below monitoring details:
        <table><tr><th>Hostname</th> <th>Total Mem</th>
        <th>User Mem</th> <th>Free Mem</th> <th>Cache Mem</th><th>Current Load</th><th>Disk</th> <th>Failed_Login</th><th>Yum Log</th></tr>
"""
HTML_END = """</table>
<p><br/><h4>Note:</h4>1. Memory measure in MB<br/>2. Disk threshold is 80% (NA means no Alert)</p>
<p><br/><br/> <br />
Regards,<br/>
Unix Team.<br/>
Email: Sunil Narhe</p>
</body>
</html>
"""
with open(FileName, 'w') as f:
    f.writelines(HTML_Header)
    HOSTS = open(InputFile)
    for Host in HOSTS:
        try:
            key = paramiko.RSAKey.from_private_key_file("/root/.ssh/id_rsa")
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=Host,port=PORT,username=USER,pkey=key)
            stdin, stdout, stderr = ssh.exec_command("uname -r | awk -F'.' '{print $(NF-1)}'")
            OSVersion = stdout.readlines()[0].rstrip()
            stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem | awk '{print $2}'")
            TotalMem = stdout.read().decode("utf-8")
            stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem | awk '{print $3}'")
            UsedMem = stdout.read().decode("utf-8")
            stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem | awk '{print $4}'")
            FreeMem = stdout.read().decode("utf-8")
            if OSVersion == "el7":
                stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem | awk '{print $6}'")
                CacheMem = stdout.read().decode("utf-8")
            elif OSVersion == "el6":
                stdin, stdout, stderr = ssh.exec_command("free -m | grep Mem | awk '{print $7}'")
                CacheMem = stdout.read().decode("utf-8")
            stdin, stdout, stderr = ssh.exec_command("df -h | awk '$5 >= 80 {print $6','$5}' | grep -v Mount")
            HighDisks = stdout.read().decode("utf-8")
            stdin, stdout, sdterr = ssh.exec_command("dmidecode -t processor | grep -c Count")
            CoreCount = stdout.read().decode("utf-8")
            stdin, stdout, stderr = ssh.exec_command("w | grep load | awk -F',' '{print $4}' | awk '{print $NF}'")
            CurrentLoad = stdout.read().decode("utf-8")
            stdin, stdout, stderr = ssh.exec_command("cat /var/log/secure | grep -E '{}.*Failed password' | cut -d' ' -f9,-f11 | sort -u".format(Log_Date))
            Failed_Login = stdout.read().decode("utf-8")
            stdin, stdout, stderr = ssh.exec_command("ls -lrth /var/log/yum.log | awk '{print $5}'")
            YumSize = stdout.read().decode("utf-8")
            if int(YumSize) > 0:
                stdin, stdout, stderr = ssh.exec_command("cat /var/log/yum.log | grep '{}' | grep Installed | cut -d' ' -f5".format(Log_Date))
                YumInstalled = stdout.read().decode("utf-8")
                stdin, stdout, stderr = ssh.exec_command("cat /var/log/yum.log | grep '{}' | grep Updated | cut -d' ' -f5".format(Log_Date))
                YumUpdated = stdout.read().decode("utf-8")
                stdin, stdout, stderr = ssh.exec_command("cat /var/log/yum.log | grep '{}' | grep Erased | cut -d' ' -f5".format(Log_Date))
                YumErased = stdout.read().decode("utf-8")
                YumLog = 1
            else:
                YumLog = 0
            stdin, stdout, stderr = ssh.exec_command("cat /var/log/messages  | grep '{}' | grep -i '^warning\|error\|fail\|bug\|stop\|start' | grep -iv 'syslogd * restart.' | grep -iv 'mount debugfs at /sys/kernel/debug' | grep -v 'failed fips test'".format(Log_Date))
            SysLog = stdout.read().decode("utf-8")
            f.write("<tr><td> {} </td>".format(Host))
            f.write("<td> {} </td>".format(TotalMem))
            f.write("<td> {} </td>".format(UsedMem))
            f.write("<td> {} </td>".format(FreeMem))
            f.write("<td> {} </td>".format(CacheMem))
            if CurrentLoad > CoreCount:
                f.write('<td bgcolor="#FF0000"> {} </td>'.format(CurrentLoad))
            else:
                f.write("<td> {} </td>".format(CurrentLoad))
            if HighDisks:
                f.write("<td> {} </td>".format(HighDisks))
            else:
                f.write("<td>NA</td>".format(HighDisks))
            if Failed_Login:
                f.write('<td bgcolor="#FF0000"> {} </td>'.format(Failed_Login))
            else:
                f.write("<td>NA</td>")
            if YumLog == 1:
                if YumInstalled and YumUpdated and YumErased is not None:
                    f.write("<td>Installed:<br>{}<br>Updated:<br>{}<br>Erased:<br>{}</td>".format(YumInstalled, YumUpdated, YumErased))
                else:
                    f.write("<td>NA</td>")
            else:
                f.write("<td>NA</td>")
            f.write("</tr>")
            PerUsedMem = '%.2f' % float(float(UsedMem) / float(TotalMem) * 100)
            if OSVersion == "el7":
                PerFreeMem = '%.2f' % (float(float(FreeMem) + float(CacheMem)) / float(TotalMem) * 100)
            elif OSVersion == "el6":
                PerFreeMem = '%.2f' % float(float(FreeMem) / float(TotalMem) * 100)
            UsedMemGraph = [Host, PerUsedMem]
            FreeMemGraph = [Host, PerFreeMem]
            append_list_as_row('Used_Memory_Graph.csv', UsedMemGraph)
            append_list_as_row('Free_Memory_Graph.csv', FreeMemGraph)
        except paramiko.AuthenticationException as error:
            print ("{} Authentication failed".format(Host))
    f.write("</table>")
Heading_Used = os.system("sed -i '1i HostName,Memory' Used_Memory_Graph.csv")
Heading_Free = os.system("sed -i '1i HostName,Memory' Free_Memory_Graph.csv")
used_mem_graph_plot = os.system("python3 graph_memory.py -ifile Used_Memory_Graph.csv -p used")
free_mem_graph_plot = os.system("python3 graph_memory.py -ifile Free_Memory_Graph.csv -p free")
RemoveUsedMem = os.system("rm -rf Used_Memory_Graph.csv")
RemoveUsedMem = os.system("rm -rf Free_Memory_Graph.csv")

#Message_body before image
with open(FileName, 'r') as fmb:
    MessBody = fmb.read()

body = '{} <p><br/><img src="cid:image1"><img src="cid:image2"></p> {}'.format(MessBody,HTML_END)

with open(FileName, 'w') as fileEnd:
    fileEnd.writelines(HTML_END)

with open(FileName, 'r') as file:
    EmailBody = file.read()

EmailMessage = """from: Root <root@dc1-lnxmgmt01.allscripts.lan>
To: {}
MIME-Version: 1.0
Content-type: text/html
Subject: Linux Monitoring

{}""".format(strTo, EmailBody)

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'Linux Monitoring'
msgRoot['From'] = strFrom
msgRoot['To'] = strTo
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText(body, 'html')
msgAlternative.attach(msgText)

# This example assumes the image is in the current directory
fp1 = open('free_mem.png', 'rb')
msgImage1 = MIMEImage(fp1.read())
fp1.close()

fp2 = open('used_mem.png', 'rb')
msgImage2 = MIMEImage(fp2.read())
fp2.close()

# Define the image's ID as referenced above
msgImage1.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage1)

msgImage2.add_header('Content-ID', '<image2>')
msgRoot.attach(msgImage2)

# Send the email (this example assumes SMTP authentication is required)
import smtplib
smtp = smtplib.SMTP()
smtp.connect('localhost')
smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.quit()

