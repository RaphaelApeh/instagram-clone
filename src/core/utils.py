from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()

def get_users_not_followed(current_user):
    profile = Profile.objects.get(user=current_user)
    followed_users = profile.following.all()
    users_not_followed = User.objects.exclude(id__in=followed_users).exclude(id=current_user.id)
    return users_not_followed

def authenticate(username=None,password=None):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.get(email=username)
    except User.DoesNotExist:
        return None
    if user.check_password(password):
        return user
    else:
        return None