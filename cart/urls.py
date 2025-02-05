from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='shopping_cart'),
    path(
        'add/<str:item_type>/<int:item_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),
    path(
        'remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
    path('checkout/', views.checkout, name='checkout'),
    path(
        'checkout/subscription/<int:subscription_id>/',
        views.subscription_checkout,
        name='subscription_checkout'
    ),
]
