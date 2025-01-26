from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import logout, login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .utils import authenticate, get_users_not_followed
from base.models import Notification
from .models import Post, Comment, Profile, PasswordReset
from .forms import UserRegisterForm, CreateForm

User = get_user_model()


def home_page(request):
    if request.user.is_anonymous:
        return redirect('login')
    all_user = get_users_not_followed(request.user).order_by('?')
    user_follow = request.user.profile
    user_profile = user_follow.following.values_list('id',flat=True)
    posts = Post.objects.filter(Q(user__id__in=user_profile)|Q(user=request.user)|Q(user__id__in=[request.user.profile.followed_by.values_list('id',flat=True)])).order_by('-timestamp')
    p = Paginator(posts, 5)
    page = request.GET.get('page')
    pages = p.get_page(page)
    return render(request, 'index.html', {'posts':posts,'all_user':all_user,'pages':pages})

@login_required(login_url='login/')
def likes_view(request, slug):
    user = User.objects.get(id=request.user.id)
    post = Post.objects.get(slug=slug)
    if post.likes.filter(id=request.user.id):
        post.likes.remove(request.user)
        count = post.likes.count()
        if request.user != post.user:
            Notification.objects.create(
                user=post.user,
                sender=request.user,
                content=f"{user.username} Unliked your post '{post.name[:10]}'... ",
                notification_type=1,
            )
        return JsonResponse({"added": False, 'count': count})
    post.likes.add(request.user)
    if request.user != post.user:
        Notification.objects.create(
            user=post.user,
            sender=request.user,
            content=f"{user.username} Liked your post '{post.name[:10]}'... ",
            notification_type=1,
        )
    count = post.likes.count()
    return JsonResponse({"added": True, "count": count})

@login_required
def save_post_view(request,slug=None):
    post = get_object_or_404(Post,slug=slug)
    if post.favourite.filter(id=request.user.id):
        post.favourite.remove(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        post.favourite.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login/')
def comments_view(request,slug):
    post = get_object_or_404(Post,slug=slug)
    comment = post.comment_set.all()
    if request.method == 'POST':
        Comment.objects.create(
            post=post,
            user=request.user,
            body=request.POST.get('body')
        )
        return redirect('comment',post.slug)
    context = {'comments':comment,'post':post}
    return render(request,'main.html',context)

@login_required(login_url='login/')
def follow_view(request,pk):
    if request.method == 'POST':
        profile = Profile.objects.get(id=pk)
        request.user.profile.following.add(profile)
        request.user.profile.save()
        Notification.objects.create(
                user=profile.user,
                sender=request.user,
                content=f"{request.user.username} started following you ",
                notification_type=2,
            )
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login/')
def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=username,password=password)
            if user is not None or not "":
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,'Invalid Credential')
                return redirect('login')
        except:
            messages.error(request,'Something went Wrong,Try again!')
            return redirect('login')
    context = {}
    return render(request,'login.html',context)

@login_required
def profile_view(request):
    return render(request,'profile.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            test_user = form.save()
            send_mail(subject='Thanks for signing in to Instagram Clone ',message='Thanks for signing in',from_email=settings.EMAIL_BACKEND,recipient_list=[test_user.email],fail_silently=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
            return redirect('home')
        else:
            messages.error(request,form.errors)
            return redirect('signup')
    form = UserRegisterForm()
    context = {'form':form}
    return render(request,'sign_up.html',context)

def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            reset = PasswordReset(user=user)
            reset.save()
            send_mail(subject='Password Reset',message=f"Reset your password here\n\n\n {request.scheme}://{request.get_host()}/reset-password/{reset.reset}/",recipient_list=[reset.user.email],from_email=settings.EMAIL_BACKEND,fail_silently=True)
            messages.success(request,f'Sent to reset to {reset.user.email}')
            return redirect('forgot-password')
        except User.DoesNotExist:
            messages.error(request,f'"{email}" Does Not Exist?')
            return redirect('forgot-password')
        #print(f'{email} >>>> {request.POST}')
    context = {}
    return render(request,'forgot-password.html',context)

def reset_password_view(request,reset_id):
    try:
        password_reset = PasswordReset.objects.get(reset=reset_id)
        if request.user.is_authenticated:
            return redirect('home')
        user = password_reset.user
        if request.method == 'POST':
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request,f'{e}')
                return redirect('reset-password',password_reset.reset)
            if password != password2:
                messages.error(request,'Password Not Match!!')
                return redirect('reset-password',password_reset.reset)
            user.set_password(password)
            user.save()
            password_reset.delete()
            messages.success(request,f'Successfuly set password for {user.get_full_name()}')
            return redirect('login')
    except PasswordReset.DoesNotExist:
        messages.error(request,'Invalid Link')
        return redirect('forgot-password')
    context = {}
    return render(request,'reset-password.html',context)

@login_required
def unfollow_view(request,pk):
    if request.method == 'POST':
        user = Profile.objects.get(id=pk)
        request.user.profile.following.remove(user.id)
        Notification.objects.create(
            user=user.user,
            sender=request.user,
            content=f"{request.user.get_full_name()} Unfollow you",
            notification_type=1,
        )
        return redirect(request.META.get('HTTP_REFERER'))
    
@login_required
def create_view(request):
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'create.html',context)

@login_required
def search_view(request,*args,**kwargs):
    query = request.GET.get('q','')
    if query:
        profile = Profile.objects.filter(Q(user__username__icontains=query))
    context = {'query':query,'profiles':profile}
    return render(request,'search.html',context)