# Generated by Django 3.2.16 on 2024-03-26 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20240326_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiondate',
            name='classname',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.classi', verbose_name='کلاس'),
        ),
    ]