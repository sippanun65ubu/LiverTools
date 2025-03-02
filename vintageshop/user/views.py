from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, EditProfileForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Address


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "สมัครสมาชิกสำเร็จ! กรุณาเข้าสู่ระบบ")
            return redirect("login")  # ✅ ไปหน้า Login หลังสมัครเสร็จ
        else:
            print(form.errors)  # 🔥 Debug: แสดงข้อผิดพลาดของฟอร์มใน Terminal

    else:
        form = CustomUserCreationForm()

    return render(request, "user/register.html", {"form": form})


from .forms import EmailAuthenticationForm

def user_login(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")  # ✅ รับค่าอีเมลจากฟอร์ม
            password = form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password)  # ✅ ใช้ email แทน username

            if user is not None:
                login(request, user)
                messages.success(request, "เข้าสู่ระบบสำเร็จ!")
                return redirect("admin_dashboard" if user.is_superuser else "product_list")
        
        messages.error(request, "อีเมลหรือรหัสผ่านไม่ถูกต้อง")

    form = EmailAuthenticationForm()
    return render(request, "user/login.html", {"form": form})

# 🔹 ฟังก์ชันออกจากระบบ
def user_logout(request):
    logout(request)
    return redirect("product_list")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขโปรไฟล์สำเร็จ!")
            return redirect("edit_profile")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "user/edit_profile.html", {"form": form})

from .forms import AddressForm

@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "ที่อยู่ของคุณถูกบันทึกเรียบร้อยแล้ว!")
            return redirect("product_list")  # เปลี่ยนไปหน้ารายการสินค้า
    else:
        form = AddressForm(instance=request.user)

    return render(request, "user/add_address.html", {"form": form})


@login_required
def edit_address(request):
    if request.method == "POST":
        form = AddressForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "ที่อยู่ของคุณถูกอัปเดตเรียบร้อยแล้ว!")
            return redirect("edit_address")  
    else:
        form = AddressForm(instance=request.user)

    return render(request, "user/edit_address.html", {"form": form})


@login_required
def address_list(request):
    addresses = request.user.addresses.all()  # using related_name="addresses"
    
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address_obj = form.save(commit=False)
            address_obj.user = request.user
            address_obj.save()
            return redirect('address_list')
    else:
        form = AddressForm()
        
    return render(request, 'user/address_list.html', {
        'addresses': addresses,
        'form': form,
    })

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    return redirect('address_list')