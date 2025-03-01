from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    """ แสดงรายการสินค้าพร้อมฟีเจอร์ค้นหาและกรองตามหมวดหมู่ """
    query = request.GET.get('q', '')  # ค้นหาสินค้า
    category_filter = request.GET.getlist('category')  # กรองตามหมวดหมู่
    min_price = request.GET.get('min_price')  
    max_price = request.GET.get('max_price')  

    products = Product.objects.all()

    # 🔹 ค้นหาสินค้าตามชื่อ
    if query:
        products = products.filter(name__icontains=query)

    # 🔹 กรองสินค้าตามหมวดหมู่ (ต้องเป็น instance ของ `Category`)
    if category_filter:
        products = products.filter(category__name__in=category_filter)

    # 🔹 กรองราคาต่ำสุด
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass  

    # 🔹 กรองราคาสูงสุด
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # 🔹 ดึงหมวดหมู่ทั้งหมดที่มีอยู่
    categories = Category.objects.all()

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_categories': category_filter,
        'min_price': min_price,      
        'max_price': max_price,       
    })


def admin_dashboard(request):
    """ แสดงหน้า Admin Dashboard พร้อมฟอร์มเพิ่มสินค้าและรายการสินค้า """
    products = Product.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)

            # 🔹 ตรวจสอบว่ามีการกรอกหมวดหมู่ใหม่หรือไม่
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                category_obj, created = Category.objects.get_or_create(name=new_category_name)
                product.category = category_obj  # ✅ กำหนดให้เป็น instance ของ `Category`
            
            product.save()
            return redirect('admin_dashboard')  # รีเฟรชหน้าแอดมินหลังเพิ่มสินค้า
    else:
        form = ProductForm()

    return render(request, 'shop/admin_dashboard.html', {
        'products': products,
        'form': form
    })


def delete_product(request, product_id):
    """ ลบสินค้าตาม product_id """
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('admin_dashboard')


def edit_product(request, product_id):
    """ แก้ไขสินค้าตาม product_id """
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)

            # 🔹 ตรวจสอบว่ามีการเปลี่ยนหมวดหมู่ใหม่หรือไม่
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                category_obj, created = Category.objects.get_or_create(name=new_category_name)
                product.category = category_obj  # ✅ กำหนดให้เป็น instance ของ `Category`

            product.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {
        'form': form,
        'product': product
    })
