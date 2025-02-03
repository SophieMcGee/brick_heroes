from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.user_profile, name='user_profile'),
    path('my-borrowings/', views.my_borrowings, name='my_borrowings'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('my-notifications/', views.my_notifications, name='my_notifications'),
    path('manage-legosets/', views.manage_legosets, name='manage_legosets'),
    path(
        'edit-legoset/<int:legoset_id>/',
        views.edit_legoset,
        name='edit_legoset',
    ),
    path(
        'delete-legoset/<int:legoset_id>/',
        views.delete_legoset,
        name='delete_legoset',
    ),
    path('admin-tools/', views.admin_tools, name='admin_tools'),
    path('borrow-cart/', views.borrow_cart, name='borrow_cart'),
    path('filter-by-price/', views.filter_by_price, name='filter_by_price'),
    path('filter-by-rating/', views.filter_by_rating, name='filter_by_rating'),
    path('filter-by-theme/', views.filter_by_theme, name='filter_by_theme'),
    path(
        'subscription-plans/',
        views.subscription_plans,
        name='subscription_plans',
    ),
    path('gift-cards/', views.gift_cards, name='gift_cards'),
    path('subscriptions/', include('subscriptions.urls')),
    path('cart/', include('cart.urls')),
]
