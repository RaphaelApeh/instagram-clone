# Generated by Django 5.0.4 on 2024-08-09 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 8, 9, 11, 31, 15, 998240, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]