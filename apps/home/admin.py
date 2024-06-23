# -*- encoding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib import admin
from .models import Person, SportField, Peyment, SessionDate, Classi, AbsenceDate, Analysis, ValidAbsenceDate, Insurance, AttendanceSheet
from django.db.models.signals import post_save
from .forms import PeymentForm, SessionForm, ClassiForm, InsuranceForm , AnalysisForm
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
    list_display = ['id', 'weekdays', 'cname', 'starttime','ctrainer','fee','cgender']
    form = ClassiForm
    search_fields = ['session_person__full_name']


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'analysis_person','dot']
    form = AnalysisForm
    model = Analysis
    #list_filter = ['analysis_person']
    #search_fields = ['analysis_person__full_name']


@admin.register(AbsenceDate)
class AbsenceDateAdmin(admin.ModelAdmin):
    list_display = ['id','absent_person', 'doa']
    search_fields = ['absent_person__full_name']
    list_filter = ['doa']

##
@admin.register(ValidAbsenceDate)
class ValidAbsenceDateAdmin(admin.ModelAdmin):
    list_display = ['id','vabsent_person', 'dova']
    search_fields = ['vabsent_person__full_name']
    list_filter = ['dova']


@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(admin.ModelAdmin):
    list_display = ['id', 'aname', 'aclass']+[f'doa_{i}' for i in range(1, 13)]
    search_fields=['aname']
    list_filter=['aname']
    #filter_horizontal = ['aperson']
    
    def get_person_display(self, obj):
        return ", ".join(person.full_name for person in obj.person.all())
    get_person_display.short_description = 'Persons'
    
    
 ################## Actions Part ####################
    
    
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
        Analysis.objects.create(analysis_person=instance,dot=jdatetime.datetime.now())


@receiver(post_save, sender=Analysis)
def AnalysysAction( instance, created, **kwargs):
    Analysis.objects.filter(id=instance.pk).update(
    current_state_pbf = instance.current_state_bfm/instance.current_state_weight,
    point_state_pbf = instance.point_state_bfm/instance.point_state_weight)

    if created:

        try:
            personID=(instance.analysis_person.id)
            previous_record = Analysis.objects.filter(
                analysis_person__pk=personID).order_by('dot').exclude(pk=instance.pk).last()
            Analysis.objects.filter(id=instance.pk).update(
                    diffrence_weight = instance.current_state_weight-previous_record.   current_state_weight,
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
        lastanalysis = str(instance.dot).split("-")
        monti = int(lastanalysis[1])+1
        if monti>12:
            yeari=int(lastanalysis[0])+1
            monti=monti%12
        else:
            yeari = int(lastanalysis[0])
        
        person_obj = Person.objects.get(id=instance.analysis_person.id)
        person_obj.nextanalysis=f"{yeari}-{monti}-{lastanalysis[2]}"
        person_obj.save()

'''

# your_app/admin.py
from django.contrib import admin
from django.db.models import Model

def prevent_duplicate_items(model_admin, request, obj, form, change):
    """
    Custom function to prevent duplicate items in the admin.
    """
    # Check if an item with the same value exists for today
    item_exists = obj.__class__.objects.filter(your_field=obj.your_field, date_field__date=obj.date_field).exists()

    if not item_exists:
        # Save the item to the database
        obj.save()
    else:
        model_admin.message_user(request, "Item already exists for today.", level=admin.WARNING)

class YourModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        prevent_duplicate_items(self, request, obj, form, change)

# Register your model with the custom admin class
admin.site.register(YourModel, YourModelAdmin)


'''