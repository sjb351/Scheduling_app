from .models import order
from input.models import product, proccessesList, proccess
from django import forms

# class jobForm(forms.ModelForm):
#     class Meta:
#         model = jobData
#         fields = ('jobName', 'length', 'startedTime')

   # def clean_title(self):
    #    title = self.cleaned_data('jobName')

class orderForm(forms.ModelForm):
    class Meta:
        model = order
        fields = ['idNumber', 'productAdd', 'quantity']
        # widgets = {
        #     'productAdd':forms.Select(choices=product.objects.all())
        # }
    def create_new(self):
        print(self)

