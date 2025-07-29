from model import User,Lots
import random
import smtplib
from email.message import EmailMessage

def gen_user_id():
    while True:
        rid = random.randint(100001, 999999)
        if not User.query.filter_by(userId=rid).first():
            return rid

def gen_lot_id():
    while True:
        alpha1=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        alpha2=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        lotId= f"{alpha1}{alpha2}"
        if not Lots.query.filter_by(lotId=lotId).first():
            return lotId

def send_mail(subject, recipients, body):
    if isinstance(recipients, str):
        recipients = [recipients]  

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = "admin@example.com"
    msg['To'] = ', '.join(recipients)
    msg.set_content(body)

    try:
        with smtplib.SMTP('localhost', 1025) as smtp:  # MailHog default SMTP
            smtp.send_message(msg)
        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
