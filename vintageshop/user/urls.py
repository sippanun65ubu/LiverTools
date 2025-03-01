from django.urls import path
from .views import user_login, user_logout, register, edit_profile, add_address, edit_address

urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", register, name="register"),
    path("edit-profile/", edit_profile, name="edit_profile"),
    path("add-address/", add_address, name="add_address"),
    path("edit-address/", edit_address, name="edit_address"),
]