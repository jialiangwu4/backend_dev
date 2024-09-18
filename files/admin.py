from django.contrib import admin
from .models import File

##need to register the File object in order to show it on the admin page
admin.site.register(File)