# Generated by Django 3.2.16 on 2024-07-16 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0031_auto_20240624_0012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='changeFlag',
            field=models.IntegerField(blank=True, default=0, editable=False),
        ),
    ]
