# 📡 WebSocket Service - Microservices Architecture

Servicio WebSocket **independiente** que recibe notificaciones del **my_first_ci_project** y las distribuye a múltiples clientes en tiempo real.

## 🏗️ Arquitectura

```
┌─────────────────┐    WebSocket ┌─────────────────┐    WebSocket    ┌─────────────────┐
│ my_first_ci_    │ ──────────► │   WebSocket     │ ──────────────► │   Clients       │
│ project         │ notifications│   Service       │  broadcasting   │   (consumers)   │
│ (Django API)    │             │ (:8765)         │                 │                 │
│ ┌─────────────┐ │             │ ┌─────────────┐ │                 │ ┌─────────────┐ │
│ │REST API     │ │             │ │Broadcasting │ │                 │ │Multiple     │ │
│ │MongoDB      │ │             │ │Multi-Client │ │                 │ │WebSocket    │ │
│ │Product CRUD │ │             │ │Live Updates │ │                 │ │Clients      │ │
│ └─────────────┘ │             │ └─────────────┘ │                 │ └─────────────┘ │
│                 │             │                 │                 │                 │
│ ✓ Hot Reload    │             │ ✓ Broadcasting  │                 │ ✓ Real-time     │
│ ✓ DEV/PROD Mode │             │ ✓ Multi-Client  │                 │ ✓ Auto-Reconnect│
└─────────────────┘             └─────────────────┘                 └─────────────────┘
```

## 🚀 Quick Start

### **Sistema Completo en UN solo comando**
```bash
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml up --build
```

> ✅ **Incluye**: Producer + WebSocket Service + Consumer + MongoDB - Todo en uno

### **Alternativa: Solo my_first_ci_project (sin microservices)**
```bash
cd Chapter-CI/my_first_ci_project
docker-compose -f docker-compose.dev.yml up --build
```

> ⚠️ **No uses ambos a la vez** - Conflictan en puerto 8000

### **Test del sistema:**
```bash
# Con microservices_architecture ejecutándose, crear producto:
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "iPhone 15", "precio": 999.99, "talla": "L"}'

# Deberías ver logs en:
# - Producer: ✅ Notified WebSocket service
# - WebSocket Service: 📦 Product notification received  
# - Consumer: 📱 Product created: iPhone 15
```

## 📋 Servicios Incluidos

### **📡 WebSocket Service (Principal)**
- **Puerto**: 8765  
- **Función**: Broadcasting de notificaciones en tiempo real
- **Stack**: Python + WebSockets (sin frameworks adicionales)
- **Health**: `ws://localhost:8765`
- **Hot Reload**: ✅ Disponible en modo desarrollo

### **🏭 Producer (External - my_first_ci_project)**
- **Puerto**: 8000 (en proyecto separado)
- **Función**: API REST que envía notificaciones al WebSocket Service
- **Ubicación**: `../my_first_ci_project/`
- **Conexión**: Se conecta a `ws://websocket-service:8765`

### **🔔 Consumer (Cliente de Prueba)**
- **Función**: Cliente WebSocket para testing
- **Stack**: Python WebSocket Client
- **Output**: Logs de notificaciones en tiempo real

### **💾 MongoDB (External)**
- **Ubicación**: En `my_first_ci_project`
- **Función**: Base de datos para productos
- **Acceso**: Puerto 27017 desde el producer

## 🛑 Cómo Apagar los Servicios

### **🔴 Parar todos los servicios (modo normal):**
```bash
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml down
```

### **🗑️ Parar y limpiar COMPLETAMENTE (recomendado):**
```bash
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml down --volumes --remove-orphans
```
- `--volumes`: Elimina volúmenes (datos de MongoDB se pierden)
- `--remove-orphans`: Elimina contenedores huérfanos

### **⚠️ Solo parar servicios (sin eliminar):**
```bash
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml stop
```

### **🎯 Parar servicios específicos:**
```bash
cd Chapter-CI/microservices_architecture

# Solo MongoDB  
docker-compose -f docker-compose.microservices.yml stop mongo

# Solo WebSocket Service
docker-compose -f docker-compose.microservices.yml stop websocket-service

# Solo Consumer
docker-compose -f docker-compose.microservices.yml stop consumer

# Solo Producer
docker-compose -f docker-compose.microservices.yml stop producer
```

### **📊 Verificar estado:**
```bash
# Ver contenedores activos
docker ps

# Ver estado de servicios del proyecto
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml ps
```

### **🔄 Reiniciar después de parar:**
```bash
cd Chapter-CI/microservices_architecture

# Reiniciar todos
docker-compose -f docker-compose.microservices.yml up -d

# Reiniciar solo algunos servicios
docker-compose -f docker-compose.microservices.yml up -d producer websocket-service
```

## 🛠️ Comandos de Desarrollo

### **🔥 Desarrollo con Hot Reload:**
```bash
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml up --build

# Hot Reload activo para websocket_server.py
# Editas código → Cambios automáticos ✨
```

### **🏭 Modo producción:**
```bash
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml up -d --build

# Para usar con my_first_ci_project en PROD:
# Terminal 1: WebSocket service
docker-compose -f docker-compose.microservices.yml up -d

# Terminal 2: Producer en modo PROD  
cd ../my_first_ci_project
docker-compose -f docker-compose.prod.yml up -d
```

### **Ver logs específicos:**
```bash
cd Chapter-CI/microservices_architecture

# Logs del Producer
docker-compose -f docker-compose.microservices.yml logs -f producer

# Logs del WebSocket Service
docker-compose -f docker-compose.microservices.yml logs -f websocket-service

# Logs del Consumer
docker-compose -f docker-compose.microservices.yml logs -f consumer
```

### **Reiniciar servicios específicos:**
```bash
cd Chapter-CI/microservices_architecture

# Reiniciar WebSocket service
docker-compose -f docker-compose.microservices.yml restart websocket-service

# Reiniciar todos
docker-compose -f docker-compose.microservices.yml restart
```

## 🚀 Comandos de Producción

### **Deploy en producción:**
```bash
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml up -d --build --force-recreate
```

### **Escalar servicios:**
```bash
cd Chapter-CI/microservices_architecture

# Escalar WebSocket service a 3 instancias
docker-compose -f docker-compose.microservices.yml up -d --scale websocket-service=3

# Escalar Consumer a 5 instancias  
docker-compose -f docker-compose.microservices.yml up -d --scale consumer=5
```

### **Verificar salud del sistema:**
```bash
cd Chapter-CI/microservices_architecture

# Status de containers
docker-compose -f docker-compose.microservices.yml ps

# Verificar API
curl -f http://localhost:8000/admin/ && echo "✅ Producer OK"

# Verificar MongoDB (desde container)
docker-compose -f docker-compose.microservices.yml exec mongo mongo --eval "db.adminCommand('ping')" && echo "✅ MongoDB OK"
```

## 🧪 Testing Completo

### **1. Test sistema completo:**
```bash
# Levantar TODO el sistema
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml up --build

# En otra terminal, crear producto
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "MacBook Pro", "precio": 2499.99, "talla": "L"}'

# Ver logs específicos si necesitas
docker-compose -f docker-compose.microservices.yml logs consumer
```

### **2. Test de múltiples productos:**
```bash
cd Chapter-CI/microservices_architecture

# Script de múltiples requests
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/product/ \
    -H "Content-Type: application/json" \
    -d "{\"nombre\": \"Product $i\", \"precio\": $(($i * 100)).99, \"talla\": \"M\"}"
  sleep 1
done
```

### **3. Test de conectividad WebSocket:**
```bash
# Verificar que el WebSocket service esté running
curl -i -N \
  -H "Connection: Upgrade" \
  -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Key: test" \
  -H "Sec-WebSocket-Version: 13" \
  http://localhost:8765/
```

## 🔧 Debugging

### **Ver logs detallados:**
```bash
cd Chapter-CI/microservices_architecture

# Logs de todos los servicios
docker-compose -f docker-compose.microservices.yml logs --tail 50

# Logs en tiempo real
docker-compose -f docker-compose.microservices.yml logs -f
```

### **Entrar a un container:**
```bash
cd Chapter-CI/microservices_architecture

# Entrar al Producer
docker-compose -f docker-compose.microservices.yml exec producer bash

# Entrar al WebSocket service
docker-compose -f docker-compose.microservices.yml exec websocket-service sh
```

### **Verificar conectividad entre services:**
```bash
cd Chapter-CI/microservices_architecture

# Test desde Producer al WebSocket service
docker-compose -f docker-compose.microservices.yml exec producer \
  curl -i websocket-service:8765

# Test desde Consumer al WebSocket service  
docker-compose -f docker-compose.microservices.yml exec consumer \
  ping websocket-service
```

## 🛠️ Troubleshooting

### **Puerto ocupado:**
```bash
# Verificar qué está usando los puertos
sudo lsof -i :8000
sudo lsof -i :8765

# Matar procesos
sudo kill -9 <PID>
```

### **Problema con containers:**
```bash
cd Chapter-CI/microservices_architecture

# Parar y limpiar todo
docker-compose -f docker-compose.microservices.yml down --volumes --remove-orphans

# Rebuild sin cache
docker-compose -f docker-compose.microservices.yml build --no-cache

# Restart completo
docker-compose -f docker-compose.microservices.yml up --build --force-recreate
```

### **WebSocket connection issues:**
```bash
cd Chapter-CI/microservices_architecture

# Verificar logs del WebSocket service
docker-compose -f docker-compose.microservices.yml logs websocket-service --tail 20

# Reiniciar solo el WebSocket service
docker-compose -f docker-compose.microservices.yml restart websocket-service

# Verificar networking
docker-compose -f docker-compose.microservices.yml exec producer \
  nc -zv websocket-service 8765
```

### **MongoDB connection issues:**
```bash
cd Chapter-CI/microservices_architecture

# Verificar MongoDB logs
docker-compose -f docker-compose.microservices.yml logs mongo --tail 20

# Test de conexión desde Producer
docker-compose -f docker-compose.microservices.yml exec producer \
  python manage.py shell -c "from pymongo import MongoClient; print(MongoClient('mongo', 27017).admin.command('ping'))"
```

## 📊 Escalamiento y Performance

### **Escalar horizontalmente:**
```bash
cd Chapter-CI/microservices_architecture

# Load balancer setup (ejemplo con múltiples WebSocket services)
docker-compose -f docker-compose.microservices.yml up -d --scale websocket-service=3

# Múltiples consumers
docker-compose -f docker-compose.microservices.yml up -d --scale consumer=5
```

### **Monitoring básico:**
```bash
cd Chapter-CI/microservices_architecture

# Resource usage
docker stats $(docker-compose -f docker-compose.microservices.yml ps -q)

# Container health
docker-compose -f docker-compose.microservices.yml ps
```

## 🔒 Seguridad y Producción

### **Variables de entorno para producción:**
```bash
# Crear archivo .env
cd Chapter-CI/microservices_architecture
cat > .env << EOF
MONGO_PASSWORD=super_secure_password
DEBUG=0
ALLOWED_HOSTS=yourdomain.com,localhost
EOF
```

### **HTTPS y SSL (para producción):**
```bash
# Añadir certificados SSL
mkdir -p ssl/
# Copiar certificados a ssl/

# Actualizar docker-compose con volumen SSL
# volumes:
#   - ./ssl:/app/ssl
```

## 📁 Estructura del Proyecto

```
microservices_architecture/
├── docker-compose.microservices.yml    # 🐳 Compose para orquestar servicios
├── websocket-service/
│   ├── websocket_server.py             # 📡 WebSocket server + Hot Reload
│   └── Dockerfile                      # 🐳 Container optimizado
└── README.md                           # 📚 Esta documentación

../my_first_ci_project/                  # 🏭 Producer (proyecto separado)
├── docker-compose.dev.yml              # 🔥 DEV: con WebSocket + Hot Reload
├── docker-compose.prod.yml             # 🏭 PROD: solo REST API
├── api/views.py                        # 🏭 Notifica a websocket-service
└── README.md                           # 📚 Documentación completa
```

## 🎯 Arquitectura y Beneficios

### **🔧 Patrón de Diseño:**
- **WebSocket Service**: Servicio dedicado exclusivamente a notificaciones tiempo real
- **Producer External**: `my_first_ci_project` como productor de eventos
- **Hot Reload**: Desarrollo ágil en ambos servicios
- **Environment Separation**: DEV (con WebSocket) vs PROD (sin WebSocket)

### **✅ Ventajas:**
- **Separación de responsabilidades**: WebSocket service independiente
- **Escalabilidad**: WebSocket service se escala por separado
- **Desarrollo ágil**: Hot reload en WebSocket server
- **Flexibilidad**: Producer puede ser DEV o PROD
- **Broadcasting**: Múltiples clientes pueden conectarse

### **⚠️ Consideraciones:**
- **Coordinación**: Necesitas levantar ambos proyectos para testing completo
- **Networking**: Comunicación entre containers
- **Dependencies**: Producer depende del WebSocket service para notificaciones

## 🚀 Integración con my_first_ci_project

### **🔥 Modo Desarrollo:**
```bash
# Sistema completo con hot reload
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml up --build

# Resultado: Producer + WebSocket + Consumer + MongoDB
# ✨ Hot reload activo en Producer y WebSocket Service
```

### **🏭 Modo Producción:**
```bash
# Paso 1: WebSocket Service
cd Chapter-CI/microservices_architecture
docker-compose -f docker-compose.microservices.yml up -d

# Paso 2: Producer en PROD mode (sin WebSocket)
cd Chapter-CI/my_first_ci_project
docker-compose -f docker-compose.prod.yml up -d

# Resultado: Solo REST API, sin notificaciones tiempo real
```

---

## 📖 **Documentación Relacionada**

- **[my_first_ci_project README](../my_first_ci_project/README.md)**: Documentación completa del producer
- **[DEPLOYMENT_GUIDE](../my_first_ci_project/DEPLOYMENT_GUIDE.md)**: Guía detallada DEV vs PROD

---

## 🎯 **Próximos Pasos**

1. **Load Balancer**: Nginx para WebSocket service
2. **Message Queue**: Redis/RabbitMQ para robustez
3. **Monitoring**: Logs centralizados
4. **Health Checks**: Endpoints de salud
5. **SSL/TLS**: Certificados para producción

---

**¡WebSocket Service listo para broadcasting! 📡✨** 