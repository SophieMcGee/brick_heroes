from django.urls import path
from . import views
from .views import add_review

urlpatterns = [
    path('', views.all_products, name='all_products'),
    path('category/<str:category_name>/', views.all_products, name='products_by_category'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('review/<int:product_id>/', add_review, name='add_review'),
]