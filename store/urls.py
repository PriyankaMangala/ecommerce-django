from django.urls import path
from . import views

urlpatterns = [
    # ---------- Website Pages ----------
    path('', views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.view_orders, name='view_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # ---------- Authentication ----------
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # ---------- API Endpoints ----------
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/<int:id>/', views.api_product_detail, name='api_product_detail'),
    path('api/checkout/', views.api_checkout, name='api_checkout'),
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/orders/<int:order_id>/cancel/', views.api_cancel_order, name='api_cancel_order'),
]