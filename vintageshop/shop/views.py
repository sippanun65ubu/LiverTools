from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm

def product_list(request):
    query = request.GET.get('q', '')
    # Get a list of category IDs from GET parameters (they come as strings)
    category_filter = request.GET.getlist('category')
    min_price = request.GET.get('min_price')  
    max_price = request.GET.get('max_price')  

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_filter:
        # Filter products that have at least one of the selected categories
        products = products.filter(category__id__in=category_filter).distinct()

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

    # Get all categories for the sidebar filter
    categories = Category.objects.all()

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
