# Chapter-CI: Producer-Consumer WebSocket System

Sistema de aprendizaje que implementa un patrón **Productor-Consumidor** usando Django, WebSockets y Docker.

## 📋 Descripción del Sistema

Este proyecto consta de dos aplicaciones principales:

- **`my_first_ci_project`** (Productor): API REST Django + Servidor WebSocket
- **`my_first_consumer`** (Consumidor): Cliente WebSocket que escucha eventos en tiempo real

## 🏗️ Arquitectura

### Flujo de Comunicación Real:
```
POST /api/product/     WebSocket Client      WebSocket Broadcast
┌─────────────────┐ ────────────────────► ┌─────────────────┐ ──────────► ┌─────────────────┐
│   Client        │                       │  WebSocket      │             │   Consumer      │
│  (Postman)      │                       │   Server        │             │   (Cliente)     │
└─────────────────┘                       │   :8765         │             └─────────────────┘
         │                                └─────────────────┘                        │
         │                                         ▲                                │
         ▼                                         │                                ▼
┌─────────────────┐                                │                    📺 Real-time notifications
│   Django API    │ ───────────────────────────────┘                    🎉 Product created!
│     :8000       │   Django connects as WS client                      📦 ID: xxx...
│                 │   when product is created                           🏷️ Name: Product
└─────────────────┘                                                     💰 Price: $XX.XX
         │
         ▼
┌─────────────────┐
│    MongoDB      │
│     :27017      │
└─────────────────┘
```

### Arquitectura Interna del Producer:
```
Container: producer
├── Process 1: Django Server (:8000)        ← API REST
├── Process 2: WebSocket Server (:8765)     ← Real-time messaging
└── Shared: MongoDB connection
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Docker & Docker Compose
- Python 3.11+ (para ejecutar consumidor local)

### Estructura del proyecto
```
Chapter-CI/
├── my_first_ci_project/         # Proyecto Django (Productor)
│   ├── docker-compose.yml       # ⚠️ Docker Compose INDIVIDUAL
│   ├── api/                     # App Django
│   ├── websocket_server.py      # Servidor WebSocket
│   └── start_services.py        # Script para levantar Django + WebSocket
├── my_first_consumer/           # Cliente WebSocket (Consumidor)
│   ├── websocket_client.py      # Cliente principal
│   ├── test_api.py              # Tester de API
│   └── requirements.txt
├── docker-compose.yml           # ⚠️ Docker Compose COMPLETO
├── test_system.py               # Test automático del sistema
└── quick_test.py                # Script de verificación rápida
```

## ⚠️ IMPORTANTE: Configuraciones Docker Compose

### Configuraciones disponibles:

#### 1. `Chapter-CI/my_first_ci_project/docker-compose.yml` (INDIVIDUAL)
- **Propósito**: Solo Django + MongoDB + Mongo Express
- **Uso**: Desarrollo del API Django independiente
- **Servicios**: `web`, `mongo`, `mongo-express`

#### 2. `Chapter-CI/docker-compose.dev.yml` (DESARROLLO)
- **Propósito**: Sistema completo con hot reload
- **Uso**: Desarrollo activo con cambios en tiempo real
- **Servicios**: `producer`, `consumer`, `mongo`, `mongo-express`

#### 3. `Chapter-CI/docker-compose.prod.yml` (PRODUCCIÓN)
- **Propósito**: Sistema completo standalone
- **Uso**: Distribución, cloud, testing final
- **Servicios**: `producer`, `consumer`, `mongo`, `mongo-express`

**🚨 NUNCA ejecutar múltiples configuraciones al mismo tiempo (conflicto de puertos)**

## 🎯 Flujos de Trabajo

### Para DESARROLLO del API Django:
```bash
cd Chapter-CI/my_first_ci_project
docker-compose up --build
# Luego probar con Postman en http://localhost:8000
```

### Para DESARROLLO del sistema completo (Hot Reload):
```bash
# Terminal 1: Levantar servicios en modo desarrollo
cd Chapter-CI  
docker-compose -f docker-compose.dev.yml up --build

# Terminal 2: Ver logs del consumer
docker-compose -f docker-compose.dev.yml logs -f consumer

# Terminal 3: Generar eventos
cd Chapter-CI/my_first_consumer
python test_api.py
```

### Para PRODUCCIÓN/DISTRIBUCIÓN:
```bash
cd Chapter-CI
docker-compose -f docker-compose.prod.yml up --build
```

### Para TESTING AUTOMÁTICO del sistema:
```bash
cd Chapter-CI
docker-compose -f docker-compose.dev.yml up -d  # segundo plano
python test_system.py  # test completo
```

## 🌐 Servicios y Puertos

| Servicio | Puerto | URL | Descripción |
|----------|--------|-----|-------------|
| Django API | 8000 | http://localhost:8000 | API REST para productos |
| WebSocket Server | 8765 | ws://localhost:8765 | Servidor WebSocket |
| MongoDB | 27017 | localhost:27017 | Base de datos |
| Mongo Express | 8081 | http://localhost:8081 | UI web para MongoDB |

## 📡 API Endpoints

### Productos
- `GET /api/` - Página principal
- `GET /api/products/` - Listar todos los productos
- `GET /api/product/<id>/` - Obtener producto por ID
- `POST /api/product/` - Crear nuevo producto

### Ejemplo crear producto:
```bash
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Camiseta", "precio": 25.99, "talla": "M"}'
```

## 🔌 WebSocket

### Conexión
```javascript
const ws = new WebSocket('ws://localhost:8765');
```

### Tipos de mensajes

#### Del servidor al cliente:
- `connection_established` - Confirmación de conexión
- `product_created` - Nuevo producto creado
- `pong` - Respuesta a ping
- `status` - Estado del servidor
- `error` - Errores del servidor

#### Del cliente al servidor:
- `ping` - Verificar conexión
- `get_status` - Solicitar estado del servidor

## 🛠️ Comandos Docker

### Desarrollo (Hot Reload):
```bash
cd Chapter-CI
docker-compose -f docker-compose.dev.yml up --build     # Levantar con hot reload
docker-compose -f docker-compose.dev.yml up -d          # En segundo plano
docker-compose -f docker-compose.dev.yml logs -f        # Ver logs
docker-compose -f docker-compose.dev.yml exec producer bash  # Acceder al container
docker-compose -f docker-compose.dev.yml down           # Parar servicios
```

### Producción (Standalone):
```bash
cd Chapter-CI
docker-compose -f docker-compose.prod.yml up --build    # Levantar modo producción
docker-compose -f docker-compose.prod.yml up -d         # En segundo plano
docker-compose -f docker-compose.prod.yml logs -f       # Ver logs
docker-compose -f docker-compose.prod.yml down          # Parar servicios
```

### Solo Django (individual):
```bash
cd Chapter-CI/my_first_ci_project
docker-compose up --build              # Solo Django + MongoDB
docker-compose exec web bash           # Acceder al container
```

### Comandos Django en containers:
```bash
# Para desarrollo:
docker-compose -f docker-compose.dev.yml exec producer python manage.py migrate
docker-compose -f docker-compose.dev.yml exec producer python manage.py test
docker-compose -f docker-compose.dev.yml exec producer python manage.py createsuperuser

# Para producción:
docker-compose -f docker-compose.prod.yml exec producer python manage.py migrate
docker-compose -f docker-compose.prod.yml exec producer python manage.py test

# Para individual:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py test
```

## 🧪 Testing

### Test manual del sistema:
1. Levantar servicios: `cd Chapter-CI && docker-compose up`
2. En otra terminal: `cd my_first_consumer && python websocket_client.py`
3. En otra terminal: `cd my_first_consumer && python test_api.py`
4. Usar comando `auto` en el tester para crear productos
5. Ver notificaciones en tiempo real en el consumidor

### Test automático:
```bash
cd Chapter-CI
docker-compose up -d
python test_system.py
```

### Verificación rápida (si hay problemas):
```bash
cd Chapter-CI
python quick_test.py
```

## 📚 Tecnologías Utilizadas

- **Backend**: Django 5.2.4, Django REST Framework
- **Database**: MongoDB with MongoEngine
- **WebSocket**: websockets library
- **Containerization**: Docker & Docker Compose
- **Client**: Python asyncio, colorama

## 🔄 Flujo de Datos

1. **Cliente** (Postman) → **POST** `/api/product/` → **Django API**
2. **Django** guarda producto en **MongoDB**
3. **Django** se conecta como **cliente WebSocket** → `ws://localhost:8765`
4. **Django** envía mensaje al **WebSocket Server**
5. **WebSocket Server** hace **broadcast** → **Todos los clientes conectados**
6. **Consumer** recibe notificación → **Muestra en consola en tiempo real**

### Detalles técnicos:
- Django usa `websockets.connect()` para enviar notificaciones
- WebSocket Server usa `websockets.serve()` para recibir y retransmitir
- Threading evita bloquear Django durante las notificaciones

## 📝 Historia de Comandos

Para ver el historial completo de comandos disponibles, consulta el archivo `cmds.txt`.

## 🤝 Contribución

Este es un proyecto educativo del Chapter-CI. Para agregar funcionalidades:

1. Fork del proyecto
2. Crear branch para feature
3. Hacer cambios
4. Testear con `python test_system.py`
5. Crear Pull Request

## 🐛 Debugging y Troubleshooting

### Ver notificaciones WebSocket:
```bash
# Opción 1: Ver logs del consumer
docker-compose logs -f consumer

# Opción 2: Ejecutar consumer localmente
cd my_first_consumer && python websocket_client.py

# Opción 3: Ver logs de ambos servicios
docker-compose logs -f producer consumer
```

### Verificar que WebSocket server está corriendo:
```bash
docker-compose exec producer ps aux | grep websocket
docker-compose exec producer netstat -tuln | grep 8765
```

### Problemas comunes:

#### "Connection failed [Errno 111]"
- **Normal** al inicio: WebSocket server tarda 2-3 segundos en arrancar
- El consumer se reconecta automáticamente
- Espera a ver: `✅ Connected to WebSocket server!`

#### "No veo notificaciones WebSocket"
```bash
# 1. Verificar logs del producer al hacer POST
docker-compose logs producer | tail -10

# 2. Debería mostrar:
# "✅ WebSocket notification sent: ProductName"
# "📦 Broadcasting product created: {...}"

# 3. Si no aparece, reiniciar:
docker-compose down && docker-compose up --build
```

#### "Consumer no se conecta"
```bash
# Verificar que todos los servicios están UP
docker-compose ps

# Verificar logs del consumer
docker-compose logs consumer
```

### Test paso a paso:
1. `docker-compose -f docker-compose.dev.yml up` → Ver que todos los servicios arranquen
2. Esperar: `✅ Connected to WebSocket server!` en consumer
3. POST en Postman → Verificar 201 response
4. Ver notificación en tiempo real en consumer logs

## 🔄 Desarrollo vs Producción

### 📊 Comparación de Configuraciones

| Característica | Desarrollo (`dev.yml`) | Producción (`prod.yml`) |
|---------------|------------------------|-------------------------|
| **Código** | Volume mount desde host | Embebido en imagen |
| **Hot Reload** | ✅ Activado (DEBUG=1) | ❌ Desactivado (DEBUG=0) |
| **Cambios** | Inmediatos sin rebuild | Requiere rebuild |
| **Tamaño** | Imagen pequeña + código externo | Imagen completa |
| **Exportable** | ❌ Depende de archivos locales | ✅ Standalone |
| **Velocidad** | Inicio rápido | Inicio normal |
| **Uso** | Desarrollo local | Cloud, distribución, CI/CD |

### 🔍 Diferencias Técnicas

#### **Desarrollo:**
```yaml
volumes:
  - ./my_first_ci_project:/app  # ← Código desde tu máquina
environment:
  - DEBUG=1                     # ← Auto-reload activado
```

**Flujo:**
```
Tu código local ──mount──► Container ──hot reload──► Cambios inmediatos
```

#### **Producción:**
```yaml
# NO volumes: Código embebido durante build
environment:
  - DEBUG=0                     # ← Sin auto-reload
```

**Flujo:**
```
Build: Código ──COPY──► Imagen Docker ──deploy──► Container independiente
```

### 🚀 Cuándo usar cada uno

#### **Desarrollo (`docker-compose.dev.yml`):**
- ✅ Desarrollo activo
- ✅ Testing de cambios rápidos
- ✅ Debugging
- ✅ Prototipado
- ❌ Distribución
- ❌ Producción

#### **Producción (`docker-compose.prod.yml`):**
- ✅ Deploy en cloud (AWS, GCP, Azure)
- ✅ CI/CD pipelines
- ✅ Distribución de aplicación
- ✅ Testing final
- ✅ Contenedores portables
- ❌ Desarrollo con cambios frecuentes

### 🛠️ Script Helper

Usa el script incluido para alternar fácilmente:

```bash
# Ver ayuda
./build_and_test.sh help

# Modo desarrollo
./build_and_test.sh dev

# Modo producción  
./build_and_test.sh prod

# Exportar para distribución
./build_and_test.sh export
```

### 🏭 Despliegue en Cloud

Para deployar en la nube:

1. **Construir imagen de producción:**
```bash
docker-compose -f docker-compose.prod.yml build
```

2. **Exportar imagen:**
```bash
docker save -o my-app.tar chapter-ci-producer
```

3. **En el servidor/cloud:**
```bash
docker load -i my-app.tar
docker-compose -f docker-compose.prod.yml up -d
```

**¡La imagen de producción es completamente independiente del código local!** 🎉

## 📄 Licencia

Ver archivo `LICENSE` en la raíz del proyecto. 