#module to send mail with attachment of zip file containing csv files
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os
import subprocess
from complete_log_parser import body

smtp_username = ''
smtp_server = ''
smtp_password = ''
smtp_port = ''

email_fromaddr = ''
email_toaddrs = [''] #add mail separated by comma and within single quotes

#run the main script for generating attachmen
subprocess.call(" python3 main.py 1", shell=True)

def email(email_fromaddr,email_toaddrs,message):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        try:
            #server.set_debuglevel(10)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(email_fromaddr, email_toaddrs, message)
            print("mail sent successfully")
        except smtplib.SMTPException as e:
            print("error unable to send mail {}".format(e))

SUBJECT = "Please go through the below attachments for the log reports"

message = MIMEMultipart('alternative')

message['Subject'] = SUBJECT

message['From'] = email_fromaddr
message['To'] = ",".join(email_toaddrs)
# message['Body'] = body
attachments = ['./LOGS.zip']
part1=MIMEText(body, 'plain')

for file in attachments:
       with open(file, 'rb') as fp:
            msg = MIMEBase('application', "octet-stream")
            msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            message.attach(msg)
message.attach(part1)           
message = message.as_string()

email(email_fromaddr, email_toaddrs, message)



