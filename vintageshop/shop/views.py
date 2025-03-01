from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, ChatMessage
from .forms import ProductForm, ChatForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ ใช้ Custom User Model

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

@login_required
def user_chat(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    messages = ChatMessage.objects.filter(
        sender=request.user, receiver=admin_user
    ) | ChatMessage.objects.filter(sender=admin_user, receiver=request.user)
    
    messages = messages.order_by('timestamp')

    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.sender = request.user
            chat_message.receiver = admin_user
            chat_message.save()
            return redirect('user_chat')

    else:
        form = ChatForm()

    return render(request, 'shop/user_chat.html', {'messages': messages, 'form': form})

@login_required
def admin_chat(request):
    if not request.user.is_superuser:
        return redirect('product_list')  # ป้องกัน user ธรรมดาเข้าถึง

    users = User.objects.filter(is_superuser=False)
    selected_user_id = request.GET.get('user')
    selected_user = None
    messages = ChatMessage.objects.none()

    if selected_user_id:
        selected_user = get_object_or_404(User, id=selected_user_id)
        messages = ChatMessage.objects.filter(
            sender=selected_user, receiver=request.user
        ) | ChatMessage.objects.filter(sender=request.user, receiver=selected_user)
        messages = messages.order_by('timestamp')

        # ✅ ตรวจสอบว่ามีการส่งข้อความหรือไม่
        if request.method == "POST":
            message_text = request.POST.get('message')
            if message_text:  # ตรวจสอบว่าข้อความไม่ว่างเปล่า
                ChatMessage.objects.create(
                    sender=request.user,  # ✅ แอดมินเป็นคนส่ง
                    receiver=selected_user,  # ✅ ส่งไปยัง user ที่เลือก
                    message=message_text
                )
                return redirect(f"{request.path}?user={selected_user.id}")  # ✅ Redirect หลังส่ง

    return render(request, 'shop/admin_chat.html', {'users': users, 'messages': messages, 'selected_user': selected_user})

