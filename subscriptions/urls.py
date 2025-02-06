from django.urls import path
from . import views

urlpatterns = [
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('success/', views.subscription_success, name='subscription_success'),
    path('cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]