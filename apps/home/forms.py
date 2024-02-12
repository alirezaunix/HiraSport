
from dal import autocomplete

from django import forms
from .models import Peyment,SessionDate,Classi

class PeymentForm(forms.ModelForm):
    class Meta:
        model = Peyment
        fields = ( 'dop','peyment_person','rimage','ncharged','mcharged')
        widgets = {
            'peyment_person': autocomplete.ModelSelect2(url='select2_fk'), 
        }
        
class SessionForm(forms.ModelForm):
    class Meta:
        model=SessionDate
        fields=('dos','session_person')
        search_fields=['dos','session_person']

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
        fields = ['cname', 'weekdays', 'starttime','tname']

        widgets = {
            'starttime' : TimePickerInput(),
        }
