# Generated by Django 3.2.16 on 2024-02-27 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_person_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_superuser',
        ),
    ]