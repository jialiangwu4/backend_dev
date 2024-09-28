from django import forms
from files.models import File

class UploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']
        labels = {
            'name': 'File Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'filename'})
        }