from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MyLoginView

urlpatterns = [
    path("", views.home, name="home"),
    path("cart/", views.view_cart, name="view_cart"),  # cart page
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),  # add item
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),  # remove item
    path("sofas/", views.sofas, name="sofas"),
    path("chairs/", views.chairs, name="chairs"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("test-auth/", views.test_auth, name="test_auth"),
    path("signup/", views.signup, name="signup"),
    path("login/", MyLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]
