from django import forms
from django.core.validators import FileExtensionValidator
from datetime import date


class UploadFileForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today())
    file = forms.FileField(label="Add file")