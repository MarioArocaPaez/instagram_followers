from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_files, name='upload_files'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
]
