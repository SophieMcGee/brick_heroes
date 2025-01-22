from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<str:category_name>/', views.all_products, name='products_by_category'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]