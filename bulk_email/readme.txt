Welcome to Bulk Email from GMAIL !

This tool help user to sent email bulk email from GMAIL
To do this, user need to enable less secure app on for gmail.

Please enable from below URL
https://myaccount.google.com/lesssecureapps

Required Software:
1. Python 3.6.9

(Testing done in above mention versions)

Installation:
1. Download file from GitHub
2. Extract it to your directory

Note: Your attachment file must be in same directory/folder

Conguration:
1. User Name and Password: Line 33 and 34 in bulk_email_with_attachment.py
2. Email Subject: Line 37 in bulk_email_with_attachment.py
3. Email Content: Line 40 to Line 63 in bulk_email_with_attachment.py

Pre-rquisite:
1. You must have senders list with attachment file names in csv file

Example of sender.csv (First line/Heading of file mandatory "DO NOT CHANGE OR REPLACE")
Recipient,FileName
s.narhe@yahoo.in,intro.pdf
virtumentor@gmail.com,card.pdf

Execution:
python3.6 bulk_email_with_attachment.py -f senders.csv


#EOF