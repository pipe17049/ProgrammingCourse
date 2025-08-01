# 🖼️ Pipeline de Procesamiento de Imágenes Distribuido

**Proyecto de 4 días: De Threading a Sistemas Distribuidos**

Este proyecto evoluciona desde un servidor Django básico hasta un **sistema distribuido de procesamiento de imágenes** completo, demostrando conceptos de concurrencia, paralelismo y arquitecturas distribuidas.

## 🎯 Objetivos del Proyecto

### **📅 DÍA 1: Foundation** 
- ✅ **I/O-bound operations**: Leer archivos grandes del disco
- ✅ **Threading vs Multiprocessing**: Comparación de rendimiento  
- ✅ **Load testing**: Medición de concurrencia

### **📅 DÍA 2: Real Processing**
- ✅ **Filtros reales**: PIL (Pillow) y OpenCV 
- ✅ **CPU-bound tasks**: Blur, sharpen, edge detection, resize
- ✅ **Performance benchmarking**: Sequential vs Threading vs Multiprocessing
- ✅ **Resource monitoring**: CPU, memory, processing time

### **📅 DÍA 3: Distributed System** 
- ✅ **Sistema distribuido**: Redis + Worker containers
- ✅ **Load balancing**: FIFO queue con workers especializados
- ✅ **Fault tolerance**: Worker registration, heartbeat, failure handling
- ✅ **Docker orchestration**: docker-compose con múltiples servicios
- ✅ **Monitoring**: Worker status, task tracking, performance metrics

## 🏗️ Arquitectura del Sistema

```
                    🌐 Client
                (curl requests)
                       |
                ⚖️ Load Balancer
               (Docker Compose)
                  /    |    \
                 /     |     \
            🐍 API-1  🐍 API-2  🐍 API-3
            :8000     :8001     :8002
                 \     |     /
                  \    |    /
                📡 Redis Queue
              (Task Distribution
               Worker Registry)
                   /  |  \
                  /   |   \
                 /    |    \
            👷 Worker-1  👷 Worker-2  👷 Worker-3
           I/O Specialist CPU Specialist General Purpose
           resize, blur,   sharpen,      ALL FILTERS
           brightness     edges            |
                |           |              |
                |           |              |
           🖼️ Static Images ←→ 💾 Processed Images
           sample_4k.jpg      static/processed/
           misurina-sunset.jpg
                
    📊 Monitoring Dashboard
    ├── Worker Status & Heartbeat
    ├── Task Queue Length  
    ├── Processing Times
    └── Success/Failure Rates
```

### **🔄 Flujo de Procesamiento:**

```
1. 📤 Client: POST /api/process-batch/distributed/
                    ↓
2. 🐍 API: Crea tasks en Redis Queue (FIFO)
                    ↓
3. 📡 Redis: [task1, task2, task3] → Workers pull (BRPOP)
                    ↓
4. 👷 Worker: Revisa capabilities DESPUÉS de tomar task
                    ↓
5a. ✅ Compatible: Procesa → Guarda resultado
5b. ❌ Incompatible: Marca como FAILED (💀 Se pierde)
                    ↓
6. 📊 Client: Revisar respuesta con resultados/errores
```

## 🚀 Setup y Ejecución

### **Opción A: Setup Local (Días 1-2)**

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear directorios necesarios
mkdir -p static/processed

# 3. Ejecutar servidor local
python manage.py runserver 8000
```

### **Opción B: Setup Distribuido con Docker (Día 3)**

```bash
# 1. Construir imágenes
docker-compose build

# 2. Levantar sistema completo
docker-compose up -d

# 3. Verificar servicios
docker-compose ps
```

### **Verificar instalación:**
```bash
# Health check
curl http://localhost:8000/api/health/

# Ver workers activos (solo Docker)
curl http://localhost:8000/api/workers/status/
```

## 🧪 Testing y Comandos

### **📅 DÍA 1: Endpoints Básicos**

```bash
# Health check
curl http://localhost:8000/api/health/

# Información de imagen (rápido)
curl http://localhost:8000/api/image/info/

# Descargar imagen 4K (I/O-bound)  
curl http://localhost:8000/api/image/4k/ -o downloaded_4k.jpg

# Imagen con procesamiento lento
curl "http://localhost:8000/api/image/slow/?delay=3.0" -o slow_4k.jpg

# Estadísticas del servidor
curl http://localhost:8000/api/stats/
```

### **📅 DÍA 2: Filtros Reales (PIL/OpenCV)**

```bash
# Procesamiento con filtros secuencial
curl -X POST http://localhost:8000/api/process-batch/sequential/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["resize", "blur"], "filter_params": {"resize": {"width": 800, "height": 600}, "blur": {"radius": 3.0}}}'

# Procesamiento con threading
curl -X POST http://localhost:8000/api/process-batch/threading/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["sharpen", "edges"]}'

# Procesamiento con multiprocessing
curl -X POST http://localhost:8000/api/process-batch/multiprocessing/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["brightness"], "filter_params": {"brightness": {"factor": 1.5}}}'

# Comparar todos los métodos
curl -X POST http://localhost:8000/api/process-batch/compare-all/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["resize", "blur"]}'

# Stress test
curl -X POST http://localhost:8000/api/process-batch/stress/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["sharpen", "edges"], "num_iterations": 5}'
```

### **📅 DÍA 3: Sistema Distribuido (Docker)**

```bash
# Procesamiento distribuido
curl -X POST http://localhost:8000/api/process-batch/distributed/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["resize", "sharpen", "edges"], "filter_params": {"resize": {"width": 1024, "height": 768}}}'

# Estado de workers
curl http://localhost:8000/api/workers/status/ | python -m json.tool

# Monitoreo en tiempo real
watch -n 2 'curl -s http://localhost:8000/api/workers/status/ | python -m json.tool'

# Consultar estado de task individual (usar task_id de la respuesta anterior)
curl http://localhost:8000/api/task/{TASK_ID}/status/ | python -m json.tool
```

### **🎯 Testing Worker Specialization**

```bash
# Test: Solo worker-2 puede hacer 'sharpen'
# 1. Parar worker-3: docker-compose stop worker-3
# 2. Enviar múltiples tareas sharpen:
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/process-batch/distributed/ \
    -H "Content-Type: application/json" \
    -d '{"filters": ["sharpen"]}' &
done

# 3. Ver resultados: worker-1 falla, worker-2 procesa
curl http://localhost:8000/api/workers/status/
```

### **🔍 Testing Job Failure vs Worker Failure**

```bash
# SCENARIO 1: Job Failure (Worker incompatible)
# 1. Enviar task que worker-1 no puede manejar
curl -X POST http://localhost:8000/api/process-batch/distributed/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["sharpen"]}' \
  | jq '.task_id' # Guardar task_id

# 2. Consultar status específico del job
curl http://localhost:8000/api/task/{TASK_ID}/status/ | jq '
{
  status: .status,
  failure_type: .failure_type,
  failure_reason: .failure_reason,
  explanation: .explanation,
  error: .error
}'

# RESPUESTA de Job Failure:
# {
#   "status": "failed",
#   "failure_type": "job_failure",
#   "failure_reason": "worker_capability_mismatch", 
#   "explanation": "Worker tomó task pero no puede manejar el filtro requerido",
#   "error": "Worker worker-1 cannot handle filters: ['sharpen']"
# }

# SCENARIO 2: Worker Failure (Worker caído)
# 1. Parar todos los workers
docker-compose stop worker-1 worker-2 worker-3

# 2. Enviar task
curl -X POST http://localhost:8000/api/process-batch/distributed/ \
  -H "Content-Type: application/json" \
  -d '{"filters": ["resize"]}' \
  | jq '.task_id'

# 3. Consultar después de timeout
curl http://localhost:8000/api/task/{TASK_ID}/status/ | jq '
{
  status: .status,
  explanation: "No workers available to process task"
}'

# RESPUESTA de Worker Failure:
# {
#   "status": "pending",  # Task nunca fue tomada
#   "explanation": "No workers available to process task"
# }
```

## 📊 Endpoints Disponibles

### **DÍA 1: Básicos**
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/health/` | GET | Health check del servidor |
| `/api/image/info/` | GET | Metadata de imagen sin transferir |
| `/api/image/4k/` | GET | Descargar imagen 4K (I/O-bound) |
| `/api/image/slow/?delay=N` | GET | Imagen con delay simulado |
| `/api/stats/` | GET | Estadísticas del servidor |

### **DÍA 2: Procesamiento Real**
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/process-batch/sequential/` | POST | Procesamiento secuencial con filtros |
| `/api/process-batch/threading/` | POST | Procesamiento con threading |
| `/api/process-batch/multiprocessing/` | POST | Procesamiento con multiprocessing |
| `/api/process-batch/compare/` | POST | Comparar threading vs multiprocessing |
| `/api/process-batch/compare-all/` | POST | Comparar todos los métodos |
| `/api/process-batch/stress/` | POST | Test de estrés con múltiples iteraciones |

### **DÍA 3: Sistema Distribuido**
| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/process-batch/distributed/` | POST | Procesamiento distribuido con workers |
| `/api/workers/status/` | GET | Estado de todos los workers |
| `/api/task/<task_id>/status/` | GET | **Estado de task individual** (job failure vs worker failure) |

### **Filtros Disponibles:**
- **`resize`**: Cambiar tamaño (PIL) - I/O-bound
- **`blur`**: Difuminado gaussiano (PIL) - I/O-bound  
- **`brightness`**: Ajuste de brillo (PIL) - I/O-bound
- **`sharpen`**: Nitidez avanzada (OpenCV) - CPU-bound
- **`edges`**: Detección de bordes (OpenCV) - CPU-bound

## 🔍 Análisis de Rendimiento

### **🏃‍♂️ DÍA 2: Threading vs Multiprocessing**

**Para filtros I/O-bound (resize, blur, brightness):**
- ✅ **Threading wins**: ~3-5x más rápido que secuencial
- ⚡ **Multiprocessing**: ~2-3x más rápido (overhead de procesos)
- 🧠 **Razón**: GIL se libera durante I/O, threading es más eficiente

**Para filtros CPU-bound (sharpen, edges):**
- ✅ **Multiprocessing wins**: ~4-6x más rápido que secuencial  
- 🐌 **Threading**: ~1.2x más rápido (limitado por GIL)
- 🧠 **Razón**: CPU-bound necesita verdadero paralelismo

### **🌐 DÍA 3: Sistema Distribuido**

**Características del FIFO Queue:**
- ⚖️ **Load Balancing**: Simple FIFO, no inteligente
- ❌ **Fault Tolerance**: Tareas fallan si worker incompatible las toma
- 🎯 **Worker Specialization**: Configurado por `WORKER_CAPABILITIES`
- 📊 **Monitoring**: Worker registry con heartbeat

**Worker-3 como "Salvador":**
- 🛡️ Worker-3 (`capabilities=all`) previene fallos
- 🎲 Distribución basada en timing, no capabilities
- ⚠️ Si worker-3 se cae, tareas incompatibles fallan para siempre

## 🛠️ Troubleshooting

### **Local Setup Issues**
```bash
# Dependencias faltantes
pip install -r requirements.txt

# Directorios faltantes  
mkdir -p static/processed static/images

# Puerto en uso
python manage.py runserver 8080
```

### **Docker Issues**
```bash
# Servicios no inician
docker-compose down && docker-compose up --build

# Redis connection failed
docker-compose logs redis

# Workers no registran
docker-compose logs worker-1
```

### **Workers No Processan**
```bash
# Verificar workers activos
curl http://localhost:8000/api/workers/status/

# Verificar cola Redis
docker-compose exec redis redis-cli LLEN task_queue

# Restart workers
docker-compose restart worker-1 worker-2 worker-3
```

## 🏆 Logros del Proyecto

### **📈 Progresión Técnica:**
1. **Día 1**: Servidor básico I/O-bound → Threading fundamentals
2. **Día 2**: Filtros reales PIL/OpenCV → CPU vs I/O bound analysis  
3. **Día 3**: Sistema distribuido → Redis, Docker, Load balancing

### **🎯 Conceptos Demostrados:**
- ✅ **GIL Impact**: Threading vs Multiprocessing en diferentes workloads
- ✅ **Real-world Libraries**: PIL, OpenCV, Redis en production
- ✅ **Distributed Architectures**: Message queues, worker pools, fault tolerance
- ✅ **DevOps Integration**: Docker, docker-compose, multi-service systems
- ✅ **Performance Analysis**: Benchmarking, monitoring, bottleneck identification

---

**🚀 De conceptos básicos de concurrencia a sistemas distribuidos production-ready en 3 días!**

## 🖥️ **SETUP PARA WINDOWS**

### **Instalación rápida:**
```cmd
# 1. Ir a Projects folder
cd ProgrammingCourse\Chapter-Threads\Projects

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear directorio
mkdir static\processed

# 5. Verificar
python manage.py check

# 6. Iniciar servidor
python manage.py runserver 8000
```

### **Probar filtros nuevos:**
```cmd
curl -X POST http://localhost:8000/api/process-batch/threading/ -H "Content-Type: application/json" -d "{\"filters\": [\"resize\", \"blur\"], \"filter_params\": {\"resize\": {\"width\": 800, \"height\": 600}, \"blur\": {\"radius\": 3.0}}}"
```

**Nuevos endpoints:**
- `/api/process-batch/sequential/` - Procesamiento secuencial
- `/api/process-batch/threading/` - Con threading  
- `/api/process-batch/multiprocessing/` - Con multiprocessing
- `/api/process-batch/compare-all/` - Comparar todos los métodos
