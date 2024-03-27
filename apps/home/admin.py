# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib import admin
from .models import Person, SportField, Peyment, SessionDate, Classi, AbsenceDate,Analysis
from django.db.models.signals import post_save
from .forms import PeymentForm, SessionForm, ClassiForm #AnalysisForm
from django.dispatch import receiver
from django.contrib.auth.models import User
import jdatetime
from django import forms



'''
    
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['id', 'tsport', 'tfull_name', 'tphone']
    search_field = ['tfull_name']
    list_filter = ['tsport']
'''
'''
@admin.register(TrainerSeesion)
class TrainerSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_trainer', 'dos_trainer', 'class_trainer']
    search_field = ['session_trainer']
    list_filter = ['session_trainer']
'''

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
    search_fields = ['peyment_person']


@admin.register(SessionDate)
class SessionDateAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_person', 'dos']
    form = SessionForm
    model = SessionDate


@admin.register(Classi)
class ClassiAdmin(admin.ModelAdmin):
    list_display = ['id', 'weekdays', 'cname', 'starttime',]
    form = ClassiForm
    search_fields = ['session_person']


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'analysis_person','dot']
    #form = AnalysisForm
    #model = Analysis
    list_filter = ['analysis_person']
    search_fields = ['analysis_person']


@admin.register(AbsenceDate)
class AbsenceDateAdmin(admin.ModelAdmin):
    list_display = ['absent_person', 'doa']
    search_fields = ['absent_person']
    list_filter = ['doa']


@receiver(post_save, sender=AbsenceDate)
def AbsenceAction(instance, **kwargs):
    person_obj = Person.objects.filter(
        username__contains=str(instance.absent_person).split(" ")[0])
    n_absence = len(AbsenceDate.objects.all())
    current_value = list(person_obj.values())[0]['rsession']
    person_obj.update(rsession=current_value-1)


@receiver(post_save, sender=Peyment)
def PeymentAction(instance, **kwargs):
    person_obj = Person.objects.filter(full_name__contains=str(instance.peyment_person).split(
        " ")[0])
    current_value = list(person_obj.values())[0]['rsession']
    person_obj.update(rsession=current_value+instance.ncharged)


@receiver(post_save, sender=SessionDate)
def SessionAction(instance, **kwarg):
    person_obj = Person.objects.filter(full_name__contains=str(instance.session_person).split(
        " ")[0])
    current_value = list(person_obj.values())[0]['rsession']
    person_obj.update(rsession=current_value-1)

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
                pk__lt=instance.pk , analysis_person= instance.analysis_person).latest('pk')
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
    analysisperson = Analysis.objects.filter(analysis_person=instance.analysis_person).latest('dot')
    print("XxXxXxXxXxXx", analysisperson.dot)
    lastanalysis = str(analysisperson.dot).split("-")
    monti=int(lastanalysis[1])+1
    if monti>12:
        yeari=int(lastanalysis[0])+1
        monti=monti%12
    else:
        yeari = int(lastanalysis[0])
    person_obj = Person.objects.filter(full_name__contains=str(instance.analysis_person).split(
        " ")[0])
    person_obj.update(nextanalysis=f"{yeari}-{monti}-{lastanalysis[2]}")
