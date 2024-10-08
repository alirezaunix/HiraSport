
from dal import autocomplete
from django import forms
from .models import Peyment, SessionDate, Classi, Analysis, Person, Insurance, AbsenceDate, ValidAbsenceDate


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = AbsenceDate
        fields = ('classname', 'doa', 'absent_person')
        search_fields = ['absent_person__full_name']
        print("in absence form")
        widgets = {
            'absent_person': autocomplete.ModelSelect2(url='select2_fk'),
        }


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


class AnalysisForm(forms.ModelForm):
    class Meta:

        model = Analysis
        fields = ('dot', 'analysis_person', 'current_state_weight',
                  'current_state_bfm', 'current_state_smm', 'point_state_weight', 'point_state_bfm', 'point_state_smm', 'reportfile')
        search_fields = [ 'analysis_person__full_name']

        widgets = {
            'analysis_person': autocomplete.ModelSelect2(url='select2_fk'),
        }



class ValidAbsenceForm(forms.ModelForm):
    class Meta:
        model = ValidAbsenceDate
        fields = ('classname', 'dova', 'vabsent_person')
        search_fields = ['doa', 'vabsent_person__full_name']

        widgets = {
            'vabsent_person': autocomplete.ModelSelect2(url='select2_fk'),
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
                  'ctrainer', 'fee','cgender']

        widgets = {
            'starttime' : TimePickerInput(),
        }


class AttendanceForm(forms.Form):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('validabsent', ' validAbsent ')
    ]
    attendance = forms.ChoiceField(
        choices=ATTENDANCE_CHOICES, widget=forms.RadioSelect)
