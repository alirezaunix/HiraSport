# Generated by Django 3.2.16 on 2024-03-03 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_analysis_reportfile'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='reportfile_len',
            field=models.IntegerField(default=0, editable=False),
        ),
    ]