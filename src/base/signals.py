from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Notification

@receiver(post_save,sender=User)
def user_get_notify(sender,instance,created,**kwargs):
    admin = User.objects.get(id=1)
    if created:
        Notification.objects.create(
            user=instance,
            sender=admin,
            content='Welcome to Instagram clone',
            notification_type=3
        )