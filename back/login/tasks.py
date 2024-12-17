from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

@shared_task
def delete_inactive_users():
    deadline = timezone.now() - timedelta(minutes=5)
    users_deleted = CustomUser.objects.filter(is_active=False, date_joined__lt=deadline).delete()
    return users_deleted
