# imageditor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('download_from_home/', views.download_from_home, name='downloadFromHome'),
]
