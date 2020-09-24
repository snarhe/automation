"""
Name : emessage.py
Version : 1.0
Description : Sent email to sender with provided HTML template
Author : Sunil Narhe
Author Email : s.narhe@yahoo.in
URL :

Requirement :
    1. Python 3.6
    2. pip 3
    3. smtplib

Usage : python emessage.py

"""

import smtplib

FileName = '/home/snarhe/suser_pass_expiry_alert/html/server.html'
EmailTo = "s.narhe@yahoo.in"
EmailFrom = "root@server.domain.lan"

with open(FileName, 'r') as file:
    EmailBody = file.read()

EmailMessage = """from: Root <root@server.domain.lan>
To: {}
MIME-Version: 1.0
Content-type: text/html
Subject: Action Required: Password Change Required

{}""".format(EmailTo, EmailBody)

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(EmailFrom, EmailTo, EmailMessage)
#   print ("Successfully sent email")
except SMTPException:
   print ("Error: unable to send email")

