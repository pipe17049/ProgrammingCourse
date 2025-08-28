# 🔐 Django - Autenticación, Formularios y Plantillas
# Sesión 1.5 horas - Segunda parte (40 minutos)

"""
DJANGO BÁSICO II - AUTENTICACIÓN Y FORMULARIOS

Tiempo estimado: 40 minutos
- Sistema de Autenticación (15 min)
- Formularios Django (12 min)
- Plantillas (Templates) (13 min)
"""

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# ============================================================================
# 1. SISTEMA DE AUTENTICACIÓN (15 minutos)
# ============================================================================

# Vista de login personalizada
def vista_login(request):
    """Vista para iniciar sesión"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('dashboard')  # Redirigir a página principal
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'auth/login.html')

# Vista de logout
def vista_logout(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('home')

# Vista de registro
def vista_registro(request):
    """Vista para registrar nuevos usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/registro.html', {'form': form})

# Vista protegida (requiere login)
@login_required
def vista_dashboard(request):
    """Vista que requiere autenticación"""
    contexto = {
        'usuario': request.user,
        'es_staff': request.user.is_staff,
        'fecha_registro': request.user.date_joined
    }
    return render(request, 'dashboard.html', contexto)

# Vista de perfil de usuario
@login_required
def vista_perfil(request):
    """Vista del perfil del usuario"""
    if request.method == 'POST':
        # Actualizar información del usuario
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('perfil')
    
    return render(request, 'auth/perfil.html', {'user': request.user})

# ============================================================================
# 2. FORMULARIOS DJANGO (12 minutos)
# ============================================================================

# Formulario básico con campos manuales
class ContactoForm(forms.Form):
    """Formulario de contacto básico"""
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre completo'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@email.com'
        })
    )
    asunto = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Asunto del mensaje'
        })
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Escribe tu mensaje aquí...'
        })
    )
    
    # Validación personalizada
    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        if len(mensaje) < 10:
            raise forms.ValidationError('El mensaje debe tener al menos 10 caracteres')
        return mensaje

# Formulario basado en modelo (ModelForm)
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    """Formulario para crear/editar productos"""
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'categoria', 'disponible']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        return precio

# Formulario de búsqueda
class BusquedaForm(forms.Form):
    """Formulario para buscar productos"""
    OPCIONES_ORDEN = [
        ('nombre', 'Nombre A-Z'),
        ('-nombre', 'Nombre Z-A'),
        ('precio', 'Precio menor a mayor'),
        ('-precio', 'Precio mayor a menor'),
        ('-fecha_creacion', 'Más recientes'),
    ]
    
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar productos...'
        })
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activa=True),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    precio_min = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio mínimo'
        })
    )
    precio_max = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Precio máximo'
        })
    )
    ordenar_por = forms.ChoiceField(
        choices=OPCIONES_ORDEN,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

# ============================================================================
# 3. VISTAS QUE USAN FORMULARIOS
# ============================================================================

def vista_contacto(request):
    """Vista que maneja el formulario de contacto"""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Procesar datos del formulario
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            
            # Aquí podrías enviar un email, guardar en BD, etc.
            print(f"Contacto de {nombre} ({email}): {asunto}")
            
            messages.success(request, '¡Mensaje enviado correctamente!')
            return redirect('contacto')
    else:
        form = ContactoForm()
    
    return render(request, 'contacto.html', {'form': form})

@login_required
def vista_crear_producto(request):
    """Vista para crear un nuevo producto"""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.creado_por = request.user
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" creado correctamente!')
            return redirect('productos')
    else:
        form = ProductoForm()
    
    return render(request, 'productos/crear.html', {'form': form})

def vista_buscar_productos(request):
    """Vista con formulario de búsqueda"""
    form = BusquedaForm(request.GET)
    productos = Producto.objects.filter(disponible=True)
    
    if form.is_valid():
        busqueda = form.cleaned_data.get('busqueda')
        categoria = form.cleaned_data.get('categoria')
        precio_min = form.cleaned_data.get('precio_min')
        precio_max = form.cleaned_data.get('precio_max')
        ordenar_por = form.cleaned_data.get('ordenar_por')
        
        # Aplicar filtros
        if busqueda:
            productos = productos.filter(nombre__icontains=busqueda)
        if categoria:
            productos = productos.filter(categoria=categoria)
        if precio_min:
            productos = productos.filter(precio__gte=precio_min)
        if precio_max:
            productos = productos.filter(precio__lte=precio_max)
        if ordenar_por:
            productos = productos.order_by(ordenar_por)
    
    contexto = {
        'form': form,
        'productos': productos,
        'total': productos.count()
    }
    return render(request, 'productos/buscar.html', contexto)

# ============================================================================
# 4. CONFIGURACIÓN DE URLs PARA AUTENTICACIÓN
# ============================================================================

URL_PATTERNS_AUTH = """
# urls.py - URLs para autenticación y formularios

from django.urls import path
from . import views

urlpatterns = [
    # Autenticación
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('registro/', views.vista_registro, name='registro'),
    path('dashboard/', views.vista_dashboard, name='dashboard'),
    path('perfil/', views.vista_perfil, name='perfil'),
    
    # Formularios
    path('contacto/', views.vista_contacto, name='contacto'),
    path('productos/crear/', views.vista_crear_producto, name='crear_producto'),
    path('productos/buscar/', views.vista_buscar_productos, name='buscar_productos'),
]
"""

# ============================================================================
# 5. TEMPLATES (PLANTILLAS) - Ejemplos HTML
# ============================================================================

# Base template (base.html)
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Aplicación Django{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Mi App</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'dashboard' %}">Dashboard</a>
                    <a class="nav-link" href="{% url 'perfil' %}">Perfil</a>
                    <a class="nav-link" href="{% url 'logout' %}">Salir</a>
                {% else %}
                    <a class="nav-link" href="{% url 'login' %}">Iniciar Sesión</a>
                    <a class="nav-link" href="{% url 'registro' %}">Registrarse</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <!-- Mensajes -->
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

    <!-- Contenido principal -->
    <main class="container mt-4">
        {% block content %}
        {% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

# Template de login (auth/login.html)
LOGIN_TEMPLATE = '''
{% extends 'base.html' %}

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
'''

# Template con formulario (contacto.html)
CONTACTO_TEMPLATE = '''
{% extends 'base.html' %}

{% block title %}Contacto{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-8">
        <h2>Formulario de Contacto</h2>
        <form method="post">
            {% csrf_token %}
            <div class="mb-3">
                <label class="form-label">{{ form.nombre.label }}</label>
                {{ form.nombre }}
                {% if form.nombre.errors %}
                    <div class="text-danger">{{ form.nombre.errors }}</div>
                {% endif %}
            </div>
            <div class="mb-3">
                <label class="form-label">{{ form.email.label }}</label>
                {{ form.email }}
                {% if form.email.errors %}
                    <div class="text-danger">{{ form.email.errors }}</div>
                {% endif %}
            </div>
            <div class="mb-3">
                <label class="form-label">{{ form.asunto.label }}</label>
                {{ form.asunto }}
                {% if form.asunto.errors %}
                    <div class="text-danger">{{ form.asunto.errors }}</div>
                {% endif %}
            </div>
            <div class="mb-3">
                <label class="form-label">{{ form.mensaje.label }}</label>
                {{ form.mensaje }}
                {% if form.mensaje.errors %}
                    <div class="text-danger">{{ form.mensaje.errors }}</div>
                {% endif %}
            </div>
            <button type="submit" class="btn btn-primary">Enviar Mensaje</button>
        </form>
    </div>
</div>
{% endblock %}
'''

# ============================================================================
# 6. CONFIGURACIÓN EN SETTINGS.PY
# ============================================================================

SETTINGS_AUTH = """
# Configuraciones de autenticación en settings.py

# URL de redirección después del login
LOGIN_REDIRECT_URL = '/dashboard/'

# URL de redirección después del logout  
LOGOUT_REDIRECT_URL = '/'

# URL para login (cuando se requiere autenticación)
LOGIN_URL = '/login/'

# Configuración de mensajes
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
"""

# ============================================================================
# 💡 TIPS Y BUENAS PRÁCTICAS
# ============================================================================

"""
✅ BUENAS PRÁCTICAS - AUTENTICACIÓN:
- Usar @login_required para vistas protegidas
- Validar permisos en vistas sensibles
- Manejar mensajes de feedback al usuario
- Redirigir apropiadamente después de login/logout

✅ BUENAS PRÁCTICAS - FORMULARIOS:
- Usar {{ form.as_p }} para formularios rápidos
- Personalizar widgets para mejor UX
- Validar datos tanto en frontend como backend
- Usar {% csrf_token %} SIEMPRE en formularios POST

✅ BUENAS PRÁCTICAS - TEMPLATES:
- Usar template base para evitar repetición
- Organizar templates en carpetas por app
- Usar {% url %} en lugar de URLs hardcodeadas
- Escapar contenido dinámico automáticamente

⚠️ ERRORES COMUNES:
- Olvidar {% csrf_token %} en formularios
- No validar permisos en vistas protegidas
- Hardcodear URLs en templates
- No manejar errores de formularios

🔍 VERIFICACIÓN:
- Login/logout funcionan correctamente
- Formularios validan datos apropiadamente
- Templates renderizan sin errores
- Mensajes se muestran al usuario
- Redirecciones funcionan como esperado
"""

if __name__ == "__main__":
    print("🔐 Django - Autenticación y Formularios")
    print("=" * 50)
    print("📋 Checklist:")
    print("□ Sistema de autenticación configurado")
    print("□ Formularios creados y funcionando")
    print("□ Templates organizados y renderizando")
    print("□ Validaciones implementadas")
    print("□ Mensajes de feedback al usuario")
    print("\n🎉 ¡Sesión completa de Django!")


