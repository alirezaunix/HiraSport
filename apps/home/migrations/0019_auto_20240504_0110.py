# Generated by Django 3.2.16 on 2024-05-03 21:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_classi_cname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ردیف')),
                ('gname', models.CharField(max_length=250, verbose_name='نام کالا')),
                ('gdesc', models.CharField(max_length=250, verbose_name='شرح کالا')),
                ('gimage', models.ImageField(blank=True, null=True, upload_to='', verbose_name='عکس کالا')),
                ('gprice', models.IntegerField(blank=True, default=0, null=True, verbose_name='قیمت کالا')),
                ('gstock', models.IntegerField(blank=True, default=0, max_length=250, null=True, verbose_name='موجودی کالا')),
                ('gdiscount', models.IntegerField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
            ],
            options={
                'verbose_name': 'کالا',
                'verbose_name_plural': 'کالا ها',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='wallet',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='کیف پول'),
        ),
        migrations.CreateModel(
            name='WalletCharge',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ردیف')),
                ('walletcharge_dop', django_jalali.db.models.jDateField(verbose_name='تاریخ پرداخت')),
                ('rimage', models.ImageField(blank=True, null=True, upload_to='', verbose_name='عکس فیش پرداختی')),
                ('walletcharge_charged', models.IntegerField(blank=True, default=0, verbose_name='مقدار پول واریز شده')),
                ('walletcharge_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='شخص')),
            ],
            options={
                'verbose_name': 'شارژ کیف پول',
                'verbose_name_plural': '  شارژ ها کیف پول',
            },
        ),
        migrations.CreateModel(
            name='GoodsPeyment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ردیف')),
                ('gpeyment_dop', django_jalali.db.models.jDateField(verbose_name='تاریخ پرداخت')),
                ('gpeyment_goods', models.ManyToManyField(to='home.Goods', verbose_name='اجناس خریده شده')),
                ('gpeyment_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='شخص')),
            ],
            options={
                'verbose_name': 'خرید کالا',
                'verbose_name_plural': 'خرید کالا ها',
            },
        ),
    ]
