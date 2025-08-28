# 👁️ Django - Vistas, URLs y Modelos
# Sesión 1.5 horas - Primera parte (continuación - 45 minutos)

"""
DJANGO BÁSICO I - VISTAS Y MODELOS

Tiempo estimado: 45 minutos
- URLs y Vistas (20 min)
- Modelos y Base de Datos (25 min)
"""

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import models
from django.contrib.auth.models import User

# ============================================================================
# 1. VISTAS BÁSICAS (20 minutos)
# ============================================================================

# Vista función básica
def vista_hola_mundo(request):
    """Vista más simple posible"""
    return HttpResponse("<h1>¡Hola Mundo desde Django!</h1>")

# Vista con parámetros
def vista_saludo(request, nombre):
    """Vista que recibe parámetros de la URL"""
    mensaje = f"<h1>¡Hola {nombre}!</h1>"
    return HttpResponse(mensaje)

# Vista con template
def vista_home(request):
    """Vista que usa un template HTML"""
    contexto = {
        'titulo': 'Mi Primera Página Django',
        'mensaje': 'Bienvenido a nuestra aplicación',
        'usuario': request.user.username if request.user.is_authenticated else 'Anónimo'
    }
    return render(request, 'home.html', contexto)

# Vista que retorna JSON
def vista_api_datos(request):
    """Vista tipo API que retorna JSON"""
    datos = {
        'mensaje': 'Datos desde Django',
        'usuarios_total': User.objects.count(),
        'metodo': request.method
    }
    return JsonResponse(datos)

# ============================================================================
# 2. CONFIGURACIÓN DE URLs
# ============================================================================

# urls.py de la aplicación (mi_app/urls.py)
URL_PATTERNS_APP = """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_home, name='home'),
    path('hola/', views.vista_hola_mundo, name='hola'),
    path('saludo/<str:nombre>/', views.vista_saludo, name='saludo'),
    path('api/datos/', views.vista_api_datos, name='api_datos'),
]
"""

# urls.py principal (mi_proyecto/urls.py)
URL_PATTERNS_PRINCIPAL = """
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mi_app.urls')),
]
"""

# ============================================================================
# 3. MODELOS DE BASE DE DATOS (25 minutos)
# ============================================================================

class Categoria(models.Model):
    """Modelo básico para categorías"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    """Modelo más complejo con relaciones"""
    
    # Campos básicos
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    # Relación con categoría (ForeignKey)
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE,
        related_name='productos'
    )
    
    # Relación con usuario (quien creó el producto)
    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Campos de fecha
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Campos booleanos
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
    
    def esta_disponible(self):
        """Método personalizado"""
        return self.disponible and self.stock > 0

class Cliente(models.Model):
    """Modelo con choices y validaciones"""
    
    TIPOS_CLIENTE = [
        ('regular', 'Cliente Regular'),
        ('premium', 'Cliente Premium'),
        ('vip', 'Cliente VIP'),
    ]
    
    # Información personal
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    
    # Tipo de cliente
    tipo = models.CharField(
        max_length=10,
        choices=TIPOS_CLIENTE,
        default='regular'
    )
    
    # Fechas
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_ultima_compra = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['apellido', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

# ============================================================================
# 4. VISTAS QUE USAN MODELOS
# ============================================================================

def vista_productos(request):
    """Vista que muestra productos desde la base de datos"""
    productos = Producto.objects.filter(disponible=True)
    categorias = Categoria.objects.filter(activa=True)
    
    contexto = {
        'productos': productos,
        'categorias': categorias,
        'total_productos': productos.count()
    }
    return render(request, 'productos.html', contexto)

def vista_producto_detalle(request, producto_id):
    """Vista de detalle de un producto específico"""
    try:
        producto = Producto.objects.get(id=producto_id, disponible=True)
        productos_relacionados = Producto.objects.filter(
            categoria=producto.categoria,
            disponible=True
        ).exclude(id=producto_id)[:4]
        
        contexto = {
            'producto': producto,
            'productos_relacionados': productos_relacionados
        }
        return render(request, 'producto_detalle.html', contexto)
    except Producto.DoesNotExist:
        return HttpResponse("Producto no encontrado", status=404)

def vista_productos_categoria(request, categoria_id):
    """Vista que filtra productos por categoría"""
    categoria = Categoria.objects.get(id=categoria_id)
    productos = Producto.objects.filter(
        categoria=categoria,
        disponible=True
    )
    
    contexto = {
        'categoria': categoria,
        'productos': productos,
        'total': productos.count()
    }
    return render(request, 'productos_categoria.html', contexto)

# ============================================================================
# 5. COMANDOS DE MIGRACIÓN
# ============================================================================

COMANDOS_MIGRACION = """
# Después de crear/modificar modelos:

# 1. Crear migraciones
python manage.py makemigrations

# 2. Ver las migraciones pendientes
python manage.py showmigrations

# 3. Aplicar migraciones
python manage.py migrate

# 4. Ver SQL de una migración
python manage.py sqlmigrate mi_app 0001

# 5. Crear datos iniciales (opcional)
python manage.py shell
>>> from mi_app.models import Categoria, Producto
>>> cat = Categoria.objects.create(nombre="Electrónicos")
>>> prod = Producto.objects.create(nombre="Laptop", precio=15000, categoria=cat)
"""

# ============================================================================
# 6. ADMIN DJANGO (Bonus)
# ============================================================================

# admin.py - Para registrar modelos en el admin
ADMIN_REGISTRATION = """
from django.contrib import admin
from .models import Categoria, Producto, Cliente

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'fecha_creacion']
    list_filter = ['activa']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'disponible']
    list_filter = ['categoria', 'disponible', 'destacado']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'disponible']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'email', 'tipo', 'fecha_registro']
    list_filter = ['tipo']
    search_fields = ['nombre', 'apellido', 'email']
"""

# ============================================================================
# 💡 TIPS Y BUENAS PRÁCTICAS
# ============================================================================

"""
✅ BUENAS PRÁCTICAS - VISTAS:
- Usar nombres descriptivos para vistas y URLs
- Manejar excepciones (DoesNotExist, etc.)
- Separar lógica compleja en funciones auxiliares
- Usar contexto descriptivo para templates

✅ BUENAS PRÁCTICAS - MODELOS:
- Usar __str__() para representación legible
- Agregar Meta class para configuraciones
- Usar related_name en ForeignKey
- Validar datos en el modelo cuando sea posible

⚠️ ERRORES COMUNES:
- Olvidar hacer migraciones después de cambios
- No manejar excepciones en vistas
- Usar nombres confusos en URLs
- No optimizar consultas (N+1 queries)

🔍 VERIFICACIÓN:
- Las URLs responden correctamente
- Los modelos se crean sin errores
- El admin muestra los modelos registrados
- Las relaciones funcionan correctamente
"""

if __name__ == "__main__":
    print("👁️ Django - Vistas y Modelos")
    print("=" * 50)
    print("📋 Checklist:")
    print("□ URLs configuradas correctamente")
    print("□ Vistas básicas funcionando")
    print("□ Modelos creados y migrados")
    print("□ Admin configurado")
    print("□ Relaciones entre modelos funcionando")
    print("\n🎯 ¡Listo para autenticación y formularios!")


