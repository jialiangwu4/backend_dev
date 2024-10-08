from django.contrib import admin
from .models import File


class FileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'name', 'upload_timestamp',)
    readonly_fields = ('id', 'upload_timestamp')
    
    # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_model
    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)


##need to register the File object in order to show it on the admin page
admin.site.register(File, FileAdmin)