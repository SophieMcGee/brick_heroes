from django.urls import path
from . import views
from cart import views as cart_views
from .views import submit_review, delete_review

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<str:category_name>/', views.all_products, name='products_by_category'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('add/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path("admin/notifications/", views.admin_notifications, name="admin_notifications"),
    path("approve_review/<int:review_id>/", views.approve_review, name="approve_review"),
]