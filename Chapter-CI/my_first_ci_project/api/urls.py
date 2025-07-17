from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.list_products, name='list_products'),  # Para ver todos
    path('product/<str:id>/', views.get_product, name='get_product'),
    path('product/', views.create_product, name='create_product'),
]