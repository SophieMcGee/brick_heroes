from django.urls import path
from . import views
from .views import view_cart, checkout, process_checkout

urlpatterns = [
    path('', view_cart, name='shopping_cart'),
    path(
        "add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),
    path(
        "remove/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),
    path('checkout/', checkout, name='checkout'),
    path(
        'process-checkout/',
        process_checkout,
        name='process_checkout'
    ),
]
