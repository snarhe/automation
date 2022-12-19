#!/usr/bin/python3

"""

Email Setting:
1. This script required changes to in Email Server, Email, Email Subject


Alert Setting:
To get transaction alert Telegram Bot is used.
Create a bot in telegram using BotFather
Get API token from Telegram
Add bot in group with people you want to share transaction alert
Send "Hi" message in group to get chat id
https://api.telegram.org/bot<YourBOTToken>/getUpdates

Get chat Id from above json response

Update apiToken and chatID 

Execution:
To get alert, scrip need to schedule in CRON job for every 5 mins
*/5 * * * * /usr/bin/python3 /home/snarhe/credit_transaction_telegram_alert.py

Install Required Packages:
1. Python 3
2. pip install html5lib
3. pip install bs4
4. pip install requests


LICENSE:
Free to use

Disclaimer:
1. Email address and API password stored in plain text format
2. Telegram API Token stored in plain text format

For security reasons storing password and critical details in plain
text format not recommended.

You can store critical info in OS ENV, which required additional changes in script.


"""

import imaplib
import sys
import email
from email.header import decode_header
import os
from bs4 import BeautifulSoup
import requests
import datetime


# IMAP4 server
# IMAP_server = "imap.gmail.com"  # gmail IMAP server
IMAP_server = "imap.mail.yahoo.com"  # Yahoo IMAP server
mail_id = "s.narhe@yahoo.in"      # Email Address which you want to connect
pwd = '***************' # Application password generated from Mail
NoOfEmail = 2  # Number of email fetch at each execution


def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)


""" 

"""

def send_to_telegram(message):

    apiToken = '******************************'
    chatID = '****************'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        # print(response.text)
    except Exception as e:
        print(e)


def get_recent_alert(StMonth,SDate,SYear,STime,message):
    DateTime = '{} {} {} {}'.format(StMonth,SDate,SYear,STime)
    format = '%b %d %Y %H:%M:%S'
    current_time = datetime.datetime.now().replace(microsecond=0)
    pre_five_minute = current_time - datetime.timedelta(minutes=5)
    datetime_str = datetime.datetime.strptime(DateTime, format)
    if pre_five_minute < datetime_str:
        send_to_telegram(message)
    else:
        pass


# Get the data in Table format 
# SpentAmt,SpentMonth,SpentDate,SpentYear,SpentTime,SpentInfo,AvailableCredit,TotalCredit
def web_scrap(filepath):
    HTMLFileToBeOpened = open(filepath, "r")
    # Reading the file and storing in a variable
    contents = HTMLFileToBeOpened.read()
    # Creating a BeautifulSoup object and 
    # specifying the parser
    soup = BeautifulSoup(contents, 'html5lib')
    table = str(soup.select('[style*="text-align:justify;"]'))
    td_data = table.split("<br/>")
    for lines in td_data:
        if 'Info:' in lines:
            # Below message is expecting in your email alert
            data1 = lines.replace('Your ABC Bank Credit Card XXXXXX has been used for a transaction of Rs ', '').strip()
            data1 = lines.replace('Your ABC Bank Credit Card XXXXXX has been used for a transaction of INR ', '').strip()
            AllData = data1.split()
            AllData.remove("on")
            AllData.remove("Info:")
            AllData.remove("at")
            SpentAmt = AllData[0]
            SpentMonth = AllData[1]
            SpentDate = AllData[2].replace(',','')
            SpentYear = AllData[3].replace(';','')
            SpentTime = AllData[4].replace('.','')
            SpentInfo = " ".join(AllData[5:])
            SpentInfo = SpentInfo.rstrip(SpentInfo[-1])
        
    for lines in td_data:
        if 'Available Credit Limit' in lines:
            data2 = lines.strip().split("<p>")
            AllData = data2[0].replace('The Available Credit Limit on your card is Rs ', '').split()
            AvailableCredit = AllData[0].replace(',','')
            TotalCredit = AllData[-1].replace(',','')
            TotalCredit = TotalCredit.rstrip(TotalCredit[-1])
    #print("Scraped Data=+++++",SpentAmt,SpentMonth,SpentDate,SpentYear,SpentTime,SpentInfo,AvailableCredit,TotalCredit)    
    return SpentAmt,SpentMonth,SpentDate,SpentYear,SpentTime,SpentInfo,AvailableCredit,TotalCredit


if __name__ == "__main__":
    # Instantiate IMAP4 interface
    imap = imaplib.IMAP4_SSL(IMAP_server)
    # login to the server
    try:
        status, summary = imap.login(mail_id, pwd)
        if status == "OK":
            pass
    except imaplib.IMAP4.error:
        print("Error logging into Mail")
        sys.exit(0)  # Successful termination


    # Connect to a particular mailbox
    status, messages = imap.select("Credit_Card_Transaction")  # Inbox/Folder name from list()
    if status == "OK":
        # Reading the number of email(s) N
        N = NoOfEmail
        messages = int(messages[0])
        for i in range(messages, messages-N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    
                    # Check for specific subject only
                    if subject == 'Transaction alert for your ABC Bank Credit Card' :
                        # decode email sender
                        From, encoding = decode_header(msg.get("From"))[0]
                        if isinstance(From, bytes):
                            From = From.decode(encoding)
                        # print("Subject:", subject)
                        # print("From:", From)
                    
                        # if the email message is multipart
                        if msg.is_multipart():
                            # iterate over email parts
                            # print("Email is Multipart 0")
                            for part in msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # print text/plain emails and skip attachments
                                    # print(body)
                                    pass
                                elif "attachment" in content_disposition:
                                    # download attachment
                                    filename = part.get_filename()
                                    if filename:
                                        folder_name = clean(subject)
                                        if not os.path.isdir(folder_name):
                                            # make a folder for this email (named after the subject)
                                            os.mkdir(folder_name)
                                        filepath = os.path.join(folder_name, filename)
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                        else:
                            # extract content type of email
                            content_type = msg.get_content_type()
                            # get the email body
                            body = msg.get_payload(decode=True).decode()
                            if content_type == "text/plain":
                                # print only text email parts
                                # print(body)
                                pass
                        if content_type == "text/html":
                            # if it's HTML, create a new HTML file and open it in browser
                            folder_name = clean(subject)
                            if not os.path.isdir(folder_name):
                                # make a folder for this email (named after the subject)
                                os.mkdir(folder_name)
                            filename = "index.html"
                            filepath = os.path.join(folder_name, filename)
                            # write the file
                            open(filepath, "w").write(body)
                            # open in the default browser
                            # webbrowser.open(filepath)
                # print("="*100)
            # Print Data
            if filepath:
                SpentAmt,SpentMonth,SpentDate,SpentYear,SpentTime,SpentInfo,AvailableCredit,TotalCredit = web_scrap(filepath)
                MSG="Rs. {} spent on {} {} {} {} at {}".format(SpentAmt,SpentMonth,SpentDate,SpentYear,SpentTime,SpentInfo)
                get_recent_alert(SpentMonth,SpentDate,SpentYear,SpentTime,MSG)
                # send_to_telegram(MSG)
        imap.close()

    # Logout of the IMAP server
    imap.logout()

