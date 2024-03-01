# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib import admin
from .models import Person, SportField, Peyment, SessionDate, Classi, Trainer, AbsenceDate,Analysis,TrainerSeesion
from django.db.models.signals import post_save
from .forms import PeymentForm, SessionForm, ClassiForm #AnalysisForm
from django.dispatch import receiver
from django.contrib.auth.models import User
import jdatetime


    
    
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ['id', 'tsport', 'tfull_name', 'tphone']
    search_field = ['tfull_name']
    list_filter = ['tsport']


@admin.register(TrainerSeesion)
class TrainerSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_trainer', 'dos_trainer', 'class_trainer']
    search_field = ['session_trainer']
    list_filter = ['session_trainer']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', "ncode",  "scode",   "dob",
                    "gender", "classname", "sfield", "rsession", 'username', 'password']
    search_fields = ['first_name', 'last_name']
    list_filter = ['classname', 'gender', 'sfield']


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
    list_display = ['id', 'analysis_person']
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
    person_obj = Person.objects.filter(first_name__contains=str(instance.peyment_person).split(
        " ")[0], last_name__contains=str(instance.peyment_person).split(" ")[1])
    current_value = list(person_obj.values())[0]['rsession']
    person_obj.update(rsession=current_value+instance.ncharged)


@receiver(post_save, sender=SessionDate)
def SessionAction(instance, **kwarg):
    person_obj = Person.objects.filter(first_name__contains=str(instance.session_person).split(
        " ")[0], last_name__contains=str(instance.session_person).split(" ")[1])
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
        previous_record = Analysis.objects.filter(
            pk__lt=instance.pk , analysis_person= instance.analysis_person).latest('pk')
        Analysis.objects.filter(id=instance.pk).update(
            diffrence_weight = instance.current_state_weight-previous_record.current_state_weight,
            diffrence_bfm=instance.current_state_bfm-previous_record.current_state_bfm,
            diffrence_smm=instance.current_state_smm-previous_record.current_state_smm,
            diffrence_pbf=instance.current_state_pbf-previous_record.current_state_pbf,
        )
