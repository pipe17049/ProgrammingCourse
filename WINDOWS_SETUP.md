# 🖥️ **GUÍA DE SETUP PARA WINDOWS**

## 📋 **REQUISITOS PREVIOS**

### 1️⃣ **Python 3.8+**
```cmd
# Verificar si tienes Python instalado
python --version
# o
python3 --version

# Si no tienes Python, descarga desde:
# https://www.python.org/downloads/windows/
# ⚠️ IMPORTANTE: Marca "Add Python to PATH" durante la instalación
```

### 2️⃣ **Git (Opcional pero recomendado)**
```cmd
# Verificar si tienes Git
git --version

# Si no tienes Git, descarga desde:
# https://git-scm.com/download/win
```

---

## 🚀 **INSTALACIÓN PASO A PASO**

### **PASO 1: Clonar/Descargar el Proyecto**
```cmd
# Opción A: Con Git
git clone <URL_DEL_REPOSITORIO>
cd ProgrammingCourse\Chapter-Threads\Projects

# Opción B: Descargar ZIP y extraer
# Navegar a la carpeta: ProgrammingCourse\Chapter-Threads\Projects
```

### **PASO 2: Crear Entorno Virtual** (Recomendado)
```cmd
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Verificar que está activo (deberías ver (venv) en el prompt)
```

### **PASO 3: Instalar Dependencias**
```cmd
# Instalar dependencias básicas
pip install Django==4.2.7 psutil==5.9.6

# Instalar dependencias extendidas para filtros reales
pip install Pillow opencv-python numpy

# Instalar dependencias de testing (opcional)
pip install pytest pytest-benchmark

# O instalar todo de una vez:
pip install -r requirements_extended.txt
```

### **PASO 4: Crear Directorios Necesarios**
```cmd
# Crear directorio para imágenes procesadas
mkdir static\processed

# Verificar estructura
dir static
# Deberías ver: images\ y processed\
```

### **PASO 5: Verificar Instalación**
```cmd
# Verificar Django
python manage.py check

# Verificar que las librerías están disponibles
python -c "import PIL; print('PIL: OK')"
python -c "import cv2; print('OpenCV: OK')"
python -c "import numpy; print('NumPy: OK')"
```

---

## 🎯 **EJECUTAR EL PROYECTO**

### **1️⃣ Iniciar el Servidor**
```cmd
# Desde Chapter-Threads\Projects\
python manage.py runserver 8000

# Deberías ver:
# Starting development server at http://127.0.0.1:8000/
```

### **2️⃣ Probar en Nueva Terminal** (Mantén el servidor corriendo)
```cmd
# Abrir nueva terminal/cmd
# Navegar a la misma carpeta
cd ProgrammingCourse\Chapter-Threads\Projects

# Probar endpoint básico
curl http://localhost:8000/api/health/ || python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/api/health/').read().decode())"
```

### **3️⃣ Probar Filtros** (Ejemplo completo)
```cmd
# Usando curl (si está disponible)
curl -X POST http://localhost:8000/api/process-batch/threading/ ^
  -H "Content-Type: application/json" ^
  -d "{\"filters\": [\"resize\", \"blur\"], \"filter_params\": {\"resize\": {\"width\": 800, \"height\": 600}, \"blur\": {\"radius\": 3.0}}}"

# O usando PowerShell
powershell -Command "Invoke-RestMethod -Uri 'http://localhost:8000/api/process-batch/threading/' -Method POST -Headers @{'Content-Type'='application/json'} -Body '{\"filters\": [\"resize\", \"blur\"], \"filter_params\": {\"resize\": {\"width\": 800, \"height\": 600}, \"blur\": {\"radius\": 3.0}}}'"
```

---

## 🛠️ **SOLUCIÓN DE PROBLEMAS COMUNES EN WINDOWS**

### **❌ Error: "python no se reconoce"**
```cmd
# Solución: Agregar Python al PATH
# 1. Buscar "Variables de entorno" en Windows
# 2. Agregar a PATH: C:\Python39\ y C:\Python39\Scripts\
# 3. Reiniciar terminal
```

### **❌ Error: "pip no se reconoce"**
```cmd
# Solución: Reinstalar pip
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### **❌ Error: "Microsoft Visual C++ 14.0 is required"**
```cmd
# Solución: Instalar Microsoft C++ Build Tools
# Descargar desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# O usar precompilados:
pip install --only-binary=all opencv-python
```

### **❌ Error: "Access denied" al crear directorios**
```cmd
# Solución: Ejecutar terminal como Administrador
# Click derecho en CMD/PowerShell → "Ejecutar como administrador"
```

### **❌ Puerto 8000 ocupado**
```cmd
# Solución: Usar otro puerto
python manage.py runserver 8080

# Y cambiar en las pruebas:
# http://localhost:8080/api/health/
```

---

## 📦 **ARCHIVOS INCLUIDOS**

```
Chapter-Threads/Projects/
├── manage.py                 # Django management
├── requirements_extended.txt # Todas las dependencias
├── django_image_server/      # Configuración Django
├── image_api/               # API principal
│   ├── views.py            # Endpoints
│   ├── processors.py       # Lógica de procesamiento
│   └── filters.py          # Filtros de imagen
├── static/
│   ├── images/             # Imágenes originales
│   └── processed/          # Imágenes procesadas (crear)
├── workers/                # Trabajadores multiprocessing
├── benchmarks/             # Scripts de benchmark
└── tests/                  # Tests unitarios
```

---

## ✅ **VERIFICACIÓN FINAL**

### **1️⃣ Servidor funcionando**
```cmd
# Debería responder:
curl http://localhost:8000/api/health/
# {"status": "healthy", "timestamp": "..."}
```

### **2️⃣ Imágenes disponibles**
```cmd
dir static\images
# Deberías ver archivos .jpg
```

### **3️⃣ Procesamiento funcionando**
```cmd
# Debería procesar y guardar en static\processed\
curl -X POST http://localhost:8000/api/process-batch/sequential/ -H "Content-Type: application/json" -d "{\"filters\": [\"resize\"], \"filter_params\": {\"resize\": {\"width\": 400, \"height\": 300}}}"
```

---

## 🔧 **COMANDOS ÚTILES PARA DESARROLLO**

```cmd
# Activar entorno virtual
venv\Scripts\activate

# Desactivar entorno virtual
deactivate

# Ver dependencias instaladas
pip list

# Actualizar dependencias
pip install --upgrade -r requirements_extended.txt

# Ejecutar tests (si están disponibles)
python -m pytest tests/

# Ver logs del servidor
python manage.py runserver --verbosity=2
```

---

## 🎯 **LISTO PARA USAR**

Una vez completados todos los pasos, tendrás:
- ✅ Servidor Django funcionando
- ✅ Filtros reales (PIL + OpenCV) 
- ✅ Threading y Multiprocessing
- ✅ Endpoints de comparación
- ✅ Imágenes procesadas guardándose

**¡Tu proyecto estará 100% listo para demostrar concurrencia y paralelismo en Windows!** 🎉 