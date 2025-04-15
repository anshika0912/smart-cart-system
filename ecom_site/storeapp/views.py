from django.shortcuts import render

# Create your views here.
# 4. views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem
from .forms import ProductForm
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import User


from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # This will log out the user
    return redirect('home')  # Redirect to the home page after logging out
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})
# storeapp/views.py
from django.shortcuts import render
from .models import CartItem

from .models import Product  # Assuming you have a Product model
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.contrib.auth.models import User

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send confirmation email
            send_mail(
                subject='Welcome to Our Store!',
                message=f'Hi {user.username},\n\nThank you for registering at our store!',
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})
def product_list(request):
    products = Product.objects.all()  # Get all products from the database
    return render(request, 'store/product_list.html', {'products': products})
def checkout(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal
    }
    return render(request, 'store/checkout.html', context)


from django.http import HttpResponse

def place_order(request):
    if request.method == 'POST':
        # You can later save order data here
        return HttpResponse("Order placed successfully!")
    else:
        return HttpResponse("Invalid request method.")

def view_cart(request):
    ...
    return render(request, 'store/cart.html', ...)

# Featured Products View
def home(request):
    featured = Product.objects.filter(is_featured=True)
    return render(request, 'store/home.html', {'featured': featured})

# Product Details View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# Create Product
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form})

@require_POST
def update_cart_quantity(request, item_id):
    action = request.POST.get('action')
    item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
    
    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    item.save()
    return redirect('view_cart')

@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, session_key=request.session.session_key)
    item.delete()
    return redirect('view_cart')

# Delete Product
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'store/product_confirm_delete.html', {'product': product})

# Cart Views
def add_to_cart(request, product_id):
    session_key = request.session.session_key or request.session.save() or request.session.session_key
    product = get_object_or_404(Product, pk=product_id)
    item, created = CartItem.objects.get_or_create(product=product, session_key=session_key)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('view_cart')

def view_cart(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})