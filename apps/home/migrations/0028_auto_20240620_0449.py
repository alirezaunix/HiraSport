# Generated by Django 3.2.16 on 2024-06-20 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_auto_20240620_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancesheet',
            name='aperson',
        ),
        migrations.AlterField(
            model_name='attendancesheet',
            name='state',
            field=models.CharField(choices=[('absent', 'غییت غیر مجاز'), ('present', 'حاضر'), ('validabsent', 'غیبت مجاز')], default='validabsent', editable=False, max_length=20, verbose_name='وضعیت حضور'),
        ),
    ]
