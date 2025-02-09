from django.urls import path
from . import views
from cart import views as cart_views
from .views import submit_review, product_detail, submit_rating

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<str:category_name>/', views.all_products, name='products_by_category'),
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),
    path('add/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
    path('<int:product_id>/submit-rating/', submit_rating, name='submit_rating'),
]