# -*- encoding: utf-8 -*-
from email.policy import default
from tabnanny import verbose
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator


class MyUserManager(BaseUserManager):

    def create_user(self, username, password, is_superuser=False):
        user = self.model(username=username, is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  username, password, ):
        return self.create_user(username, password, is_superuser=True)


class SportField(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    sport_field = models.CharField(max_length=20, verbose_name="رشته ورزشی")

    class Meta:
        verbose_name = "رشته ورزشی"
        verbose_name_plural = "رشته های ورزشی"

    def __str__(self):
        return self.sport_field

class Classi(models.Model):
    weekdays_list = ('Sat', 'شنبه'), ('Sun', 'یکشنبه'), ('Mon', 'دوشنبه'), (
        'Tue', 'سه شنبه'), ('Wed', 'چهارشنبه'), ('Thu', 'پنجشنبه'), ('Fri', 'جمعه')
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
#    tname = models.ForeignKey(Trainer, on_delete=models.CASCADE,
#                              max_length=50, verbose_name='مربی ', blank=True, null=True)
    cname = models.CharField(
        max_length=20, verbose_name="نام کلاس ")
    weekdays = MultiSelectField(
        choices=weekdays_list, max_choices=7, max_length=30)
    starttime = models.TimeField()
    ctrainer = models.ForeignKey(
        "Person", on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="مربی کلاس")
    fee=models.IntegerField(default=0,verbose_name=" شهریه ۱۲ جلسه (تومان)",blank=True)
    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس ها"

    def __str__(self):
        return self.cname


class MyUserManager(BaseUserManager):

    def create_user(self, username, password, is_superuser=False):
        user = self.model(username=username, is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  username, password, ):
        return self.create_user(username, password, is_superuser=True)


class Person(AbstractBaseUser):
    ROLE_CHOICES = [
        ('employee', 'کارمند'),
        ('trainer', 'مربی'),
        ('student', 'ورزشکار'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,
                            verbose_name="نوع کاربر", default="student")

    gender_choice = ('m', 'مرد'), ('f', 'زن')
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    full_name = models.CharField(max_length=50, blank=True)
    ncode = models.CharField(max_length=11, verbose_name="کدملی",blank=True)
    scode = models.CharField(
        max_length=10, verbose_name="کدبیمه ورزشی", blank=True)
    insurancedate = jmodels.jDateField(
        verbose_name="تاریخ بعدی بیمه ورزشی", null=True,blank=True)
    shistory = models.TextField(verbose_name="سابقه ورزشی", blank=True)
    hhistory = models.TextField(verbose_name="سابقه پزشکی", blank=True)
    dob = jmodels.jDateField(verbose_name="تاریخ تولد", null=True,blank=True)
    gender = models.CharField(
        max_length=1, verbose_name="جنسیت", choices=gender_choice)
    # dor = jmodels.jDateField(verbose_name="تاریخ ثبت نام اولیه",null=True)
    sfield = models.ForeignKey(SportField, on_delete=models.CASCADE,
                               null=True, blank=True, default=None, verbose_name="رشته ورزشی")
    classname = models.ForeignKey(
        Classi, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="کلاس")
    discount = models.IntegerField(default=0,blank=True,validators=[MinValueValidator(0),MaxValueValidator(100)],verbose_name="درصد تخفیف نفر بر روی دوره ها")
    phone1 = models.CharField(
        max_length=20, verbose_name="شماره تلفن اول", blank=True,null=True)
    phone2 = models.CharField(
        max_length=20, verbose_name="شماره تلفن دوم", blank=True,null=True)
    address = models.TextField(verbose_name="آدرس", blank=True, null=True)
    created_time = jmodels.jDateField(auto_now_add=True)
    updated_time = jmodels.jDateField(auto_now=True)
    simage = models.ImageField(verbose_name="عکس ", blank=True, null=True)
    rsession = models.IntegerField(
        verbose_name="تعداد جلسات باقی مانده", default=0,blank=True)
    username = models.CharField(
        max_length=20, verbose_name="نام کاربری", unique=True)
    password = models.CharField(
        max_length=128, verbose_name="گذر واژه", blank=True)
    email = models.EmailField(verbose_name="ایمیل", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    #is_admin = models.BooleanField(default=False, editable=False)
    is_superuser = models.BooleanField(default=False, editable=False)
    is_staff = models.BooleanField(default=False, editable=False)
    is_trainer = models.BooleanField(default=False, editable=False)

    t_edu = models.TextField(verbose_name="میزان تحصیلات", blank=True)
    t_exp = models.TextField(verbose_name="سوابق تجربی", blank=True)
    t_shortdesc = models.TextField(verbose_name="توضیح کوتاه ", blank=True)
    
    nextanalysis = models.CharField(
        max_length=20, blank=True,editable=False)

    USERNAME_FIELD = "username"

    objects = MyUserManager()

    class Meta:
        verbose_name = "شخص"
        verbose_name_plural = "اشخاص"

    def __str__(self):
        return f"{self.full_name}"

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
        return self.is_superuser

    def __init__(self, *args, **kwargs):
        super(Person, self).__init__(*args, **kwargs)
        # Store the original value of the field
        self.__original_password = self.password

    def save(self, *args, **kwargs):
        #self.full_name = f"{self.first_name} {self.last_name}"
        if (not self.is_superuser and self.pk is None ) or  self.password != self.__original_password:
            self.set_password(self.password)
        self.is_superuser = True if self.role == 'employee' else False
        super().save(*args, **kwargs)

    @property
    def is_admin(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


class Insurance(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    insurance_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص', blank=True, null=True)
    dop = jmodels.jDateField(verbose_name="تاریخ پرداخت")
    rimage = models.ImageField(
        verbose_name="عکس  بیمه", null=True, blank=True)
    mcharged = models.IntegerField(
        verbose_name="مقدار پول واریز شده", blank=True, default=0)
    nextiInsurancedate  = jmodels.jDateField(verbose_name="تاریخ تمدید  بعدی")


    class Meta:
        verbose_name = "بیمه"
        verbose_name_plural = "بیمه ها"

    def __str__(self):
        return f"{self.insurance_person}"


class SessionDate(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    session_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص')
    classname = models.ForeignKey(
        Classi, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="کلاس")
    dos = jmodels.jDateField(verbose_name="تاریخ جلسه")
    sstudent = models.ManyToManyField(
        Person, related_name='studentINthisSession')

    class Meta:
        verbose_name = "جلسه"
        verbose_name_plural = "جلسات"

    def __str__(self):
        return f"{self.session_person} {self.dos}"


class AbsenceDate(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    classname = models.ForeignKey(
        Classi, on_delete=models.CASCADE, null=True, blank=True, default=None, verbose_name="کلاس")
    absent_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص')
    doa = jmodels.jDateField(verbose_name="تاریخ غیبت")

    class Meta:
        verbose_name = "غیبت"
        verbose_name_plural = "غیبتها"

    def __str__(self):
        return f"{self.absent_person} {self.doa}"


class Analysis (models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ردیف')
    analysis_person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name='شخص', blank=True, null=True)
    dot = jmodels.jDateField(verbose_name="تاریخ آنالیز")

    current_state_weight = models.FloatField(
        verbose_name="وضعیت موجود - وزن", default=0)
    current_state_bfm = models.FloatField(
        verbose_name="وضعیت موجود - توده چربی", default=0)
    current_state_smm = models.FloatField(
        verbose_name="وضعیت موجود - عضله ", default=0)
    current_state_pbf = models.FloatField(
        verbose_name="وضعیت موجود - درصد چربی", default=0)

    diffrence_weight = models.FloatField(
        verbose_name="وضعیت موجود - وزن", default=0, editable=False)
    diffrence_bfm = models.FloatField(
        verbose_name="وضعیت موجود - توده چربی", default=0, editable=False)
    diffrence_smm = models.FloatField(
        verbose_name="وضعیت موجود - عضله ", default=0, editable=False)
    diffrence_pbf = models.FloatField(
        verbose_name="وضعیت موجود - درصد چربی", default=0, editable=False)

    point_state_weight = models.FloatField(
        verbose_name="هدف مقطعی - وزن", default=0)
    point_state_bfm = models.FloatField(
        verbose_name="هدف مقطعی - توده چربی", default=0)
    point_state_smm = models.FloatField(
        verbose_name="هدف مقطعی - عضله ", default=0)
    point_state_pbf = models.FloatField(
        verbose_name="هدف مقطعی - درصد چربی", default=0)

    reportfile = models.FileField(
        verbose_name="فایل آنالیز", null=True, default="''", blank=True)
    reportfile_len = models.IntegerField(editable=False, default=0)

    class Meta:
        verbose_name = "آنالیز"
        verbose_name_plural = "آنالیزها"

    def __str__(self):
        return f"{self.analysis_person} {self.dot}"


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
