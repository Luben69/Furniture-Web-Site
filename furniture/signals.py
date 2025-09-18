# furniture/signals.py
print("furniture.signals module loaded")
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem

@receiver(user_logged_in)
def merge_guest_cart(sender, request, user, **kwargs):
    breakpoint()
    print('HELLO U ARE AT SIGNALS IN')
    print(request.session.session_key)
    old_session_key = request.session.get('_old_session_key')
    """
    Merge items from a guest cart into the logged-in user's cart.
    """
    print("signals.py top-level code loaded")
    print(old_session_key)

    # Get the guest cart if it exists
    guest_cart = Cart.objects.filter(session_key=old_session_key, user__isnull=True).first()

    if not guest_cart:
        print('NOOOOOOOO')
        return
    items = guest_cart.items.all()
    for item in items:
        print(item.product.name)
        print(item.quantity)

    print('session key from db', guest_cart.session_key)

    # Get or create a cart for the logged-in user
    user_cart, _ = Cart.objects.get_or_create(user=user)
    other_items = user_cart.items.all()

    for item in other_items:
        print(item.product.name)
        print(item.quantity)

    print('User_cart: ', user_cart.session_key)
    print('User_cart: ', user_cart.user)

    # Merge items
    for item in guest_cart.items.all():
        cart_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            defaults={'quantity': item.quantity}
        )
        if not created:
            cart_item.quantity += item.quantity
            cart_item.save()

    # Delete the old guest cart
    guest_cart.delete()
