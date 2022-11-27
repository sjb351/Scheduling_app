from .models import product, proccess, proccessesList
from django import forms
from django_flatpickr.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


class productForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ('name',)

class processListForma(forms.Form):
    process = forms.ModelMultipleChoiceField(queryset=proccess.objects.all())

DAY_CHOICES= [tuple([x,x]) for x in range(1,25)]
MONTH_CHOICES= [tuple([x,x]) for x in range(1,13)]

class processForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput)
    duration = forms.DurationField(widget = forms.TimeInput())
    delayTime = forms.DurationField(widget = forms.TimeInput())
    startTime = forms.DateTimeField(widget=DateTimePickerInput())
    downTime = forms.DurationField(widget = forms.TimeInput())
    
    # 'time': forms.TimeInput(attrs={'type': 'time'})
    # class Meta:
    #     model = proccess
    #     fields = ('name', 'duration', 'startTime', 'delayTime','setUpTime', 'downTime',)
    #     labels = {
    #         'name':'Process',
    #         'duration':'Job duration',
    #         'startTime':'Process start at',
    #         'dealyTimes':'Time delay:',
    #     }
    #     widgets = {
    #         'duration': forms.TimeInput(attrs={'type': 'time'}),
    #         'startTime': forms.TimeInput(attrs={'type': 'time'}),
    #         'delayTime': forms.TimeInput(attrs={'type': 'time'}),
    #         'setUpTime': forms.TimeInput(attrs={'type': 'time'})
    #     }
