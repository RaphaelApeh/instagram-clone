import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify,Truncator

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='pics',blank=True)
    likes = models.ManyToManyField(User,blank=True,related_name='liked')
    slug = models.SlugField(blank=True,null=True)
    favourite = models.ManyToManyField(User,blank=True,related_name='bookmark')
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save(self,*args,**kwargs):
        if not self.slug:
            i = Truncator(self.name).words(45)
            self.slug = slugify(i)
        super().save(*args,**kwargs)

    def truncated_name(self):
        truncator = Truncator(self.name).chars(50)
        return truncator
    
    def number_of_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True,default='default-user.png',upload_to='profile')
    bio = models.TextField(blank=True,null=True)
    following = models.ManyToManyField("self",blank=True,related_name='followed_by',symmetrical=False)
    active = models.BooleanField(default=True)
    messagers = models.ManyToManyField("self",blank=True)

    def __str__(self):
        return self.user.username
    
class PasswordReset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reset = models.UUIDField(default=uuid.uuid4(),editable=False,unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username