import smtplib
from email.mime.text import MIMEText

def send_test_email():
    msg = MIMEText("Hello from MailHog!")
    msg['Subject'] = 'Test Email'
    msg['From'] = 'sender@example.com'
    msg['To'] = 'receiver@example.com'

    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)

send_test_email()
