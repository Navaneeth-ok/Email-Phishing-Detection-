

#email_filter.py

import sqlite3
import re

def load_phishing_urls():
    conn = sqlite3.connect('threat_intel.db')
    c = conn.cursor()
    c.execute("SELECT url FROM phishing_urls")
    urls = [row[0] for row in c.fetchall()]
    conn.close()
    return urls



def check_email_for_phishing(email_content,email_headers):
    phishing_urls = load_phishing_urls()

    for url in phishing_urls:
        if re.search(re.escape(url), email_content):
           return True


    suspicious_keywords = ["urgent","account","login","click here","update","immediately","bank","verify your identity"]
    for keyword in suspicious_keywords:
        if keyword.lower() in email_content.lower():
             return True

    from_address = email_headers.get('FROM')
    reply_to_address = email_headers.get('Reply-To')
    if reply_to_address and reply_to_address != from_address:
         return True

    attachments = email_headers.get('Attachments',[])
    suspicious_file_types = ['.exe', '.scr', '.zip', '.rar', '.js', '.jar']
    for attachment in attachments:
        if any(attachment.endswith(ext) for ext in suspicious_file_types):
            return True

    return False
