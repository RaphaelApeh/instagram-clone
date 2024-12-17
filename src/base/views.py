from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from core.models import Profile,Post
from .models import Message,Notification

User = get_user_model()

@login_required
def notification_view(request):
    notifications = Notification.objects.filter(user=request.user,is_read=False).order_by('-timestamp')[:7]
    post = Post.objects.filter(user=request.user)
    profile = Profile.objects.exclude(user__id__in=[request.user.profile.following.values_list('id',flat=True)]).exclude(id=request.user.id).order_by('?')[:10]
    context = {'notifications':notifications,'post':post,'profile':profile}
    return render(request,'notification.html',context)

@login_required
def messages_view(request,pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(user=request.user)
    message = Message.objects.filter(Q(sender=request.user) & Q(receiver=user)| Q(sender=user) & Q(receiver=request.user)).order_by('timestamp')
    if request.method == 'POST':
        Message.objects.create(
            sender=request.user,
            receiver=user,
            text=request.POST.get('body')
        )
        profile.messagers.add(user.id)
        user.profile.messagers.add(request.user.id)
        Notification.objects.create(
                user=user,
                sender=request.user,
                content=f'sent a message .....',
                notification_type=3,
            )
        return redirect('base:messages',user.pk)
    context = {'message':message,'message_user':user}
    return render(request,'messages.html',context)

@login_required
def inbox_view(request):
    message = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    context = {'message':message}
    return render(request,'inbox.html',context)