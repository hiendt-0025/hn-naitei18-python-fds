from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import SearchResultsView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register/inform/', views.inform, name='inform'),
    path('register/success_activation/', views.success_activation, name='success_activation'),
    path('register/fail_activation/', views.fail_activation, name='fail_activation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit', views.updateProfile, name='edit_profile'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product_details'),
    path('add/<int:pk>/',views.cart_add, name='add_to_cart'),
    path('order/',views.cart_detail, name='order'),
    path('item_clear/<int:pk>/',views.item_clear,name='item_clear'),
    path('make_order/',views.make_order,name='make_order'),
    path('item_increment/<int:pk>/',views.item_increment,name='item_increment'),
    path('item_decrement/<int:pk>/', views.item_decrement, name='item_decrement'),
    path('order/<int:pk>/',views.order_detail_view, name='order'),
    path('order/<int:pk>/<int:pk2>',views.delete_a_product, name='delete_a_product'),
    path('addcomment/<int:pk>', views.addcomment, name='addcomment'),
    path('category/<int:pk>', views.product_by_category, name='product_by_category'),
    path('review/<int:pk>', views.review_product, name='review_product'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('category/<int:pk>/price/', views.filter_price, name='filter_price'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
