# Generated by Django 3.2.16 on 2024-03-03 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_analysis_reportfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='reportfile',
            field=models.FileField(null=True, upload_to='', verbose_name='فایل آنالیز'),
        ),
    ]
