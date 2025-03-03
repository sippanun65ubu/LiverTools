from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category ,Cart, CartItem, Order, OrderItem, ChatMessage
from .forms import ProductForm, ChatForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.admin.views.decorators import staff_member_required
from user.models import Address
from django.contrib import messages
from django.db import models 

User = get_user_model() 

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
            product = form.save(commit=False)
            if product.quantity == 0:
                messages.error(request, "ไม่สามารถเพิ่มสินค้าที่มีจำนวน 0 ได้")
                return redirect('admin_dashboard')  # ✅ ป้องกันการเพิ่มสินค้า
            product.save()
            messages.success(request, "เพิ่มสินค้าสำเร็จ")
            return redirect('admin_dashboard')

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

    # ✅ ตรวจสอบว่าสินค้ามี stock เพียงพอหรือไม่
    quantity = int(request.POST.get('quantity', 1))
    if product.quantity == 0:
        messages.error(request, "สินค้าไม่มีในสต็อก ไม่สามารถเพิ่มลงตะกร้าได้")
        return redirect('product_list')  # หรือเปลี่ยนไปยังหน้าที่เหมาะสม

    if quantity > product.quantity:
        messages.error(request, f"สินค้าในสต็อกมีเพียง {product.quantity} ชิ้นเท่านั้น")
        return redirect('product_list')

    cart = get_or_create_cart(request.user)

    # ตรวจสอบว่าสินค้านี้มีอยู่ในตะกร้าแล้วหรือไม่
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}  # ตั้งค่าเริ่มต้นถ้ายังไม่มีสินค้า
    )

    if not created:
        # ✅ อัปเดตจำนวนสินค้าในตะกร้า (ห้ามเกิน stock)
        if cart_item.quantity + quantity > product.quantity:
            messages.error(request, f"คุณสามารถเพิ่มได้อีกเพียง {product.quantity - cart_item.quantity} ชิ้นเท่านั้น")
            return redirect('cart_detail')

        cart_item.quantity += quantity  
        cart_item.save()

    # ✅ ลดจำนวน stock ของสินค้า
    product.quantity -= quantity
    product.save()

    messages.success(request, "เพิ่มสินค้าเข้าไปในตะกร้าสำเร็จ!")
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    # ✅ คืนจำนวนสินค้าเข้า stock ก่อนลบออกจากตะกร้า
    product = cart_item.product
    product.quantity += cart_item.quantity
    product.save()

    # ✅ ลบสินค้าออกจากตะกร้า
    cart_item.delete()
    messages.success(request, "ลบสินค้าออกจากตะกร้าและคืนสต็อกสำเร็จ!")

    return redirect('cart_detail')


@login_required
def update_cart_item(request, item_id):
    cart = get_or_create_cart(request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        
        # ✅ เช็คว่าผู้ใช้ลดจำนวนสินค้าหรือไม่
        if new_quantity < cart_item.quantity:
            difference = cart_item.quantity - new_quantity
            cart_item.product.quantity += difference  # ✅ คืนสินค้าเข้า stock
            cart_item.product.save()
        elif new_quantity > cart_item.quantity:
            # ✅ ตรวจสอบว่าสินค้าในสต็อกเพียงพอหรือไม่
            difference = new_quantity - cart_item.quantity
            if difference > cart_item.product.quantity:
                messages.error(request, f"สินค้าในสต็อกมีเพียง {cart_item.product.quantity} ชิ้นเท่านั้น")
                return redirect('cart_detail')

            cart_item.product.quantity -= difference  # ✅ ลดสินค้าใน stock
            cart_item.product.save()

        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, "อัปเดตจำนวนสินค้าในตะกร้าสำเร็จ!")

    return redirect('cart_detail')


@login_required
def checkout(request):
    if request.method == 'POST':
        # ดึงที่อยู่ที่ผู้ใช้เลือกจาก session
        selected_address_id = request.session.get('selected_address_id')
        if not selected_address_id:
            return redirect('select_address')  # บังคับให้เลือกที่อยู่ก่อน Checkout

        # ตรวจสอบว่า Address นี้เป็นของผู้ใช้จริงหรือไม่
        address_obj = get_object_or_404(Address, id=selected_address_id, user=request.user)

        # ดึงข้อมูลตะกร้าของผู้ใช้
        cart = get_or_create_cart(request.user)
        items = cart.items.select_related('product')
        
        if not items.exists():
            return redirect('cart_detail')  # ป้องกันการ Checkout ตะกร้าว่าง

        # ✅ สร้างคำสั่งซื้อใหม่
        order = Order.objects.create(
            user=request.user,
            address_line=address_obj.address_line,  # ✅ ใช้ field ที่ถูกต้อง
            zip_code=address_obj.zip_code
        )

        # ✅ ย้ายสินค้าแต่ละชิ้นจาก Cart -> Order
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # ✅ ลบสินค้าทั้งหมดออกจากตะกร้าหลัง Checkout
        cart.items.all().delete()

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
    # Instead of "completed":
    order.status = "waiting_confirm"
    order.save()
    return redirect('product_list')

@login_required
def payment_status(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # แสดงคำสั่งซื้อล่าสุดก่อน
    
    
    for order in orders:
        total_price = sum(item.quantity * item.price for item in order.items.all())
        order.total_price = total_price  # ✅ เพิ่ม attribute ให้ order (แต่ไม่บันทึกใน DB)

    return render(request, 'shop/payment_status.html', {'orders': orders})

@login_required
def user_chat(request):
    admin_user = User.objects.filter(is_superuser=True).first()  # ✅ ดึงแอดมินคนแรก
    if not admin_user:
        return render(request, 'shop/user_chat.html', {'error': "ไม่พบแอดมิน"})

    messages = ChatMessage.objects.filter(
        sender=request.user, receiver=admin_user
    ) | ChatMessage.objects.filter(sender=admin_user, receiver=request.user)

    messages = messages.order_by('timestamp')  # ✅ เรียงลำดับข้อความเก่า → ใหม่

    if request.method == "POST":
        message_text = request.POST.get('message')
        if message_text:  # ✅ ตรวจสอบว่าข้อความไม่ว่างเปล่า
            ChatMessage.objects.create(
                sender=request.user,  
                receiver=admin_user,  # ✅ สมาชิกส่งไปยังแอดมิน
                message=message_text
            )
            return redirect('user_chat')  # ✅ รีเฟรชหน้าเพื่อแสดงข้อความล่าสุด

    return render(request, 'shop/user_chat.html', {'messages': messages})


@login_required
def admin_chat(request):
    if not request.user.is_superuser:
        return redirect('product_list')  # ✅ ป้องกัน user ธรรมดาเข้าถึง

    users = User.objects.filter(is_superuser=False)  # ✅ ดึงเฉพาะสมาชิกที่ไม่ใช่แอดมิน
    selected_user_id = request.GET.get('user')
    selected_user = None
    messages = ChatMessage.objects.none()

    if selected_user_id:
        selected_user = get_object_or_404(User, id=selected_user_id)
        messages = ChatMessage.objects.filter(
            sender=selected_user, receiver=request.user
        ) | ChatMessage.objects.filter(sender=request.user, receiver=selected_user)

        messages = messages.order_by('timestamp')

        if request.method == "POST":
            message_text = request.POST.get('message')
            if message_text:
                ChatMessage.objects.create(
                    sender=request.user,  
                    receiver=selected_user,  # ✅ แอดมินส่งไปยังสมาชิก
                    message=message_text
                )
                return redirect(f"{request.path}?user={selected_user.id}")  # ✅ รีเฟรชหน้าเพื่อแสดงข้อความใหม่

    return render(request, 'shop/admin_chat.html', {
        'users': users,
        'messages': messages,
        'selected_user': selected_user
    })


@login_required
@staff_member_required
def admin_order_list(request):
    """แสดงรายการคำสั่งซื้อ พร้อมเรียงลำดับให้คำสั่งซื้อที่ยังไม่อนุมัติอยู่บนสุด"""
    
    orders = Order.objects.all().order_by(
        # ✅ นำ waiting_confirm ไว้บนสุด
        models.Case(
            models.When(status="waiting_confirm", then=0),
            models.When(status="approved", then=1),
            models.When(status="rejected", then=2),
            default=3, output_field=models.IntegerField(),
        ),
        # ✅ จากนั้นเรียงตามวันที่ (ล่าสุดขึ้นก่อน)
        "-created_at"
    )

    # ✅ คำนวณราคารวมของแต่ละออเดอร์
    for order in orders:
        total_price = sum(item.quantity * item.price for item in order.items.all())
        order.total_price = total_price

    return render(request, 'shop/admin_order_list.html', {'orders': orders})




@login_required
@staff_member_required
def admin_confirm_payment(request, order_id):
    """Admin view to confirm (approve) a user's payment."""
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        # For example, set status to approved (or completed)
        order.status = "approved"
        order.save()
        return redirect('admin_order_list')
    return render(request, 'shop/admin_confirm_payment.html', {'order': order})

@login_required
@staff_member_required
def admin_reject_payment(request, order_id):
    """Admin view to reject a user's payment."""
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        # e.g., set status to rejected
        order.status = "rejected"
        order.save()
        return redirect('admin_order_list')
    
    # If GET request, show a simple confirmation page
    return render(request, 'shop/admin_reject_payment.html', {'order': order})


@login_required
def select_address(request):
    # Retrieve all addresses for the logged-in user
    addresses = request.user.addresses.all()

    if request.method == 'POST':
        # Suppose the user picks an address via radio buttons or a dropdown
        selected_address_id = request.POST.get('address_id')
        if selected_address_id:
            request.session['selected_address_id'] = selected_address_id
            return redirect('checkout')  # Move to the checkout step
    return render(request, 'shop/select_address.html', {'addresses': addresses})
