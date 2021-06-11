from django import forms
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    library = forms.CharField(label="library", min_length=1, max_length=50, disabled=True)
    date = forms.DateField()
    file = forms.FileField(label="Add file", validators=[FileExtensionValidator(allowed_extensions=['csv'])])