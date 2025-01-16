from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('profile/', views.profile, name='user_profile'),
    path('collections/', views.collections, name='collections'),
    path('my-borrowings/', views.my_borrowings, name='my_borrowings'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('my-notifications/', views.my_notifications, name='my_notifications'),
]