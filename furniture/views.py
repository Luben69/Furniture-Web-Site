from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def home(request):
    return render(request, 'furniture/index.html')


class MyLoginView(LoginView):
    template_name = 'furniture/login.html'  # your login template
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        # Save old guest session key before login (session rotates after login)
        self.request.session['_old_session_key'] = self.request.session.session_key
        return super().form_valid(form)
    

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # creates new User in auth_user

            request.session['_old_session_key'] = request.session.session_key

            login(request, user)  # log them in directly
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "furniture/signup.html", {"form": form})


def test_auth(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Logged in as {request.user.username}")
    else:
        return HttpResponse(f"Guest user with session key: {request.session.session_key}")


def cart(request):
    cart = get_cart(request)              # get current cart (user or session)
    items = cart.items.all()              # fetch all CartItem objects for this cart

    # calculate subtotal and total
    cart_items = []
    total_price = 0
    for item in items:
        subtotal = item.product.price * item.quantity
        total_price += subtotal
        cart_items.append({
            "item": item,
            "subtotal": subtotal
        })

    return render(request, "furniture/cart.html", {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price
    })


def sofas(request):
    products = Product.objects.filter(category__name="sofa")
    return render(request, "furniture/sofas.html", {
        "products": products,
    })


def chairs(request):
    products = Product.objects.filter(category__name="chair")
    return render(request, "furniture/chairs.html", {"products": products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "furniture/product_detail.html", {"product": product})


# Helper: get or create the cart
def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()  # explicitly create session
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


# Add a product to cart
@require_POST
def add_to_cart(request, product_id):
    print("ADD TO CART session key:", request.session.session_key)
    cart = get_cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    return redirect('product_detail', product_id=product.id)

# Remove a product from cart
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('view_cart')

# View cart page
def view_cart(request):
    cart = get_cart(request)
    items = cart.items.all()

    cart_items = []
    total_price = 0
    for item in items:
        subtotal = item.product.price * item.quantity
        total_price += subtotal
        cart_items.append({
            "item": item,
            "subtotal": subtotal
        })

    return render(request, 'furniture/cart.html', {
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price
    })