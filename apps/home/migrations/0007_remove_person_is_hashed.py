# Generated by Django 3.2.16 on 2024-02-22 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_trainer_dob'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_hashed',
        ),
    ]
