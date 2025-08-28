# 🚀 Ejercicio 2: Blog Completo con Autenticación

**Tiempo estimado:** 25-30 minutos  
**Nivel:** Intermedio  
**Objetivos:** Agregar autenticación, formularios y templates al blog

---

## 📋 Prerrequisitos

- Haber completado el Ejercicio 1
- Tener el proyecto `mi_blog` funcionando
- Servidor Django ejecutándose

---

## 🎯 Instrucciones

### Parte 1: Sistema de Autenticación (10 minutos)

#### 1.1 Crear vistas de autenticación

Agrega a `blog/views.py`:

```python
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect

def vista_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('lista_posts')
        else:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'registration/login.html')

def vista_registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cuenta creada exitosamente')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/registro.html', {'form': form})

def vista_logout(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión')
    return redirect('lista_posts')

@login_required
def mi_perfil(request):
    return render(request, 'blog/perfil.html')
```

#### 1.2 Actualizar URLs

Actualiza `blog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
    path('login/', views.vista_login, name='login'),
    path('registro/', views.vista_registro, name='registro'),
    path('logout/', views.vista_logout, name='logout'),
    path('perfil/', views.mi_perfil, name='perfil'),
]
```

### Parte 2: Templates Básicos (8 minutos)

#### 2.1 Crear estructura de carpetas

```bash
mkdir -p blog/templates/blog
mkdir -p blog/templates/registration
```

#### 2.2 Template base (`blog/templates/blog/base.html`)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Blog Django{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'lista_posts' %}">📝 Mi Blog</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <span class="navbar-text me-3">Hola, {{ user.username }}!</span>
                    <a class="nav-link" href="{% url 'perfil' %}">Perfil</a>
                    <a class="nav-link" href="{% url 'logout' %}">Salir</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Iniciar Sesión</a>
                    <a class="nav-link" href="{% url 'registro' %}">Registrarse</a>
                {% endif %}
            </div>
        </div>
    </nav>

    {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <main class="container mt-4">
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
```

#### 2.3 Lista de posts (`blog/templates/blog/lista_posts.html`)

```html
{% extends 'blog/base.html' %}

{% block title %}Posts - Mi Blog{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2>Últimos Posts</h2>
        {% for post in posts %}
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">{{ post.titulo }}</h5>
                    <p class="card-text">{{ post.contenido|truncatewords:30 }}</p>
                    <small class="text-muted">
                        Por {{ post.autor.username }} en {{ post.categoria.nombre }}
                        - {{ post.fecha_creacion|date:"d/m/Y" }}
                    </small>
                    <div class="mt-2">
                        <a href="{% url 'detalle_post' post.id %}" class="btn btn-primary btn-sm">Leer más</a>
                    </div>
                </div>
            </div>
        {% empty %}
            <p>No hay posts publicados aún.</p>
        {% endfor %}
    </div>
    
    <div class="col-md-4">
        <h4>Categorías</h4>
        <div class="list-group">
            {% for categoria in categorias %}
                <a href="#" class="list-group-item list-group-item-action">
                    {{ categoria.nombre }}
                </a>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
```

#### 2.4 Login template (`blog/templates/registration/login.html`)

```html
{% extends 'blog/base.html' %}

{% block title %}Iniciar Sesión{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h4>Iniciar Sesión</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="username" class="form-label">Usuario</label>
                        <input type="text" class="form-control" name="username" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Contraseña</label>
                        <input type="password" class="form-control" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Iniciar Sesión</button>
                </form>
                <div class="text-center mt-3">
                    <a href="{% url 'registro' %}">¿No tienes cuenta? Regístrate</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Parte 3: Formularios para Posts (7 minutos)

#### 3.1 Crear formulario en `blog/forms.py`

```python
from django import forms
from .models import Post, Categoria

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'categoria', 'publicado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'publicado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
```

#### 3.2 Vista para crear posts

Agrega a `blog/views.py`:

```python
from .forms import PostForm

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            messages.success(request, 'Post creado exitosamente!')
            return redirect('lista_posts')
    else:
        form = PostForm()
    
    return render(request, 'blog/crear_post.html', {'form': form})
```

#### 3.3 Template para crear posts (`blog/templates/blog/crear_post.html`)

```html
{% extends 'blog/base.html' %}

{% block title %}Crear Post{% endblock %}

{% block content %}
<h2>Crear Nuevo Post</h2>
<form method="post">
    {% csrf_token %}
    <div class="mb-3">
        <label class="form-label">Título</label>
        {{ form.titulo }}
    </div>
    <div class="mb-3">
        <label class="form-label">Contenido</label>
        {{ form.contenido }}
    </div>
    <div class="mb-3">
        <label class="form-label">Categoría</label>
        {{ form.categoria }}
    </div>
    <div class="mb-3 form-check">
        {{ form.publicado }}
        <label class="form-check-label">Publicar inmediatamente</label>
    </div>
    <button type="submit" class="btn btn-success">Crear Post</button>
    <a href="{% url 'lista_posts' %}" class="btn btn-secondary">Cancelar</a>
</form>
{% endblock %}
```

#### 3.4 Actualizar URLs

Agrega a `blog/urls.py`:

```python
path('crear/', views.crear_post, name='crear_post'),
```

---

## ✅ Criterios de Evaluación

**Al final debes poder:**

1. ✅ Registrar nuevos usuarios
2. ✅ Iniciar y cerrar sesión
3. ✅ Ver lista de posts con diseño Bootstrap
4. ✅ Crear nuevos posts (solo usuarios autenticados)
5. ✅ Ver mensajes de éxito/error
6. ✅ Navegar entre páginas con navbar

---

## 🎉 Bonus Challenges

Si terminas antes de tiempo:

1. **Agregar vista de detalle de post** con template
2. **Filtrar posts por categoría** 
3. **Agregar contador de posts** en la navbar
4. **Permitir editar solo tus propios posts**
5. **Agregar fecha de última actualización**

---

## 🆘 Solución de Problemas

**Templates no se encuentran:**
```python
# En settings.py, asegúrate de tener:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Puede estar vacío
        'APP_DIRS': True,  # ¡Debe estar en True!
        # ...
    },
]
```

**Bootstrap no carga:**
- Verifica tu conexión a internet
- Los CDN deben estar disponibles

**Formularios no se envían:**
- Asegúrate de incluir `{% csrf_token %}`
- Verifica el atributo `method="post"`

---

## 📚 Lo que Aprendiste

- ✅ Sistema completo de autenticación Django
- ✅ Templates con herencia y Bootstrap
- ✅ Formularios ModelForm
- ✅ Decoradores (@login_required)
- ✅ Mensajes de feedback al usuario
- ✅ Protección CSRF
- ✅ URLs con nombres y redirecciones

**¡Felicitaciones! 🎉 Tienes un blog funcional con Django**


