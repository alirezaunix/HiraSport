# -*- encoding: utf-8 -*-
# TODO: one to one
from email.policy import default
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, UserManager


class SportField(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    sport_field = models.CharField(max_length=20, verbose_name="رشته ورزشی")

    class Meta:
        verbose_name = "رشته ورزشی"
        verbose_name_plural = "رشته های ورزشی"

    def __str__(self):
        return self.sport_field


class Trainer(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    tsport = models.ForeignKey(
        SportField, on_delete=models.CASCADE, verbose_name='رشته ', blank=True, null=True)
    tfull_name = models.CharField(
        max_length=30, verbose_name="نام و نام خانوادگی")
    tphone = models.CharField(max_length=20, verbose_name="شماره تلفن ")

    class Meta:
        verbose_name = "مربی"
        verbose_name_plural = "مربی ها"

    def __str__(self):
        return self.tfull_name


class Classi(models.Model):
    weekdays_list = ('Sat', 'شنبه'), ('Sun', 'یکشنبه'), ('Mon', 'دوشنبه'), (
        'Tue', 'سه شنبه'), ('Wed', 'چهارشنبه'), ('Thu', 'پنجشنبه'), ('Fri', 'جمعه')
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    tname = models.ForeignKey(Trainer, on_delete=models.CASCADE,
                              max_length=50, verbose_name='مربی ', blank=True, null=True)
    cname = models.CharField(max_length=20, verbose_name="نام کلاس ")
    weekdays = MultiSelectField(
        choices=weekdays_list, max_choices=7, max_length=30)
    starttime = models.TimeField()

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس ها"

    def __str__(self):
        return self.cname


class MyUserManager(BaseUserManager):

    def create_user(self, username, password=None):
        print("in create user------>>>>>>")
        user = self.model(username=username)
        user.set_password(password)
        self.is_hashed = True
        user.save(using=self._db)
        return user

    def create_superuser(self,  username, password=None):
        print("in create superuser------>>>>>>")

        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        print(f"{user.is_admin=:}")
        print(f"{user.is_superuser=:}")
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    gender_choice = ('m', 'مرد'), ('f', 'زن')
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    first_name = models.CharField(max_length=20, verbose_name="نام")
    last_name = models.CharField(max_length=30, verbose_name="نام خانوادگی")
    full_name = models.CharField(max_length=50, blank=True, editable=False)
    ncode = models.CharField(max_length=11, verbose_name="کدملی")
    scode = models.CharField(max_length=10, verbose_name="کدبیمه ورزشی")
    shistory = models.TextField(verbose_name="سابقه ورزشی", blank=True)
    hhistory = models.TextField(verbose_name="سابقه پزشکی", blank=True)
    dob = jmodels.jDateField(verbose_name="تاریخ تولد", null=True)
    gender = models.CharField(
        max_length=1, verbose_name="جنسیت", choices=gender_choice)
    # dor = jmodels.jDateField(verbose_name="تاریخ ثبت نام اولیه",null=True)
    sfield = models.ForeignKey(SportField, on_delete=models.CASCADE,
                               null=True, blank=True, default=None, verbose_name="رشته ورزشی")
    classname = models.ForeignKey(
        Classi, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="کلاس")
    phone1 = models.CharField(
        max_length=20, verbose_name="شماره تلفن اول", null=True)
    phone2 = models.CharField(
        max_length=20, verbose_name="شماره تلفن دوم", null=True)
    address = models.TextField(verbose_name="آدرس", blank=True, null=True)
    created_time = jmodels.jDateField(auto_now_add=True)
    updated_time = jmodels.jDateField(auto_now=True)
    simage = models.ImageField(verbose_name="عکس ", blank=True, null=True)
    rsession = models.IntegerField(
        verbose_name="تعداد جلسات باقی مانده", default=0)
    username = models.CharField(
        max_length=20, verbose_name="نام کاربری", unique=True)
    password = models.CharField(
        max_length=20, verbose_name="گذر واژه", blank=True)
    email = models.EmailField(verbose_name="ایمیل")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_hashed = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = MyUserManager()

    class Meta:
        verbose_name = "شخص"
        verbose_name_plural = "اشخاص"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        if not self.is_hashed:
            # New user: set the password
            print("in hashing in save method.")
            #self.set_password(self.password)
        super().save(*args, **kwargs)


class Peyment(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    peyment_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص', blank=True, null=True)
    dop = jmodels.jDateField(verbose_name="تاریخ پرداخت")
    rimage = models.ImageField(
        verbose_name="عکس فیش پرداختی", null=True, blank=True)
    mcharged = models.IntegerField(
        verbose_name="مقدار پول واریز شده", blank=True, default=0)
    ncharged = models.IntegerField(verbose_name="تعداد جلسات شارژ شده")

    class Meta:
        verbose_name = "پرداختی"
        verbose_name_plural = "پرداختی ها"

    def __str__(self):
        return f"{self.peyment_person}"


class SessionDate(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    session_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص')
    dos = jmodels.jDateField(verbose_name="تاریخ جلسه")

    class Meta:
        verbose_name = "جلسه"
        verbose_name_plural = "جلسات"

    def __str__(self):
        return f"{self.session_person} {self.dos}"


class AbsenceDate(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    absent_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص')
    doa = jmodels.jDateField(verbose_name="تاریخ غیبت")

    class Meta:
        verbose_name = "غیبت"
        verbose_name_plural = "غیبتها"

    def __str__(self):
        return f"{self.session_person} {self.doa}"


class Analysis (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    analysis_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص')
    dot = jmodels.jDateField(verbose_name="تاریخ آنالیز")

    current_state_weight = models.FloatField(verbose_name="وضعیت موجود - وزن")
    current_state_bfm = models.FloatField(
        verbose_name="وضعیت موجود - توده چربی")
    current_state_smm = models.FloatField(verbose_name="وضعیت موجود - عضله ")
    current_state_pbf = models.FloatField(
        verbose_name="وضعیت موجود - درصد چربی")

    point_state_weight = models.FloatField(verbose_name="هدف مقطعی - وزن")
    point_state_bfm = models.FloatField(verbose_name="هدف مقطعی - توده چربی")
    point_state_smm = models.FloatField(verbose_name="هدف مقطعی - عضله ")
    point_state_pbf = models.FloatField(verbose_name="هدف مقطعی - درصد چربی")

    class Meta:
        verbose_name = "آنالیز"
        verbose_name_plural = "آنالیزها"

    def __str__(self):
        return ""
