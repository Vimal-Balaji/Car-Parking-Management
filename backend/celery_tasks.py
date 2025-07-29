# celery_tasks.py
from celery_app import apps
import os,csv

from func import send_mail
from extensions import app
from model import User,OccupiedSlot

REPORT_FOLDER = os.path.join(os.getcwd(), 'reports')


@apps.task(name='celery_tasks.send_email')
def send_email():
    with app.app_context():
        os.makedirs(REPORT_FOLDER, exist_ok=True)

        users = User.query.all()
        for user in users:
            details = OccupiedSlot.query.filter_by(userId=user.userId).all()
            if not details:
                continue

            file_name = f"{user.userId}_report.csv"
            file_path = os.path.join(REPORT_FOLDER, file_name)

            # Write CSV file
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Slot ID', 'Lot ID', 'Vehicle No', 'Price', 'Start Time', 'End Time'])
                for d in details:
                    writer.writerow([
                        d.slotId, d.lotId, d.vehicleNo, d.price,
                        d.startTime.strftime('%Y-%m-%d %H:%M'),
                        d.endTime.strftime('%Y-%m-%d %H:%M')
                    ])

            # Generate public link
            file_url = f"http://localhost:5000/reports/{file_name}"

            # Compose email
            subject = "Monthly Parking Report"
            recipient = [user.email]
            body = f"""
Hi {user.name},

Your monthly parking report is ready.

You can download it from the following link:
{file_url}

Regards,  
Admin
"""
            send_mail(subject, recipient, body)