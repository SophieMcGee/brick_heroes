from django.urls import path
from . import views
from cart import views as cart_views
from .views import add_review, delete_review

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<str:category_name>/', views.all_products, name='products_by_category'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('review/<int:product_id>/', add_review, name='add_review'),
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),
    path('add/<int:product_id>/', cart_views.add_to_cart, name='add_to_cart'),
]