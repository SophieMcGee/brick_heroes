from django.urls import path
from . import views

urlpatterns = [
    path(
        'subscription-plans/',
        views.subscription_plans,
        name='subscription_plans',
    ),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),
]
