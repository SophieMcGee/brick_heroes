from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.profile, name='account_profile'),
    path('collections/', views.collections, name='collections'),
]