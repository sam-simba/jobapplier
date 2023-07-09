from django import forms
from  django.forms import ModelForm
from .models import Job

class ApplicationForm(forms.Form):
    # resume = forms.FileField()
    userEmail = forms.EmailField(max_length=100, label='Email')

class JobPostForm(ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ['applicants', 'posted', 'hiring_mgr'] 
