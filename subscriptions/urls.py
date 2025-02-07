from django.urls import path
from . import views

urlpatterns = [
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('subscribe/confirm/<int:plan_id>/', views.subscription_confirmation, name='subscription_confirmation'),
    path('subscribe/checkout/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('checkout/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('success/', views.subscription_success, name='subscription_success'),
    path('cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]
