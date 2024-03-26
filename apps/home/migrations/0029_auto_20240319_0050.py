# Generated by Django 3.2.16 on 2024-03-18 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_analysis_reportfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='reportfile',
            field=models.FileField(blank=True, default="''", null=True, upload_to='', verbose_name='فایل آنالیز'),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='person',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone1',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره تلفن اول'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone2',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره تلفن دوم'),
        ),
        migrations.AlterField(
            model_name='person',
            name='scode',
            field=models.CharField(blank=True, max_length=10, verbose_name='کدبیمه ورزشی'),
        ),
    ]