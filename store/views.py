from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, Order


# ---------- Home Page ----------
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# ---------- Add to Cart ----------
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('view_cart')


# ---------- View Cart ----------
def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    context = {
        'products': products,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Order

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Your cart is empty.")
        return redirect('view_cart')

    user = request.user

    # Create orders directly from the cart
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        Order.objects.create(
            user=user,
            product=product,
            quantity=quantity,
            status='Order Placed'
        )

    # Clear the cart and redirect to Orders page
    request.session['cart'] = {}
    messages.success(request, "Your order has been placed successfully!")
    return redirect('view_orders')


# ---------- Remove from Cart ----------
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('view_cart')

# ---------- View Orders ----------
@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user).exclude(status='Cancelled')
    context = {'orders': orders}
    return render(request, 'orders.html', context)


# ---------- Cancel Order ----------
@login_required
def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.status != "Cancelled":
        order.status = "Cancelled"
        order.save()
    return render(request, "cancel_success.html", {"order": order})


# ---------- Register User ----------
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


# ---------- Login User ----------
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    return render(request, 'login.html')


# ---------- Logout User ----------
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# ---------- API: List Products ----------
def api_products(request):
    products = list(Product.objects.values('id', 'name', 'description', 'price', 'image'))
    return JsonResponse({'products': products}, safe=False)


# ---------- API: Single Product ----------
def api_product_detail(request, id):
    try:
        product = Product.objects.values('id', 'name', 'description', 'price', 'image').get(id=id)
        return JsonResponse({'product': product})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


# ---------- API: Checkout ----------
@csrf_exempt
@login_required
def api_checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            # Create order directly from cart data
            for item in data.get('cart', []):
                product = Product.objects.get(id=item['product_id'])
                Order.objects.create(
                    user=request.user,
                    product=product,
                    quantity=item['quantity'],
                    status='Order Placed'
                )

            return JsonResponse({'message': 'Order placed successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
# ---------- API: Orders ----------
@login_required
def api_orders(request):
    orders = list(
        Order.objects.filter(user=request.user)
        .values('id', 'product__name', 'quantity', 'status', 'created_at')
    )
    return JsonResponse({'orders': orders})


# ---------- API: Cancel Order ----------
@csrf_exempt
@login_required
def api_cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order.status = 'Cancelled'
        order.save()
        return JsonResponse({'message': f'Order {order_id} cancelled successfully'})
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)