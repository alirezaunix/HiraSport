# Generated by Django 3.2.16 on 2024-04-09 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20240408_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ردیف')),
                ('dop', django_jalali.db.models.jDateField(verbose_name='تاریخ پرداخت')),
                ('rimage', models.ImageField(blank=True, null=True, upload_to='', verbose_name='عکس فیش پرداختی')),
                ('mcharged', models.IntegerField(blank=True, default=0, verbose_name='مقدار پول واریز شده')),
                ('nextiInsurancedate', django_jalali.db.models.jDateField(verbose_name='تاریخ تمدید تاریخ بعدی')),
                ('insurance_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='شخص')),
            ],
            options={
                'verbose_name': 'پرداختی',
                'verbose_name_plural': 'پرداختی ها',
            },
        ),
    ]
