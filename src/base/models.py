from django.db import models
from django.contrib.auth.models import User
    
class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_sender')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver_user')
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10]
    
class Notification(models.Model):
    NOTIFICATION_TYPE = ((1,'Likes'),(2,'Follow'),(3,'Message'))
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='sender')
    content = models.CharField(max_length=100)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content