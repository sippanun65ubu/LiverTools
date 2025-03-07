from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'), 
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'), 
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('upload-payment-slip/<int:order_id>/', views.upload_payment_slip, name='upload_payment_slip'),
    path('order-complete/<int:order_id>/', views.order_complete, name='order_complete'),
    path('payment-status/', views.payment_status, name='payment_status'),
    path('chat/', views.user_chat, name='user_chat'),
    path('admin-chat/', views.admin_chat, name='admin_chat'), 
    path('admin-orders/', views.admin_order_list, name='admin_order_list'),
    path('admin-orders/confirm/<int:order_id>/', views.admin_confirm_payment, name='admin_confirm_payment'),
    path('admin-orders/reject/<int:order_id>/', views.admin_reject_payment, name='admin_reject_payment'),
    path('select-address/', views.select_address, name='select_address'),
    path('checkout/', views.checkout, name='checkout'),
]


