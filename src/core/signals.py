from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver, Signal

from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created,**kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )

@receiver(user_logged_in)
def login_user(sender, request, user, *args, **kwargs):
    print(f'{user} login')


per_remove = Signal()

@receiver(per_remove)
def test_it(sender,**kwargs):
    print(kwargs)