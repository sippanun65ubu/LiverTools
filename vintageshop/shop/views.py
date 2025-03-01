from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm

def product_list(request):
    # Existing filters
    query = request.GET.get('q', '')
    category_filter = request.GET.getlist('category')
    min_price = request.GET.get('min_price')  
    max_price = request.GET.get('max_price')  

    # Base queryset
    products = Product.objects.all()

    # Search filter
    if query:
        products = products.filter(name__icontains=query)

    # Category filter (multiple checkboxes)
    if category_filter:
        products = products.filter(category__in=category_filter)

    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass  

    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass


    categories = Product.objects.values_list('category', flat=True).distinct()

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_categories': category_filter,
        'min_price': min_price,      
        'max_price': max_price,       
    })


def admin_dashboard(request):
    products = Product.objects.all()
    form = ProductForm()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # รีเฟรชหน้าแอดมินหลังเพิ่มสินค้า

    return render(request, 'shop/admin_dashboard.html', {
        'products': products,
        'form': form
    })

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

    return render(request, 'shop/edit_product.html', {
        'form': form,
        'product': product
    })
