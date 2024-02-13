
from dal import autocomplete

from django import forms
from .models import Peyment, SessionDate, Classi, Analysis

class PeymentForm(forms.ModelForm):
    class Meta:
        model = Peyment
        fields = ( 'dop','peyment_person','rimage','ncharged','mcharged')
        search_fields = ['do', 'peyment_person']

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
class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ('id', 'analysis_person', 'dot', 'current_state_weight', 'current_state_bfm', 'current_state_smm',
                  'current_state_pbf', 'point_state_weight', 'point_state_bfm', 'point_state_smm', 'point_state_pbf')

        search_fields = ['id', 'analysis_person', 'dot',]

        widgets = {
            'analysis_person': autocomplete.ModelSelect2(url='select2_fk'),
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
