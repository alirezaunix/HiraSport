# Generated by Django 3.2.16 on 2024-04-13 18:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20240412_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiondate',
            name='sstudent',
            field=models.ManyToManyField(related_name='studentINthisSession', to=settings.AUTH_USER_MODEL),
        ),
    ]