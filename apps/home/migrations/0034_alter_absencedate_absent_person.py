# Generated by Django 3.2.16 on 2024-08-16 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_attendancesheet_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absencedate',
            name='absent_person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='شخص'),
        ),
    ]
