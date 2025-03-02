from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Address  


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="ชื่อผู้ใช้",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "กรอกชื่อผู้ใช้"}),
        help_text=""  
    )
    full_name = forms.CharField(
        max_length=255, required=True, label="ชื่อ-นามสกุล",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "กรอกชื่อ-นามสกุล"})
    )
    phone_number = forms.CharField(
        max_length=15, required=True, label="เบอร์โทร",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "กรอกเบอร์โทร"})
    )
    email = forms.EmailField(
        required=True, label="อีเมล",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "กรอกอีเมล"})
    )
    password1 = forms.CharField(
        label="รหัสผ่าน",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "กรอกรหัสผ่าน"}),
        help_text="" 
    )
    password2 = forms.CharField(
        label="ยืนยันรหัสผ่าน",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "ยืนยันรหัสผ่าน"}),
        help_text="" 
    )

    class Meta:
        model = CustomUser
        fields = ["username", "full_name", "phone_number", "email", "password1", "password2"]

class EditProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=255, required=True, label="ชื่อ-นามสกุล",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "กรอกชื่อ-นามสกุล"})
    )
    phone_number = forms.CharField(
        max_length=15, required=True, label="เบอร์โทร",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "กรอกเบอร์โทร"})
    )
    email = forms.EmailField(
        required=True, label="อีเมล",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "กรอกอีเมล"})
    )

    class Meta:
        model = CustomUser
        fields = ["full_name", "phone_number", "email"]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'zip_code']
        widgets = {
            'address_line': forms.Textarea(attrs={
                "class": "form-control", 
                "placeholder": "กรอกที่อยู่ของคุณ",
                "rows": 3,
            }),
            'zip_code': forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "กรอกรหัสไปรษณีย์"
            }),
        }

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(required=True, label="อีเมล",widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "กรอกอีเมล"}))