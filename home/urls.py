from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.profile, name='user_profile'),
    path('collections/', views.collections, name='collections'),
    path('my-borrowings/', views.my_borrowings, name='my_borrowings'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('my-notifications/', views.my_notifications, name='my_notifications'),
    path('manage-legosets/', views.manage_legosets, name='manage_legosets'),
    path('edit-legoset/<int:legoset_id>/', views.edit_legoset, name='edit_legoset'),
    path('delete-legoset/<int:legoset_id>/', views.delete_legoset, name='delete_legoset'),
    path('admin-tools/', views.admin_tools, name='admin_tools'),
    path('borrow-cart/', views.borrow_cart, name='borrow_cart'),
    path('all-products/', views.all_products, name='all_products'),
    path('filter-by-price/', views.filter_by_price, name='filter_by_price'),
    path('filter-by-rating/', views.filter_by_rating, name='filter_by_rating'),
    path('filter-by-theme/', views.filter_by_theme, name='filter_by_theme'),
]