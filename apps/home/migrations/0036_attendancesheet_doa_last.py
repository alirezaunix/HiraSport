# Generated by Django 3.2.16 on 2024-09-16 19:31

from django.db import migrations
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_sendsms'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancesheet',
            name='doa_last',
            field=django_jalali.db.models.jDateField(blank=True, editable=False, null=True, verbose_name=' تاریخ آخرین جلسه '),
        ),
    ]
