#Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Define these once; use them twice!
strFrom = 'root@server.lan'
strTo = 'virtumentor@gmail.com'

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

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
#msgText = MIMEText('<b>Some <i>HTML</i> text</b> and an image.<br><img src="cid:image1"><br>Nifty!', 'html')
msgText = MIMEText('<br><img src="cid:image1"><br><img src="cid:image2">', 'html')
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
#smtp.login('exampleuser', 'examplepass')
smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.quit()