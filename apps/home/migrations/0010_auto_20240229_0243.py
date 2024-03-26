# Generated by Django 3.2.16 on 2024-02-28 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_remove_person_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='person',
            name='is_superuser',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='current_state_bfm',
            field=models.FloatField(default=0, verbose_name='وضعیت موجود - توده چربی'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='current_state_pbf',
            field=models.FloatField(default=0, verbose_name='وضعیت موجود - درصد چربی'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='current_state_smm',
            field=models.FloatField(default=0, verbose_name='وضعیت موجود - عضله '),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='current_state_weight',
            field=models.FloatField(default=0, verbose_name='وضعیت موجود - وزن'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='point_state_bfm',
            field=models.FloatField(default=0, verbose_name='هدف مقطعی - توده چربی'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='point_state_pbf',
            field=models.FloatField(default=0, verbose_name='هدف مقطعی - درصد چربی'),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='point_state_smm',
            field=models.FloatField(default=0, verbose_name='هدف مقطعی - عضله '),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='point_state_weight',
            field=models.FloatField(default=0, verbose_name='هدف مقطعی - وزن'),
        ),
    ]