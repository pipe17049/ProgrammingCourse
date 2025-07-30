# ProgrammingCourse

## AriasAenima

## Here I am going to share your homeworks and you have to pull the changes

## Test pull

## Hola mundo 

## :)

## 🦆
## :smile:

---

## 🖥️ **SETUP PARA WINDOWS**

### **Requisitos:**
- Python 3.8+ con "Add to PATH" habilitado
- Git (opcional)

### **Instalación rápida:**
```cmd
# 1. Ir a Projects folder
cd ProgrammingCourse\Chapter-Threads\Projects

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install Django==4.2.7 psutil==5.9.6 Pillow opencv-python numpy

# 4. Crear directorio
mkdir static\processed

# 5. Verificar
python manage.py check

# 6. Iniciar servidor
python manage.py runserver 8000
```

### **Probar filtros:**
```cmd
curl -X POST http://localhost:8000/api/process-batch/threading/ -H "Content-Type: application/json" -d "{\"filters\": [\"resize\", \"blur\"], \"filter_params\": {\"resize\": {\"width\": 800, \"height\": 600}, \"blur\": {\"radius\": 3.0}}}"
```

**Endpoints disponibles:**
- `/api/health/` - Verificar servidor
- `/api/process-batch/sequential/` - Procesamiento secuencial
- `/api/process-batch/threading/` - Con threading  
- `/api/process-batch/multiprocessing/` - Con multiprocessing
- `/api/process-batch/compare-all/` - Comparar todos los métodos
