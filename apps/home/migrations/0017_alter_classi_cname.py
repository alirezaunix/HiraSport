# Generated by Django 3.2.16 on 2024-04-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_alter_person_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classi',
            name='cname',
            field=models.CharField(default=None, max_length=20, verbose_name='نام کلاس '),
        ),
    ]