from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag, name='bag'),  # Maps 'bag/' to the 'bag' view
]