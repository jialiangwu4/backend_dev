from django import forms
from .models import File

class UploadForm(forms.ModelForm):
    
    # override the init method, add user object. 
    # note: the object needs to be passed in from the view
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) # get the user object 
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        model = super().save(commit=False) # get the model object without saving
        if self.user.is_authenticated: # check authentication
            model.user = self.user # assign the user to the model field - user
        if commit:
            model.save()
        return model # return the model and call save() in the view
        
    class Meta:
        model = File
        fields = ['name', 'file']
        labels = {
            'name': 'File Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'filename'})
        }