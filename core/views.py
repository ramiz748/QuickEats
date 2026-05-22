from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import FoodItem, Category, Cart, CartItem, Order, OrderItem
from .forms import RegisterForm, CheckoutForm


def home(request):
    categories = Category.objects.all()
    featured = FoodItem.objects.filter(is_available=True)[:6]
    return render(request, 'home.html', {'categories': categories, 'featured': featured})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('menu')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cart.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created! Welcome.')
            return redirect('menu')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('menu')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            Cart.objects.get_or_create(user=user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('menu')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')

def menu_view(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    q = request.GET.get('q', '')
    if category_id:
        food_items = FoodItem.objects.filter(category_id=category_id, is_available=True)
        active_cat = int(category_id)
    else:
        food_items = FoodItem.objects.filter(is_available=True)
        active_cat = None
    if q:
        food_items = food_items.filter(name__icontains=q)
    return render(request, 'menu.html', {
        'food_items': food_items,
        'categories': categories,
        'active_cat': active_cat,
    })


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.select_related('food_item').all()
    return render(request, 'cart.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, id=food_id, is_available=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food_item=food)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'"{food.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'menu'))


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cart_items.all()

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone']
            payment_method = form.cleaned_data['payment_method']

            order = Order.objects.create(
                user=request.user,
                total_amount=cart.get_total(),
                address=address,
                phone=phone,
                payment_method=payment_method,
                payment_done=(payment_method == 'cod'),
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    food_item=item.food_item,
                    quantity=item.quantity,
                    price=item.food_item.price,
                )

            cart_items.delete()

            if payment_method == 'online':
                return redirect('payment', order_id=order.id)
            else:
                messages.success(request, f'Order #{order.id} placed successfully!')
                return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'cart': cart,
        'cart_items': cart_items,
    })


@login_required
def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.payment_done = True
        order.status = 'confirmed'
        order.save()
        messages.success(request, f'Payment successful! Order #{order.id} confirmed.')
        return redirect('order_success', order_id=order.id)
    return render(request, 'payment.html', {'order': order})


@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('order_items__food_item')
    return render(request, 'my_orders.html', {'orders': orders})