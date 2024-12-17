from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from core.models import Profile

@login_required
def users_profile_view(request,username):
    try:
        user = User.objects.get(username=username)
        if user == request.user:
            return redirect('profile')
    except User.DoesNotExist:
        return redirect('profile')
    context = {'user_profile':user}
    return render(request,'profiles.html',context)