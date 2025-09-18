from .views import get_cart


def cart_context(request):
    print(request.session.session_key)
    cart = get_cart(request)
    cart_item_count = sum(item.quantity for item in cart.items.all())
    return {"cart_item_count": cart_item_count}


    # cart = get_cart(request)
    # print("Cart ID:", cart.id)
    # print("Items:", [(i.product.name, i.quantity) for i in cart.items.all()])
    # cart_item_count = sum(item.quantity for item in cart.items.all())
    # print("Cart item count:", cart_item_count)
    # return {"cart_item_count": cart_item_count}

    # cart = get_cart(request)
    # cart_item_count = sum(item.quantity for item in cart.items.all())
    # return {"cart_item_count": cart_item_count, "cart": cart}