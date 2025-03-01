from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category ,Cart, CartItem, Order, OrderItem
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

def product_list(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.getlist('category')
    size_filter = request.GET.getlist('size')  # New filter for size
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    
    if query:
        products = products.filter(name__icontains=query)
    if category_filter:
        products = products.filter(category__id__in=category_filter).distinct()
    if size_filter:
        products = products.filter(size__in=size_filter)
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

    categories = Category.objects.all()  # Use Category model
    size_choices = Product.SIZE_CHOICES

    # Calculate cart information if the user is authenticated.
    cart_items_count = 0
    cart_total_price = 0
    if request.user.is_authenticated:
        cart = get_or_create_cart(request.user)  # This helper should return a Cart object.
        for item in cart.items.all():
            cart_items_count += item.quantity
            cart_total_price += item.product.price * item.quantity

    context = {
        'products': products,
        'categories': categories,
        'selected_categories': category_filter,
        'min_price': min_price,
        'max_price': max_price,
        'size_choices': size_choices,
        'selected_sizes': size_filter,
        'cart_items_count': cart_items_count, 
        'cart_total_price': cart_total_price, 
    }
    return render(request, 'shop/product_list.html', context)


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
@login_required
def cart_detail(request):
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product')
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart = get_or_create_cart(request.user)

    # ตรวจสอบว่าสินค้านี้มีอยู่ในตะกร้าแล้วหรือไม่
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}  # ตั้งค่าเริ่มต้นถ้ายังไม่มีสินค้า
    )

    if not created:
        cart_item.quantity += quantity  # ถ้ามีอยู่แล้วให้เพิ่มจำนวนสินค้า
        cart_item.save()

    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()
    
    return redirect('cart_detail')

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = get_or_create_cart(request.user)
        items = cart.items.select_related('product')

        if not items.exists():
            return redirect('cart_detail')

        # สร้างคำสั่งซื้อ
        order = Order.objects.create(user=request.user)

        # ย้ายสินค้าจากตะกร้ามาเป็นคำสั่งซื้อ
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            # ลดจำนวนสินค้าในสต็อก
            item.product.quantity -= item.quantity
            item.product.save()

        # ลบตะกร้าสินค้า
        items.delete()

        # ไปหน้าคำสั่งซื้อสำเร็จ
        return redirect('order_success', order_id=order.id)

    return redirect('cart_detail')

@login_required
def upload_payment_slip(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST' and 'payment_slip' in request.FILES:
        order.payment_slip = request.FILES['payment_slip']
        order.save()
        return redirect('order_success', order_id=order.id)

    return render(request, 'shop/upload_slip.html', {'order': order})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})

def get_or_create_cart(user):
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=user)
        return cart
    else:
        # For anonymous users, you could store a cart ID in session, etc.
        # Or create a Cart with user=None
        cart = Cart.objects.create(user=None)
        return cart

def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # อัปเดตสถานะคำสั่งซื้อให้เป็น 'เสร็จสิ้น'
    order.status = "completed"
    order.save()

    return redirect('product_list')  # กลับไปยังหน้าแรกหลังจากทำรายการเสร็จ

@login_required
def payment_status(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # แสดงคำสั่งซื้อล่าสุดก่อน
    return render(request, 'shop/payment_status.html', {'orders': orders})
