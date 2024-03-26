# Generated by Django 3.2.16 on 2024-03-19 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_auto_20240319_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='is_trainer',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='trainer',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AddField(
            model_name='trainer',
            name='password',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='گذر واژه'),
        ),
        migrations.AddField(
            model_name='trainer',
            name='username',
            field=models.CharField(default='', max_length=20, unique=True, verbose_name='نام کاربری'),
        ),
    ]