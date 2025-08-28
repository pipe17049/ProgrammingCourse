# 🚀 Django - Configuración Inicial del Proyecto
# Sesión 1.5 horas - Primera parte (45 minutos)

"""
DJANGO BÁSICO I - CONFIGURACIÓN DEL PROYECTO

Tiempo estimado: 45 minutos
- Creación del proyecto (15 min)
- Configuración inicial (15 min)  
- Primer servidor de desarrollo (15 min)
"""

# ============================================================================
# 1. INSTALACIÓN Y CONFIGURACIÓN INICIAL (15 minutos)
# ============================================================================

# Paso 1: Crear entorno virtual
# python -m venv django_env

# Paso 2: Activar entorno virtual
# Windows: django_env\Scripts\activate
# Mac/Linux: source django_env/bin/activate

# Paso 3: Instalar Django
# pip install django

# Paso 4: Verificar instalación
# django-admin --version

# ============================================================================
# 2. CREAR PROYECTO DJANGO (15 minutos)
# ============================================================================

# Paso 1: Crear proyecto
# django-admin startproject mi_proyecto

# Paso 2: Navegar al proyecto
# cd mi_proyecto

# Paso 3: Estructura del proyecto generado
"""
mi_proyecto/
├── manage.py              # Herramienta de administración
├── mi_proyecto/
│   ├── __init__.py       # Paquete Python
│   ├── settings.py       # Configuraciones del proyecto
│   ├── urls.py           # URLs principales
│   ├── wsgi.py           # Configuración WSGI
│   └── asgi.py           # Configuración ASGI
"""

# ============================================================================
# 3. CONFIGURACIÓN BÁSICA - settings.py (15 minutos)
# ============================================================================

# Configuración de ejemplo para settings.py
CONFIGURACION_BASICA = {
    'DEBUG': True,  # Solo en desarrollo
    'ALLOWED_HOSTS': ['localhost', '127.0.0.1'],
    
    # Base de datos SQLite (por defecto)
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    },
    
    # Idioma y zona horaria
    'LANGUAGE_CODE': 'es-es',
    'TIME_ZONE': 'America/Mexico_City',
    'USE_I18N': True,
    'USE_TZ': True,
}

# ============================================================================
# 4. PRIMER SERVIDOR DE DESARROLLO
# ============================================================================

# Comando para ejecutar el servidor
# python manage.py runserver

# El servidor estará disponible en:
# http://127.0.0.1:8000/

# ============================================================================
# 5. CREAR PRIMERA APLICACIÓN
# ============================================================================

# Comando para crear una aplicación
# python manage.py startapp mi_app

# Estructura de la aplicación generada
"""
mi_app/
├── __init__.py
├── admin.py              # Administración
├── apps.py               # Configuración de la app
├── migrations/           # Migraciones de BD
├── models.py             # Modelos de datos
├── tests.py              # Pruebas
└── views.py              # Vistas (lógica)
"""

# ============================================================================
# 6. REGISTRAR LA APLICACIÓN
# ============================================================================

# En settings.py, agregar a INSTALLED_APPS:
INSTALLED_APPS_EJEMPLO = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mi_app',  # ← Agregar nuestra aplicación
]

# ============================================================================
# 7. COMANDOS ÚTILES PARA RECORDAR
# ============================================================================

COMANDOS_DJANGO = {
    'crear_proyecto': 'django-admin startproject nombre_proyecto',
    'crear_app': 'python manage.py startapp nombre_app',
    'servidor': 'python manage.py runserver',
    'servidor_puerto': 'python manage.py runserver 8080',
    'migraciones': 'python manage.py makemigrations',
    'aplicar_migraciones': 'python manage.py migrate',
    'superusuario': 'python manage.py createsuperuser',
    'shell': 'python manage.py shell',
}

# ============================================================================
# 💡 TIPS IMPORTANTES
# ============================================================================

"""
✅ BUENAS PRÁCTICAS:
- Siempre usar entornos virtuales
- Mantener DEBUG=False en producción
- Usar nombres descriptivos para aplicaciones
- Documentar configuraciones especiales

⚠️ ERRORES COMUNES:
- Olvidar activar el entorno virtual
- No registrar la app en INSTALLED_APPS
- Ejecutar servidor sin hacer migraciones
- Usar DEBUG=True en producción

🔍 VERIFICACIÓN:
- El servidor corre sin errores
- Se puede acceder a http://127.0.0.1:8000/
- La aplicación aparece en INSTALLED_APPS
- No hay mensajes de error en consola
"""

if __name__ == "__main__":
    print("🐍 Django - Configuración del Proyecto")
    print("=" * 50)
    print("📋 Checklist de configuración:")
    print("□ Entorno virtual creado y activado")
    print("□ Django instalado")
    print("□ Proyecto creado")
    print("□ Aplicación creada")
    print("□ App registrada en settings.py")
    print("□ Servidor ejecutándose correctamente")
    print("\n🚀 ¡Listo para continuar con vistas y modelos!")


