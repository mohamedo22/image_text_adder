# imageditor/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView , PasswordChangeView , PasswordChangeDoneView
urlpatterns = [
    path('', views.home, name='home'),
    # path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('download_from_home/', views.download_from_home, name='downloadFromHome'),
    path('login_admin/', views.loginAdmin, name='loginAdmin'),
    path('admin_home/', views.adminHome, name='adminHome'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('settings/change_password/',PasswordChangeView.as_view(template_name='change_password.html'),name='password_change'),
    path('settings/change_password/done/', PasswordChangeDoneView.as_view(template_name = 'changeDone.html'), name='password_change_done'),
    path('change_codes/', views.change_codes, name='changeCodes'),
    path('change_images/', views.change_images, name='changeImages'),
    path('check_code/', views.check_code, name='checkValidCode'),
]
