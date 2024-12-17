from django.core.management.base import BaseCommand
from core.models import PasswordReset
from core.signals import per_remove

import datetime

class Command(BaseCommand):

    def handle(self,*args,**kwargs):
        today = datetime.date.today()
        for obj in PasswordReset.objects.all():
            user = obj.user.username
            per_remove.send(sender=self.__class__,user=obj.user,username=obj.user.username)
            start_time = obj.timestamp.date()
            end_time = start_time + datetime.timedelta(days=1)
            print(f'{start_time} >>> {end_time}')
            if end_time > today:
                obj.delete()
                print(f'{user}')