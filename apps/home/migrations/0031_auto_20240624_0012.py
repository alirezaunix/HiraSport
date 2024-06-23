# Generated by Django 3.2.16 on 2024-06-23 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_alter_attendancesheet_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='current_state_pbf',
            field=models.FloatField(default=0, editable=False, verbose_name='وضعیت موجود - درصد چربی'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='diffrence_bfm',
            field=models.FloatField(default=0, editable=False, verbose_name=' اختلاف - توده چربی'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='diffrence_pbf',
            field=models.FloatField(default=0, editable=False, verbose_name=' اختلاف - درصد چربی'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='diffrence_smm',
            field=models.FloatField(default=0, editable=False, verbose_name=' اختلاف - عضله '),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='diffrence_weight',
            field=models.FloatField(default=0, editable=False, verbose_name=' اختلاف - وزن'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='point_state_pbf',
            field=models.FloatField(default=0, editable=False, verbose_name='هدف مقطعی - درصد چربی'),
        ),
    ]
