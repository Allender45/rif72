from django.urls import path, include

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('view/', view, name='view'),
    path('products/<str:slug>/', product_view, name='product_detail'),
    path('category/<str:slug>/', category_view, name='category_detail'),
    path('sub_category/<str:slug>/', sub_category_view, name='sub_category_detail'),
    path('cart/', cart_view, name='cart'),
    path('add_to_cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete_from_cart/<str:slug>/<str:cart_id>/', delete_from_cart, name='delete_from_cart'),
    path('change_qty/<str:slug>/<str:cart_id>/', change_qty, name='change_qty'),
    path('checkout/', checkout, name='checkout'),
    path('checkout_post/', checkout_post, name='checkout_post'),
    path('blog/', blog, name='blog'),
    path('blog/<str:slug>/', blog_detail, name='blog_detail'),
]