from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True, label="ชื่อ-นามสกุล")
    phone_number = forms.CharField(max_length=15, required=True, label="เบอร์โทร")
    email = forms.EmailField(required=True, label="อีเมล")

    class Meta:
        model = CustomUser
        fields = ["username", "full_name", "phone_number", "email", "password1", "password2"]
