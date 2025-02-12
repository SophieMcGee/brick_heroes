from django.urls import path, include
from django.contrib import admin
from . import views
from .views import contact_view, contact_success
from notifications.views import admin_notifications
from subscriptions.views import user_profile


urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', user_profile, name='user_profile'),
    path(
        'subscription-plans/',
        views.subscription_plans,
        name='subscriptigion_plans',
    ),
    path('subscriptions/', include('subscriptions.urls')),
    path('cart/', include('cart.urls')),
    path('contact/', contact_view, name='contact'),
    path('contact/success/', contact_success, name='contact_success'),
    path(
        "admin/notifications/",
        admin_notifications,
        name="admin_notifications",
    ),
    path(
        "manage-store/",
        views.manage_store,
        name="manage_store",
    ),
    path(
        "privacy-policy/",
        views.privacy_policy,
        name="privacy_policy",
    ),
    path(
        "manage-store/edit/<int:product_id>/",
        views.edit_product,
        name="edit_product",
    ),
    path(
        "manage-store/delete/<int:product_id>/",
        views.delete_product,
        name="delete_product",
    ),
]
