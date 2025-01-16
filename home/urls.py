from django.urls import path
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
]