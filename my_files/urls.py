from django.urls import path, include
from my_files import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
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
