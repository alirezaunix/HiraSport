# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib import admin
from .models import Person, SportField, Peyment, SessionDate, Classi, AbsenceDate, Analysis, Insurance
from django.db.models.signals import post_save
from .forms import PeymentForm, SessionForm, ClassiForm, InsuranceForm  # AnalysisForm
from django.dispatch import receiver
from django.contrib.auth.models import User
import jdatetime
from django import forms


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    #list_display = ['id',  'full_name', "ncode",  "scode",   "dob",
     #               "gender", "classname", "sfield", "rsession", 'username', 'password']
    list_display = ['id',  'full_name',  
                    "gender",  'username', 'password', 'dob', 'simage', 'is_active']
    search_fields = [ 'full_name']
    list_filter = ['classname', 'gender', 'sfield','role']

    class Media:
        js = ('admin.js',)


    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'role':
                kwargs['widget'] = forms.RadioSelect
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(SportField)
class SportFieldAdmin(admin.ModelAdmin):
    list_display = ['id', 'sport_field']
    search_fields = ['id', 'sport_field']


@admin.register(Peyment)
class PeymentAdmin(admin.ModelAdmin):
    list_display = ["id", "peyment_person",
                    "dop", "rimage", "ncharged", "mcharged"]
    form = PeymentForm
    list_filter = ['dop']
    search_fields = ['peyment_person__full_name']


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ["id", "insurance_person",
                    "dop", "rimage", "mcharged", "nextiInsurancedate"]
    form = InsuranceForm
    list_filter = ['dop']
    search_fields = ['insurance_person__full_name']


@admin.register(SessionDate)
class SessionDateAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_person', 'dos']
    form = SessionForm
    model = SessionDate


@admin.register(Classi)
class ClassiAdmin(admin.ModelAdmin):
    list_display = ['id', 'weekdays', 'cname', 'starttime','ctrainer','fee']
    form = ClassiForm
    search_fields = ['session_person__full_name']


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'analysis_person','dot']
    #form = AnalysisForm
    #model = Analysis
    list_filter = ['analysis_person']
    search_fields = ['analysis_person__full_name']


@admin.register(AbsenceDate)
class AbsenceDateAdmin(admin.ModelAdmin):
    list_display = ['absent_person', 'doa']
    search_fields = ['absent_person__full_name']
    list_filter = ['doa']


@receiver(post_save, sender=AbsenceDate)
def AbsenceAction(instance,created, **kwargs):
    if created:
        person_obj = Person.objects.get(
            pk=instance.absent_person.id)
        current_value = person_obj.rsession
        person_obj.rsession=current_value-1
        person_obj.save()


@receiver(post_save, sender=Peyment)
def PeymentAction(instance,created, **kwargs):
    if created:
        person_obj = Person.objects.get(
            pk=instance.peyment_person.id)
        current_value = person_obj.rsession
        person_obj.rsession = current_value+instance.ncharged
        person_obj.save()


@receiver(post_save, sender=Insurance)
def InsuranceAction(instance, created, **kwargs):
    if created:
        person_obj = Person.objects.get(pk=instance.insurance_person.id)
        person_obj.insurancedate=instance.nextiInsurancedate
        person_obj.save()




@receiver(post_save, sender=SessionDate)
def SessionAction(instance,created, **kwarg):
    if created:
        person_obj = Person.objects.get(
            pk=instance.session_person.id)
        current_value = person_obj.rsession
        person_obj.rsession = current_value-1
        person_obj.save()



@receiver(post_save, sender=Person)
def PersonAction( instance, created, **kwargs):
    if created:
        Analysis.objects.create(analysis_person=instance,
                                dot=jdatetime.datetime.now())


@receiver(post_save, sender=Analysis)
def AnalysysAction( instance, created, **kwargs):
    if created:
        try:
            previous_record = Analysis.objects.filter(
                pk__lt=instance.pk , id= instance.analysis_person.id).latest('pk')
            Analysis.objects.filter(id=instance.pk).update(
                diffrence_weight = instance.current_state_weight-previous_record.current_state_weight,
                diffrence_bfm=instance.current_state_bfm-previous_record.current_state_bfm,
                diffrence_smm=instance.current_state_smm-previous_record.current_state_smm,
                diffrence_pbf=instance.current_state_pbf-previous_record.current_state_pbf,
            )
        except:
            Analysis.objects.filter(id=instance.pk).update(
                diffrence_weight=instance.current_state_weight,
                diffrence_bfm=instance.current_state_bfm,
                diffrence_smm=instance.current_state_smm,
                diffrence_pbf=instance.current_state_pbf,
            )
    analysisperson = Analysis.objects.filter(id=instance.analysis_person.id).latest('dot')
    print("XxXxXxXxXxXx", analysisperson.dot)
    lastanalysis = str(analysisperson.dot).split("-")
    monti=int(lastanalysis[1])+1
    if monti>12:
        yeari=int(lastanalysis[0])+1
        monti=monti%12
    else:
        yeari = int(lastanalysis[0])
    person_obj = Person.objects.get(id=instance.analysis_person.id)
    person_obj.nextanalysis=f"{yeari}-{monti}-{lastanalysis[2]}"
    person_obj.save()
