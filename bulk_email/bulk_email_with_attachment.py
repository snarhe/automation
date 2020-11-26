"""
Name : bulk_email_with_attachment.py
Version : 1.0
Description : Sent bulk email from your gmail account with one attachment
Author : Sunil Narhe
Author Email : virtumentor@gmail.com
URL :
Requirement :
    1. Python 3.6
    2. pip 3
    3. paramiko, smtplib

Usage : python bulk_email.py -f sender.csv

Example of sender.csv (First line/Heading of file mandatory "DO NOT CHANGE OR REPLACE")
Recipient,FileName
s.narhe@yahoo.in,intro.pdf
virtumentor@gmail.com,card.pdf

"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from smtplib import SMTP
import argparse
import csv
import time

# You Gmail credential which used to send email
strFrom = 'virtumentor@gmail.com'
strPass = '***********'

#Email Subject
strSubject = "Greeting from VirtuMentor"

#Email Content
strMessage = """Welcome to VirtuMentor!!

Thank you for contacting us.

Latest Technologies

Now a days, technologies are changing drastically. We ensure the latest and upcoming technologies to be a part of our syllabus.

Mentor based Courses

Learning without a teacher like reading a book without understanding. We provide only Mentor based courses to have better understanding of knowledge.

For inquiry or more details WhatsApp
https://wa.me/message/YXAIWEERBSVLA1

For Free Courses
Subscribe to our Channel:

https://youtube.com/channel/UCeP9ldQqg1-Bo14yj84sAHg

Learning Today, Leading Tomorrow

Regards,
VirtuMentor
"""

#SMTP Details
GSMTP = "smtp.gmail.com:587"

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--inputfile', help='Input File which have Recipient and FileName with comma(,) separated', required=True)
    arguments = parser.parse_args()
    InputFile = arguments.inputfile
    return InputFile

InputFile = get_args()

def FileAttach(AttachFile):
    with open(AttachFile, 'rb') as opened:
        openedfile = opened.read()
        attachedfile = MIMEApplication(openedfile, _subtype = "pdf", _encoder = encode_base64)
        attachedfile.add_header('content-disposition', 'attachment', filename = attachfile)
        msgRoot.attach(attachedfile)

with open(InputFile) as file:
    reader = csv.DictReader(file)
    for row in reader:
        email = row['Recipient']
        attachfile = row['FileName']
        try:
            server = SMTP(GSMTP)
            server.ehlo()
            server.starttls()
            server.login(strFrom, strPass)
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = strSubject
            msgRoot['From'] = strFrom
            msgRoot.preamble = 'This is a multi-part message in MIME format.'
            msgtext = MIMEText(strMessage)
            msgRoot.attach(msgtext)
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)
            msgText = MIMEText('There is an issue to attach file.')
            msgAlternative.attach(msgText)
            FileAttach(attachfile)
            time.sleep(10)
            server.sendmail(msgRoot['From'], email, msgRoot.as_string())
            print(f'Email sent to {email}')
        except:
            print(f'Error: Issue sending email to {email}')
        server.quit()
