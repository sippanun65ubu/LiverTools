from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # หน้าแสดงสินค้า
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'), 
]
