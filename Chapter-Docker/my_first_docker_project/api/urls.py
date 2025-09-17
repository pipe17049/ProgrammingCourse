from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.list_products, name='list_products'),  # Para ver todos
    path('product/<str:id>/', views.get_product, name='get_product'),
    path('product/', views.create_product, name='create_product'),
    
    # 🕷️ Web Scraping endpoints
    path('search/mercadolibre/', views.search_mercadolibre, name='search_mercadolibre'),
    path('compare/prices/', views.compare_product_prices, name='compare_prices'),
    path('scrape/details/', views.get_product_details_ml, name='scrape_details'),
]