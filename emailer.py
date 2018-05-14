import httplib2
import os
import oauth2client
from oauth2client import client, tools
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from apiclient import errors, discovery
import mimetypes
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase

class Emailer(object):
    def __init__(self):
         self.scopes = 'https://www.googleapis.com/auth/gmail.send'
         self.client_secret_file = 'client_secret.json'
         self.application_name = 'Send CU Email'
         
    def get_credentials(self):
        credential_path = './credentials.json'
        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.scopes)
            flow.user_agent = self.application_name
            credentials = tools.run_flow(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
    
    def SendMessage(self, sender, to, bcc, subject, msgHtml, msgPlain, attachmentFile=None):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        if attachmentFile:
            message1 = self.CreateMessageWithAttachment(sender, to, bcc, subject, msgHtml, msgPlain, attachmentFile)
        else: 
            message1 = self.CreateMessageHtml(sender, to, bcc, subject, msgHtml, msgPlain)
        result = self.SendMessageInternal(service, "me", message1)
        return result
    
    def SendMessageInternal(self, service, user_id, message):
        try:
            message = (service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return True
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return False
        return "OK"

    def CreateMessageHtml(self, sender, to, bcc, subject, msgHtml, msgPlain):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to
        msg['BCC'] = bcc
        msg.attach(MIMEText(msgPlain, 'plain'))
        msg.attach(MIMEText(msgHtml, 'html'))
        return {'raw': base64.urlsafe_b64encode(msg.as_string())}

    def CreateMessageWithAttachment(self, sender, to, bcc, subject, msgHtml, msgPlain, attachmentFile):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        msgHtml: Html message to be sent
        msgPlain: Alternative plain text message for older email clients          
        attachmentFile: The path to the file to be attached.

        Returns:
        An object containing a base64url encoded email object.
        """
        message = MIMEMultipart('mixed')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message['BCC'] = bcc
        messageA = MIMEMultipart('alternative')
        messageR = MIMEMultipart('related')

        messageR.attach(MIMEText(msgHtml, 'html'))
        messageA.attach(MIMEText(msgPlain, 'plain'))
        messageA.attach(messageR)

        message.attach(messageA)

        print("create_message_with_attachment: file: %s" % attachmentFile)
        content_type, encoding = mimetypes.guess_type(attachmentFile)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(attachmentFile, 'rb')
            msg = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(attachmentFile, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(attachmentFile, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(attachmentFile, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(attachmentFile)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_string())}


    def Send(self, bcc=""):
        try:
            to = "jack.rothrock@colorado.edu"
            sender = "jack.rothrock@colorado.edu"
            subject = "CU Classes Ranked By GPA - Find The 'Easiest' Classes For Subjects/Cores."
            msgHtml = "Using the FCQ data, I created an Excel application which ranks the classes for each core subject from highest GPA to lowest GPA - ie, human diversity, ideals and values, etc. I wrote an article highlighting these findings (with pictures of all classes and gpas for each subject), as well as other interesting findings - like how a dorm impacts your graduation rates, and graduation rates for those with less than a 2.8 compared to those with above a 3.2.<br><br> The article can be found here: <a href='https://jackrothrock.com/uni-of-colorado-grade-distribution/'>https://jackrothrock.com/uni-of-colorado-grade-distribution/</a><br><br>The code for the Excel project can be found here: <a href='https://github.com/jrothrock/cu_grades'>https://github.com/jrothrock/cu_grades</a><br><br>A direct download to the Excel file can be found here: <a href='https://www.dropbox.com/s/zlipro1btos075b/CU_Class_Helper.xlsm?dl=0'>https://www.dropbox.com/s/zlipro1btos075b/CU_Class_Helper.xlsm?dl=0</a><br><br>And code for the scraping of CU research faculty and sending of email: <a href='https://github.com/jrothrock'>https://github.com/jrothrock/cu_scrape</a><br><br><br><br><strong>Also, I'm looking for a summer research position. </strong> I'm currently doing one for another teacher, but it's only 10 hours a week. I'm mainly looking for a paid position. Included is my resume.<br><br>Also, FWIW, this hasn't/wont be sent to other students.<br>"
            msgPlain = "Using the FCQ data, I created an Excel application which ranks the classes for each core subject from highest GPA to lowest GPA - ie, human diversity, ideals and values, etc. I wrote an article highlighting these findings (with pictures of all classes and gpas for each subject), as well as other interesting findings - like how a dorm impacts your graduation rates, and graduation rates for those with less than a 2.8 compared to those with above a 3.2.\n\nThe article can be found here: https://jackrothrock.com/uni-of-colorado-grade-distribution/\n\nThe code for the Excel project can be found here: https://github.com/jrothrock/cu_grades\n\nA direct download to the Excel file can be found here: https://www.dropbox.com/s/zlipro1btos075b/CU_Class_Helper.xlsm?dl=0\n\nAnd code for the scraping of CU research faculty and sending of email: https://github.com/jrothrock/cu_scrape (https://github.com/jrothrock)\n\nALSO, I'M LOOKING FOR A SUMMER RESEARCH POSITION. I'm currently doing one for another teacher, but it's only 10 hours a week. I'm mainly looking for a paid position. Included is my resume.\n\nAlso, FWIW, this hasn't/wont be sent to other students."
            return self.SendMessage(sender, to, bcc, subject, msgHtml, msgPlain, './Jack Rothrock\'s Resume.pdf')
        except Exception as ex:
            print ex
            
    def __enter__(self):
        return self
    
    def __exit__(self, *args, **kwargs):
        return self

# with Emailer() as email:
#     email.Send()