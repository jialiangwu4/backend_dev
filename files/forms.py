from django import forms
from files.models import File

class UploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file_type', 'file']
        labels = {
            'name': 'File Name',
            'file_type': 'File Type',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'filename'})
        }