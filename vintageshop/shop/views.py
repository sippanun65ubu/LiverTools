from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def product_list(request):
    # 🔹 รับค่าจาก URL parameter
    query = request.GET.get('q', '')  # ค่าค้นหาสินค้า
    category_filter = request.GET.get('category', '')  # หมวดหมู่สินค้า

    # 🔹 ดึงสินค้าทั้งหมด
    products = Product.objects.all()

    # 🔹 ถ้ามีการค้นหา ให้กรองสินค้าที่ชื่อคล้ายกัน
    if query:
        products = products.filter(name__icontains=query)

    # 🔹 ถ้ามีการเลือกประเภทสินค้า ให้กรองเฉพาะประเภทนั้น
    if category_filter:
        products = products.filter(category=category_filter)

    # 🔹 ดึงรายชื่อหมวดหมู่ทั้งหมด
    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
    })

def admin_dashboard(request):
    products = Product.objects.all()
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # รีเฟรชหน้าแอดมินหลังเพิ่มสินค้า

    return render(request, 'shop/admin_dashboard.html', {'products': products, 'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_dashboard')

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})