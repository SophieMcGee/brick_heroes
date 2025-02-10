from django.urls import path
from . import views
from .views import return_borrowed_sets, cancel_subscription

urlpatterns = [
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('subscribe/confirm/<int:plan_id>/', views.subscription_confirmation, name='subscription_confirmation'),
    path('checkout/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('success/', views.subscription_success, name='subscription_success'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path("return-borrowed-sets/", return_borrowed_sets, name="return_borrowed_sets"),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),
]
