from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file_type', 'upload_timestamp',)
    readonly_fields = ('id', 'upload_timestamp')


##need to register the File object in order to show it on the admin page
admin.site.register(File, FileAdmin)