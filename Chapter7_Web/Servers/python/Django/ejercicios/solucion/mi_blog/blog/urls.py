from django.urls import path
from . import views

urlpatterns = [
    path('postentries/', views.lista_postsentries, name='lista_postsentries'),
    path('<int:postentry_id>/', views.detalle_postentry, name='detalle_postentry'),
]