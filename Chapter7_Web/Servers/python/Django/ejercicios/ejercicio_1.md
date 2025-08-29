# 🎯 Ejercicio 1: Django Core - Mi Primer Blog

**Tiempo estimado:** 25 minutos  
**Nivel:** Principiante  
**Objetivo:** Entender el flujo básico Django: **URL → Vista → Template**

---

## 🚀 Lo que Vamos a Construir

Un **blog simple** que muestre posts desde la base de datos.

**Flujo que aprenderemos:**
```
Usuario visita /posts → Django busca URL → Ejecuta vista → Renderiza template → Muestra HTML
```

---

## 📋 Parte 1: Proyecto y App (10 minutos)

### 1.1 Crear el proyecto
```bash
django-admin startproject mi_blog
cd mi_blog
```

### 1.2 Crear la aplicación  
```bash
python manage.py startapp blog
```

### 1.3 Registrar la app en `settings.py`
```python
# mi_blog/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', 
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # ← Agregar esta línea
]
```

**🎯 Checkpoint:** `python manage.py runserver` debe funcionar sin errores.

---

## 📋 Parte 2: Modelos (15 minutos)

### 2.1 Definir modelos en `blog/models.py`
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
```

### 2.2 Crear migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2.3 Crear datos de prueba en `blog/management/commands/crear_posts.py`
```bash
# Crear directorios
mkdir -p blog/management/commands
touch blog/management/__init__.py
touch blog/management/commands/__init__.py
```

```python
# blog/management/commands/crear_posts.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crear usuario si no existe
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user('demo', 'demo@example.com', 'demo123')
        
        autor = User.objects.get(username='demo')
        
        # Crear posts de ejemplo
        posts_ejemplo = [
            {
                'titulo': 'Mi primer post en Django',
                'contenido': 'Este es mi primer post usando Django. ¡Es increíble lo fácil que es!'
            },
            {
                'titulo': 'Aprendiendo Python web',
                'contenido': 'Django hace que el desarrollo web sea muy productivo y divertido.'
            },
            {
                'titulo': 'Modelos y base de datos',
                'contenido': 'Los modelos de Django hacen muy fácil trabajar con bases de datos.'
            }
        ]
        
        for post_data in posts_ejemplo:
            Post.objects.get_or_create(
                titulo=post_data['titulo'],
                defaults={
                    'contenido': post_data['contenido'],
                    'autor': autor
                }
            )
        
        self.stdout.write('✅ Posts de ejemplo creados!')
```

```bash
# Ejecutar comando para crear datos
python manage.py crear_posts
```

**🎯 Checkpoint:** Tienes modelos y datos en la base de datos.

---

## 📋 Parte 3: Vistas (10 minutos)

### 3.1 Crear vista en `blog/views.py`
```python
from django.shortcuts import render
from .models import Post

def lista_posts(request):
    """Vista que muestra todos los posts publicados"""
    posts = Post.objects.filter(publicado=True).order_by('-fecha_creacion')
    
    contexto = {
        'posts': posts,
        'titulo_pagina': 'Mi Blog Django'
    }
    
    return render(request, 'blog/lista_posts.html', contexto)

def detalle_post(request, post_id):
    """Vista que muestra un post específico"""
    post = Post.objects.get(id=post_id, publicado=True)
    
    contexto = {
        'post': post
    }
    
    return render(request, 'blog/detalle_post.html', contexto)
```

**🎯 Concepto clave:** La vista toma datos de los modelos y los pasa al template.

---

## 📋 Parte 4: URLs (10 minutos)

### 4.1 Crear `blog/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
]
```

### 4.2 Conectar en `mi_blog/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # ← Agregar esta línea
]
```

**🎯 Concepto clave:** Django busca el patrón de URL y ejecuta la vista correspondiente.

---

## 📋 Parte 5: Templates (15 minutos)

### 5.1 Crear estructura de templates
```bash
mkdir -p blog/templates/blog
```

### 5.2 Template base `blog/templates/blog/base.html`
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Blog Django{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .post { border: 1px solid #ddd; padding: 20px; margin: 20px 0; }
        .post h2 { color: #333; }
        .meta { color: #666; font-size: 0.9em; }
        a { color: #007cba; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <header>
        <h1><a href="{% url 'lista_posts' %}">🐍 Mi Blog Django</a></h1>
    </header>
    
    <main>
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
```

### 5.3 Lista de posts `blog/templates/blog/lista_posts.html`
```html
{% extends 'blog/base.html' %}

{% block title %}{{ titulo_pagina }}{% endblock %}

{% block content %}
<h2>Posts Recientes</h2>

{% for post in posts %}
    <div class="post">
        <h3><a href="{% url 'detalle_post' post.id %}">{{ post.titulo }}</a></h3>
        <p>{{ post.contenido|truncatewords:30 }}</p>
        <div class="meta">
            Por {{ post.autor.username }} el {{ post.fecha_creacion|date:"d/m/Y" }}
        </div>
    </div>
{% empty %}
    <p>No hay posts publicados aún.</p>
{% endfor %}
{% endblock %}
```

### 5.4 Detalle de post `blog/templates/blog/detalle_post.html`
```html
{% extends 'blog/base.html' %}

{% block title %}{{ post.titulo }}{% endblock %}

{% block content %}
<article>
    <h2>{{ post.titulo }}</h2>
    <div class="meta">
        Por {{ post.autor.username }} el {{ post.fecha_creacion|date:"d/m/Y H:i" }}
    </div>
    <div style="margin-top: 20px;">
        {{ post.contenido|linebreaks }}
    </div>
</article>

<a href="{% url 'lista_posts' %}">← Volver a la lista</a>
{% endblock %}
```

---

## ✅ Verificación Final

### Prueba tu blog:
```bash
python manage.py runserver
```

**URLs para probar:**
- `http://127.0.0.1:8000/` → Lista de posts
- `http://127.0.0.1:8000/post/1/` → Detalle del primer post

### Debe mostrar:
- ✅ Lista de 3 posts de ejemplo
- ✅ Enlaces que funcionan
- ✅ Navegación entre lista y detalle
- ✅ Información del autor y fecha

---

## 🎓 Lo que Aprendiste

### Flujo Completo Django:
1. **URL** (`blog/urls.py`) → Patrón que coincide con la petición
2. **Vista** (`blog/views.py`) → Función que procesa la lógica  
3. **Modelo** (`blog/models.py`) → Datos de la base de datos
4. **Template** (`blog/templates/`) → HTML dinámico renderizado

### Conceptos Clave:
- ✅ **Modelos:** Definen estructura de datos
- ✅ **Migraciones:** Actualizan base de datos  
- ✅ **Vistas:** Lógica de negocio
- ✅ **URLs:** Enrutamiento de peticiones
- ✅ **Templates:** Presentación HTML
- ✅ **Contexto:** Datos pasados del view al template

**¡Ya tienes un blog funcional! 🎉 Siguiente: Ejercicio 2 - Formularios y Autenticación**
