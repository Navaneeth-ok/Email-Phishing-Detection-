
#email_integration.py

import imaplib
import email
from email_filter import check_email_for_phishing


def fetch_emails():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('rizzzler60@gmail.com',' uwsj ntrs bxnw vjtk')
    mail.select('inbox')


    result,data = mail.search(None, 'ALL')
    email_ids = data[0].split()


    for  email_id in email_ids:
         result, msg_data = mail.fetch(email_id, '(RFC822)')
         raw_email = msg_data[0][1]
         msg = email.message_from_bytes(raw_email)


         email_content = ""
         email_headers = {
             "From":msg['From'],
             "Reply-To":msg['Reply-To'],
             "Attachments":[part.get_filename() for part in msg.walk() if part.get_filename()]
         }


         for part in msg.walk():
             content_type = part.get_content_type()
             if content_type == 'text/plain':
                  email_content += part.get_payload(decode=True).decode('utf-8', 'ignore')


         if check_email_for_phishing(email_content,email_headers):
             print(f"Phishing email detected: {msg['Subject']}")
         else:
             print(f"Email is safe: {msg['Subject']}")


    mail.logout()

if __name__ == '__main__':
     fetch_emails()
