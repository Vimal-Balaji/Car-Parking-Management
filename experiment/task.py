from celery import Celery
import smtplib
from email.mime.text import MIMEText

# Create Celery app
app = Celery('tasks', broker='redis://localhost:6379/0')

# Define the task
@app.task
def send_hello_email(from_email, from_password, to_email):
    msg = MIMEText("Hello from Celery!")
    msg['Subject'] = 'Celery Test'
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(from_email, from_password)
            smtp.sendmail(from_email, to_email, msg.as_string())
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email: {e}"
