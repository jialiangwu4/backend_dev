from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    
    def __str__(self):
        return self.name
