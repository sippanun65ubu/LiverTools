from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ล็อกอินอัตโนมัติหลังสมัคร
            messages.success(request, "สมัครสมาชิกสำเร็จ!")
            return redirect("product_list")  # ไปหน้าหลัก
    else:
        form = CustomUserCreationForm()
    
    return render(request, "user/register.html", {"form": form})
# 🔹 ฟังก์ชันเข้าสู่ระบบ
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect("admin_dashboard")  # ถ้าเป็นแอดมินไปหน้า Admin Dashboard
                else:
                    return redirect("product_list")  # ถ้าเป็นสมาชิกทั่วไปไปหน้าสินค้า
        messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    
    form = AuthenticationForm()
    return render(request, "user/login.html", {"form": form})

# 🔹 ฟังก์ชันออกจากระบบ
def user_logout(request):
    logout(request)
    return redirect("product_list")
