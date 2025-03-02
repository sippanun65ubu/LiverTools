from django.urls import path
from .views import user_login, user_logout, register, edit_profile, address_list, delete_address

urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", register, name="register"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path('addresses/', address_list, name='address_list'),
    path('addresses/delete/<int:address_id>/', delete_address, name='delete_address'),
]