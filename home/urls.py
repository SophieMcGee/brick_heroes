from django.urls import path, include
from django.contrib import admin
from . import views
from .views import contact_view, contact_success
from notifications.views import admin_notifications
from subscriptions.views import user_profile

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', user_profile, name='user_profile'),
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
    path('filter-by-rating/', views.filter_by_rating, name='filter_by_rating'),
    path('filter-by-theme/', views.filter_by_theme, name='filter_by_theme'),
    path(
        'subscription-plans/',
        views.subscription_plans,
        name='subscription_plans',
    ),
    path('subscriptions/', include('subscriptions.urls')),
    path('cart/', include('cart.urls')),
    path('contact/', contact_view, name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
    path("admin/notifications/", admin_notifications, name="admin_notifications"),
    path('admin/', admin.site.urls),
]
