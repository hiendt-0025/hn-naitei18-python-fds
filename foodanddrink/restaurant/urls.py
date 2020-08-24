from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/inform/', views.inform, name='inform'),
    path('register/success_activation/', views.success_activation, name='success_activation'),
    path('register/fail_activation/', views.fail_activation, name='fail_activation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('accounts/profile/', views.profile, name='profile'),

]
