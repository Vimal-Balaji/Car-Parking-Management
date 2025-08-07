from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from .models import User

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    if not User.objects.filter(email="admin@example.com").exists():
        User.objects.create(
            userId=100000,
            name="admin",
            email="admin@example.com",
            password=make_password("admin123"),
            address="Admin Address"
        )
        print("Admin user created")
