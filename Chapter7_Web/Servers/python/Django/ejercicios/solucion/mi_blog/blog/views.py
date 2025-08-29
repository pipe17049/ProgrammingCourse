from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.shortcuts import render
from .models import PostEntry

def lista_postsentries(request):
    """Vista que muestra todos los posts publicados"""
    posts = PostEntry.objects.filter(publicado=True).order_by('-fecha_creacion')
    
    contexto = {
        'posts': posts,
        'autores': User.objects.get(),
        'titulo_pagina': 'Mi Blog Django'
    }
    
    return render(request, 'lista_posts.html', contexto)

def detalle_postentry(request, postentry_id):
    """Vista que muestra un post específico"""
    post = PostEntry.objects.get(id=postentry_id, publicado=True)
    
    contexto = {
        'post': post
    }
    
    return render(request, 'detalle_postentry.html', contexto)