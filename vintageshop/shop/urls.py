from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'), 
    path('chat/', views.user_chat, name='user_chat'),
    path('admin-chat/', views.admin_chat, name='admin_chat'),  # ✅ แก้ path เป็น 'admin-chat/'
]
