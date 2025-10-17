# 🎯 Ejercicio 1: Django Básico - Estructura y Contenido Estático

**Tiempo estimado:** 30 minutos  
**Nivel:** Principiante  
**Objetivo:** Entender la **estructura de Django** y crear **páginas estáticas**

---

## 🚀 Lo que Vamos a Construir

Un proyecto Django con **páginas estáticas** que demuestre la estructura básica:
- 📄 **Páginas HTML fijas** (sin base de datos)
- 🏗️ **Estructura de apps** y organización
- 🔗 **Sistema de URLs** 
- 📊 **Migraciones** básicas

**Concepto clave:** Antes de trabajar con bases de datos, entendamos la estructura de Django.

---

## 📋 Parte 1: Crear el Proyecto Base (10 minutos)

### 1.1 Crear el proyecto Django
```bash
django-admin startproject mi_blog
cd mi_blog
```

### 1.2 Crear la app para páginas estáticas
```bash
python manage.py startapp staticpages
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
    'staticpages',  # ← Nueva app
]
```

---

## 📋 Parte 2: Crear Páginas Estáticas (15 minutos)

### 2.1 Crear `staticpages/views.py`
```python
# staticpages/views.py
from django.http import HttpResponse

def home(request):
    """Vista que devuelve HTML fijo - sin base de datos"""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>📄 Mi Primera Página Django</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f8ff; }
            .container { max-width: 800px; margin: 0 auto; background: white; 
                        padding: 30px; border-radius: 10px; }
            nav a { margin-right: 15px; text-decoration: none; color: #007cba; }
        </style>
    </head>
    <body>
        <div class="container">
            <nav>
                <a href="/static-pages/">🏠 Home</a>
                <a href="/static-pages/about/">ℹ️ About</a>
                <a href="/static-pages/contact/">📧 Contact</a>
            </nav>
            
            <h1>📄 ¡Bienvenido a Django!</h1>
            <p><strong>¿Qué es contenido estático?</strong></p>
            <ul>
                <li>✅ HTML completamente fijo</li>
                <li>✅ No consulta base de datos</li>
                <li>✅ Respuesta muy rápida</li>
                <li>✅ Ideal para landing pages</li>
            </ul>
            
            <p><em>Esta página está definida directamente en el código Python.</em></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def about(request):
    """Página About estática"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📋 Acerca de</title>
        <style>body { font-family: Arial; margin: 40px; }</style>
    </head>
    <body>
        <h1>📋 Acerca de Mi Sitio</h1>
        <p>Esta es una página estática creada con Django.</p>
        <p><strong>Características:</strong></p>
        <ul>
            <li>No usa base de datos</li>
            <li>HTML fijo definido en views.py</li>
            <li>Respuesta inmediata</li>
        </ul>
        <a href="/static-pages/">← Volver al Home</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def contact(request):
    """Formulario de contacto estático"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📧 Contacto</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            .form-group { margin: 15px 0; }
            input, textarea { width: 300px; padding: 8px; }
            button { background: #007cba; color: white; padding: 10px 20px; border: none; }
        </style>
    </head>
    <body>
        <h1>📧 Contacto</h1>
        <p><strong>⚠️ Formulario estático</strong> - No procesa datos realmente.</p>
        
        <form>
            <div class="form-group">
                <label>Nombre:</label><br>
                <input type="text" placeholder="Tu nombre">
            </div>
            <div class="form-group">
                <label>Email:</label><br>
                <input type="email" placeholder="tu@email.com">
            </div>
            <div class="form-group">
                <label>Mensaje:</label><br>
                <textarea rows="4" placeholder="Tu mensaje..."></textarea>
            </div>
            <button type="button" onclick="alert('¡Formulario estático!')">
                📤 Enviar
            </button>
        </form>
        
        <p><a href="/static-pages/">← Volver al Home</a></p>
    </body>
    </html>
    """
    return HttpResponse(html_content)
```

### 2.2 Crear `staticpages/urls.py`
```python
# staticpages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='static_home'),
    path('about/', views.about, name='static_about'),
    path('contact/', views.contact, name='static_contact'),
]
```

### 2.3 Configurar URLs principales
```python
# mi_blog/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('static-pages/', include('staticpages.urls')),
]
```

---

## 📋 Parte 3: Entender Migraciones (5 minutos)

### 3.1 ¿Qué son las migraciones?
Las **migraciones** son archivos que Django usa para actualizar la base de datos:

```bash
# Ver estado de migraciones
python manage.py showmigrations

# Crear migraciones (cuando cambies modelos)
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate
```

### 3.2 Aplicar migraciones iniciales
```bash
# Aplicar migraciones por defecto de Django
python manage.py migrate
```

**Resultado:** Se crea `db.sqlite3` con tablas de autenticación, sesiones, etc.

### 3.3 Revisar migraciones aplicadas
```bash
python manage.py showmigrations
```

**Salida esperada:**
```
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 # ... más migraciones
staticpages
 (no migrations)
```

---

## 🚀 Probar el Proyecto

### Ejecutar servidor
```bash
# Solo en tu computadora (localhost)
python manage.py runserver

# Para acceso desde móviles/otros dispositivos
python manage.py runserver 0.0.0.0:8000
```

### 📱 Configurar para dispositivos móviles

Si quieres probar desde tu **móvil** o **otros dispositivos**:

1. **Actualizar `settings.py`:**
```python
# mi_blog/settings.py
ALLOWED_HOSTS = ['*']  # Permite acceso desde cualquier IP
```

2. **Obtener tu IP local:**
```bash
# En Windows
ipconfig

# En Mac/Linux  
ifconfig | grep inet
```

3. **Acceder desde el móvil:**
```
http://TU_IP_LOCAL:8000/static-pages/
# Ejemplo: http://192.168.1.100:8000/static-pages/
```

### Navegar a las páginas
- **Home:** `http://127.0.0.1:8000/static-pages/`
- **About:** `http://127.0.0.1:8000/static-pages/about/`
- **Contact:** `http://127.0.0.1:8000/static-pages/contact/`

**💡 Tip:** Con `0.0.0.0:8000` puedes mostrar tu trabajo a compañeros en la misma red WiFi!

---

## 📊 Estructura Final del Proyecto

```
mi_blog/
├── manage.py
├── db.sqlite3                     # Base de datos (creada tras migrate)
├── mi_blog/
│   ├── __init__.py
│   ├── settings.py               # ✅ staticpages registrada
│   ├── urls.py                   # ✅ URLs configuradas
│   ├── wsgi.py
│   └── asgi.py
└── staticpages/
    ├── __init__.py
    ├── views.py                  # ✅ 3 vistas estáticas
    ├── urls.py                   # ✅ 3 rutas configuradas
    ├── apps.py
    ├── admin.py                  # (sin usar)
    ├── models.py                 # (sin usar)
    ├── tests.py
    └── migrations/
        └── __init__.py           # Sin migraciones (no hay modelos)
```

---

## 🎯 Conceptos Aprendidos

### ✅ Estructura de Django
- **Proyecto** vs **App**: `mi_blog` es el proyecto, `staticpages` es una app
- **URLs**: Enrutamiento de `/static-pages/` hacia `staticpages.urls`
- **Vistas**: Funciones que procesan requests y devuelven responses

### ✅ Páginas Estáticas
- **HTML fijo** definido en Python (views.py)
- **Sin base de datos** - contenido que no cambia
- **Respuesta rápida** - no hay consultas SQL

### ✅ Migraciones
- **showmigrations**: Ver estado de migraciones
- **migrate**: Aplicar migraciones a la base de datos
- **makemigrations**: Crear migraciones (cuando tengas modelos)

---

## ➡️ Próximo Paso

En el **Ejercicio 2** agregaremos:
- 🗄️ **Modelos** con base de datos
- 🎨 **Templates dinámicos** 
- 🔌 **API REST** para JSON

**¡Has completado tu primera app Django con páginas estáticas!** 🎉