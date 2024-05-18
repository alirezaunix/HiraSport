
from dal import autocomplete
from django import forms
from .models import Peyment, SessionDate, Classi, Analysis, Person, Insurance

class PeymentForm(forms.ModelForm):
    class Meta:
        model = Peyment
        fields = ( 'dop','peyment_person','rimage','ncharged','mcharged')
        search_fields = ['peyment_person__full_name']

        widgets = {
            'peyment_person': autocomplete.ModelSelect2(url='select2_fk'),
        }


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ('dop', 'insurance_person', 'rimage',
                   'mcharged', 'nextiInsurancedate')
        search_fields = ['dop', 'insurance_person__full_name']

        widgets = {
            'insurance_person': autocomplete.ModelSelect2(url='select2_fk'),
        }


        
class SessionForm(forms.ModelForm):
    class Meta:
        model=SessionDate
        fields=('dos','session_person','classname')
        search_fields = ['dos', 'session_person__full_name']

        widgets = {
            'session_person': autocomplete.ModelSelect2(url='select2_fk'), 
        }



        
class TimePickerInput(forms.TimeInput):
        input_type = 'time'


class ExampleForm(forms.Form):
        my_time_field = forms.TimeField(widget=TimePickerInput)
        
        
        
class ClassiForm(forms.ModelForm):
    class Meta:
        model = Classi
        fields = ['cname', 'weekdays', 'starttime',
                  'ctrainer', 'fee']

        widgets = {
            'starttime' : TimePickerInput(),
        }
