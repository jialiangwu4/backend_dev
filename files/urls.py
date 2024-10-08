"""
URL configuration for files project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from files import views, settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.index, name='index'),
    path('files/', views.files, name='files'),
    path('files/<int:file_id>/', views.file, name='file'),
    path('files/edit/<int:file_id>/', views.edit, name='edit'),
    path('files/delete/<int:file_id>/', views.delete, name='delete'),
    path('files/upload/', views.upload, name='upload'),
    path('files/upload/create/', views.create, name='create'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    # rest api endpoints 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/files/', views.files_api, name='files_api'),
    path('api/files/<int:file_id>/', views.file_api, name='file_api'),
    path('api/files/upload/', views.upload_api, name='upload_api'),
    path('api/register/', views.register_api, name='register_api'),
]

# add the media path to the static files - local
# urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

# support .json url suffix
urlpatterns = format_suffix_patterns(urlpatterns)