from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.view_cart, name='view_cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/add/', views.product_create, name='product_create'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # Add the product list URL here
    path('products/', views.product_list, name='product_list'),  # ✅ Add this line
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),  # Ensure this is correct
    path('logout/', views.logout_view, name='logout'),

]
