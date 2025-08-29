# 🐍 Sesión Django Core - 1.5 Horas

## 📋 Agenda de la Sesión

**Duración Total:** 90 minutos  
**Enfoque:** Django fundamentals - **SIN admin panel**  
**Objetivo:** Entender el flujo core de Django: URL → Vista → Template

---

## 🗓️ Cronograma Simplificado

### ⏰ Primera Parte (45 minutos) - Django Básico
- **🚀 Proyecto y App** (10 min) - Estructura de Django
- **🗄️ Modelos y BD** (15 min) - Definir y migrar datos  
- **👁️ Vistas** (10 min) - Lógica de negocio
- **🔗 URLs** (10 min) - Rutas y navegación

### ☕ Descanso (5 minutos)

### ⏰ Segunda Parte (40 minutos) - Django Web
- **🎨 Templates** (15 min) - HTML dinámico
- **📝 Formularios** (12 min) - Capturar datos del usuario
- **🔐 Autenticación Básica** (13 min) - Login/logout simple

---

## 📚 Contenido de la Sesión

### 📁 Estructura de Archivos
```
Django/
├── README.md                # Este archivo - Guía de la sesión  
├── ejercicios/              # Ejercicios prácticos paso a paso
│   ├── ejercicio_1.md       # Django Core (modelos, vistas, URLs)
│   └── ejercicio_2.md       # Django Web (forms, auth, templates)
└── templates_examples/      # Ejemplos de HTML para referencia
    ├── base.html            # Template base con Bootstrap
    ├── formulario_ejemplo.html
    └── lista_ejemplo.html
```

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta sesión, los estudiantes **entenderán el flujo completo de Django**:

### Flujo de Datos Django
- ✅ **Usuario** hace request → **URL** encuentra patrón → **Vista** procesa → **Template** responde
- ✅ **Modelos** definen estructura de datos y **Migraciones** actualizan base de datos
- ✅ **Templates** renderizan HTML dinámico con datos del contexto
- ✅ **Formularios** capturan y validan entrada del usuario

### Habilidades Prácticas
- ✅ Crear proyecto Django funcional (blog)
- ✅ Definir modelos con relaciones
- ✅ Configurar URLs y vistas  
- ✅ Diseñar templates responsivos
- ✅ Implementar autenticación básica

---

## 🛠️ Requisitos Previos

- Python 3.8+ instalado
- Conocimientos básicos de Python
- Editor de código (VS Code, PyCharm, etc.)
- Terminal/Línea de comandos

## 📦 Instalación de Django

```bash
# Crear entorno virtual
python -m venv django_env

# Activar entorno virtual
# En Windows:
django_env\Scripts\activate
# En Mac/Linux:
source django_env/bin/activate

# Instalar Django
pip install django

# Verificar instalación
django-admin --version
```

---

## 🚀 Comenzar la Sesión

### 📋 Orden de los Ejercicios:

1. **Ejercicio 1** (`ejercicios/ejercicio_1.md`) - 25 min
   - ✅ Crear proyecto Django desde cero
   - ✅ Definir modelos y hacer migraciones
   - ✅ Crear vistas y configurar URLs
   - ✅ Hacer templates básicos
   - **Resultado:** Blog funcional básico

2. **Ejercicio 2** (`ejercicios/ejercicio_2.md`) - 30 min  
   - ✅ Agregar formularios Django
   - ✅ Implementar autenticación básica
   - ✅ Mejorar templates con Bootstrap
   - ✅ Agregar navegación dinámica
   - **Resultado:** Blog completo e interactivo

### 🎯 Al Final Tendrás:
Un blog Django completamente funcional con:
- 📝 Crear, leer posts
- 👤 Registro y autenticación de usuarios  
- 🎨 Diseño responsive con Bootstrap
- 🔐 Rutas protegidas por login
- 📱 Navegación dinámica según estado

**¡Sin admin panel! Solo Django puro y conceptos fundamentales! 🚀**
