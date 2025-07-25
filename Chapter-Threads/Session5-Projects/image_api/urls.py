"""
🖼️ URLs para Image API

Endpoints para demostrar operaciones I/O-bound:
- Servir imágenes 4K
- Información de imágenes  
- Procesamiento lento simulado
- Estadísticas del servidor
"""

from django.urls import path
from . import views

urlpatterns = [
    # 🏠 Health check
    path('', views.health_check, name='health_check'),
    
    # 🖼️ Endpoints de imágenes
    path('image/4k/', views.serve_4k_image, name='serve_4k_image'),
    path('image/info/', views.get_image_info, name='get_image_info'),
    path('image/slow/', views.serve_slow_image, name='serve_slow_image'),
    
    # 📊 Estadísticas del servidor
    path('stats/', views.get_server_stats, name='get_server_stats'),
] 