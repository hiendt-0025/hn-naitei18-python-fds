from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/inform/', views.inform, name='inform'),
    path('register/success_activation/', views.success_activation, name='success_activation'),
    path('register/fail_activation/', views.fail_activation, name='fail_activation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('accounts/profile/', views.profile, name='profile'),

    path('order/<int:pk>/',views.order_detail_view, name='order'),
    path('order/<int:pk>/<int:pk2>',views.delete_a_product, name='delete_a_product')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
