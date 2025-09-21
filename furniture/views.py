from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'furniture/index.html')


def cart_count(request):
    cart = get_cart(request)
    count = sum(item.quantity for item in cart.items.all())
    return JsonResponse({"cart_count": count})


class MyLoginView(LoginView):
    print('HELLO U ARE AT LOGGIN IN')
    template_name = 'furniture/login.html'  # login template
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        # breakpoint()
        # Save old guest session key before login (session rotates after login)
        print(self.request.session.session_key)
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


# @require_POST
# def update_cart_item(request, item_id):
#     action = request.POST.get("action")  # "increase" or "decrease"
#     cart_item = get_object_or_404(CartItem, id=item_id)
#     product = cart_item.product

#     if action == "increase":
#         if product.stock > 0:
#             cart_item.quantity += 1
#             product.stock -= 1
#             cart_item.save()
#             product.save()
#         else:
#             messages.error(request, f"Sorry, {product.name} is out of stock.")

#     elif action == "decrease":
#         if cart_item.quantity > 0:
#             cart_item.quantity -= 1
#             product.stock += 1

#             if cart_item.quantity == 0:
#                 cart_item.delete()  # remove item completely
#             else:
#                 cart_item.save()

#             product.save()

#     return redirect("view_cart")  # replace with your cart page’s URL name


@require_POST
def update_cart_item(request, item_id):
    action = request.POST.get("action")
    cart_item = get_object_or_404(CartItem, id=item_id)
    product = cart_item.product

    if action == "increase":
        if product.stock > 0:
            cart_item.quantity += 1
            product.stock -= 1
            cart_item.save()
        else:
            return JsonResponse({"success": False, "message": f"{product.name} is out of stock."})

    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            product.stock += 1
            cart_item.save()
        elif cart_item.quantity == 1:
            # Removing item completely
            product.stock += 1
            cart_item.delete()
            cart_item = None  # mark as deleted
        else:
            return JsonResponse({"success": False, "message": "Cannot decrease further."})

    product.save()

    cart = get_cart(request)
    cart_item_count = sum(item.quantity for item in cart.items.all())
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

    new_subtotal = 0
    if cart_item:
        new_subtotal = cart_item.product.price * cart_item.quantity

    return JsonResponse({
        "success": True,
        "new_quantity": cart_item.quantity if cart_item else 0,
        "new_subtotal": f"{new_subtotal:.2f}",
        "total_price": f"{total_price:.2f}",
        "cart_item_count": cart_item_count
    })


def refresh_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse ({
        "stock": product.stock,
        "price": str(product.price),
    })


# def cart(request):
#     cart = get_cart(request)              # get current cart (user or session)
#     items = cart.items.all()              # fetch all CartItem objects for this cart

#     # calculate subtotal and total
#     cart_items = []
#     total_price = 0
#     for item in items:
#         subtotal = item.product.price * item.quantity
#         total_price += subtotal
#         cart_items.append({
#             "item": item,
#             "subtotal": subtotal
#         })

#     return render(request, "furniture/cart.html", {
#         "cart": cart,
#         "cart_items": cart_items,
#         "total_price": total_price
#     })


def chairs(request):
    products = Product.objects.filter(category__name="chair")
    return render(request, "furniture/chairs.html", {"products": products})


def sofas(request):
    products = Product.objects.filter(category__name="sofa")
    return render(request, "furniture/sofas.html", {"products": products,})


def tables(request):
    products = Product.objects.filter(category__name="table")
    return render(request, "furniture/chairs.html", {"products": products})


def beds(request):
    products = Product.objects.filter(category__name="bed")
    return render(request, "furniture/chairs.html", {"products": products})


def lamps(request):
    products = Product.objects.filter(category__name="lamp")
    return render(request, "furniture/chairs.html", {"products": products})


def desks(request):
    products = Product.objects.filter(category__name="desk")
    return render(request, "furniture/chairs.html", {"products": products})


def paintings(request):
    products = Product.objects.filter(category__name="painting")
    return render(request, "furniture/chairs.html", {"products": products})


def doors(request):
    products = Product.objects.filter(category__name="door")
    return render(request, "furniture/chairs.html", {"products": products})


def curtains(request):
    products = Product.objects.filter(category__name="curtain")
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

    if quantity > product.stock:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": f"Only {product.stock} items left."})
        messages.error(request, f"Only {product.stock} items are in stock.")
        return redirect('product_detail', product_id=product.id)

    
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity

    product.stock -= quantity 

    product.save()
    item.save()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "stock": product.stock,
            "cart_quantity": item.quantity,
            "product_id": product.id,
            "price": str(product.price),  # safer than float for money
        })
    

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