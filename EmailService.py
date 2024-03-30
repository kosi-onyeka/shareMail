import imaplib
import email
import html2text
import os

class EmailService:
    def __init__(self):
        self.emailAddress = "kosionyeka@yahoo.com"
        self.__connectToEmail()

    
    def __connectToEmail(self): 
        emailPassword = os.environ['YAHOO_PASSWORD']
        yahoo_imap_server = "imap.mail.yahoo.com"
        yahoo_imap_port = 993
        try:
            self.mailServer = imaplib.IMAP4_SSL(yahoo_imap_server, yahoo_imap_port)
        except imaplib.IMAP4.error as e:
            print(f"Failed to connect to the server: {e}")
            exit()
        self.mailServer.login(self.emailAddress, emailPassword)
        self.mailServer.select('INBOX')
        

    def getHuluLogin(self):
        status, messages = self.mailServer.search(None, "FROM", "Hulu")
        if status == "OK":
            # Get the latest message number
            latest_email_id = messages[0].split()[-1]

            # Fetch and print details of the most recent email
            status, msg_data = self.mailServer.fetch(latest_email_id, "(RFC822)")
            for response in msg_data:
                if type(response) is tuple:
                    myMsg = email.message_from_bytes(response[1])
                    body = myMsg.get_payload(decode=True).decode("utf-8")
                    plainTextContent = html2text.html2text(body)  
                    plainTextContent = plainTextContent.split('.')
                    self.verification_code = plainTextContent[0]

