# 🎯 Ejercicio 1: Mi Primer Proyecto Django

**Tiempo estimado:** 20-25 minutos  
**Nivel:** Principiante  
**Objetivos:** Crear un proyecto Django funcional con modelos, vistas y admin

---

## 📋 Instrucciones

### Parte 1: Configuración Inicial (5 minutos)

1. **Crear entorno virtual**
   ```bash
   python -m venv mi_blog_env
   source mi_blog_env/bin/activate  # Mac/Linux
   # mi_blog_env\Scripts\activate   # Windows
   ```

2. **Instalar Django**
   ```bash
   pip install django
   django-admin --version
   ```

3. **Crear proyecto**
   ```bash
   django-admin startproject mi_blog
   cd mi_blog
   ```

4. **Crear aplicación**
   ```bash
   python manage.py startapp blog
   ```

5. **Registrar la aplicación** en `settings.py`
   ```python
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

### Parte 2: Modelos (8 minutos)

Crea los siguientes modelos en `blog/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.nombre

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    publicado = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
```

### Parte 3: Migraciones (3 minutos)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Parte 4: Admin y Superusuario (4 minutos)

1. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

2. **Registrar modelos** en `blog/admin.py`:
   ```python
   from django.contrib import admin
   from .models import Categoria, Post

   @admin.register(Categoria)
   class CategoriaAdmin(admin.ModelAdmin):
       list_display = ['nombre', 'descripcion']
       search_fields = ['nombre']

   @admin.register(Post)
   class PostAdmin(admin.ModelAdmin):
       list_display = ['titulo', 'autor', 'categoria', 'publicado', 'fecha_creacion']
       list_filter = ['categoria', 'publicado', 'fecha_creacion']
       search_fields = ['titulo', 'contenido']
       list_editable = ['publicado']
   ```

### Parte 5: Vistas Básicas (5 minutos)

Crea en `blog/views.py`:

```python
from django.shortcuts import render
from .models import Post, Categoria

def lista_posts(request):
    posts = Post.objects.filter(publicado=True)
    categorias = Categoria.objects.all()
    
    contexto = {
        'posts': posts,
        'categorias': categorias
    }
    return render(request, 'blog/lista_posts.html', contexto)

def detalle_post(request, post_id):
    post = Post.objects.get(id=post_id, publicado=True)
    return render(request, 'blog/detalle_post.html', {'post': post})
```

Crea `blog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
]
```

Actualiza `mi_blog/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

---

## ✅ Criterios de Evaluación

**Debes poder hacer lo siguiente:**

1. ✅ Ejecutar `python manage.py runserver` sin errores
2. ✅ Acceder al admin en `http://127.0.0.1:8000/admin/`
3. ✅ Crear categorías y posts desde el admin
4. ✅ Ver que los modelos se muestran correctamente
5. ✅ Acceder a `http://127.0.0.1:8000/` (aunque dé error de template)

---

## 🎉 ¡Bonus!

Si terminas rápido, intenta:

- Crear algunos posts de prueba en el admin
- Cambiar el idioma a español en `settings.py`:
  ```python
  LANGUAGE_CODE = 'es-es'
  TIME_ZONE = 'America/Mexico_City'
  ```
- Explorar el admin y sus funcionalidades

---

## 🆘 Problemas Comunes

**Error: No module named 'blog'**
- Verifica que agregaste `'blog'` a `INSTALLED_APPS`

**Error en migraciones**
- Asegúrate de estar en la carpeta del proyecto
- Verifica que el entorno virtual esté activado

**No aparecen los modelos en admin**
- Revisa que registraste los modelos en `admin.py`
- Reinicia el servidor

---

## 📚 Lo que Aprendiste

- ✅ Crear proyecto y aplicación Django
- ✅ Definir modelos con relaciones
- ✅ Hacer migraciones
- ✅ Configurar el admin de Django
- ✅ Crear vistas y URLs básicas

**¡Siguiente paso:** Ejercicio 2 - Autenticación y formularios
