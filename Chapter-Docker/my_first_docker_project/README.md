# 🏭 My First CI Project

Un proyecto Django con **API REST** para gestión de productos, que incluye configuraciones para **desarrollo** y **producción**.

## 🎯 **Características**

- **API REST**: CRUD completo de productos
- **🕷️ Web Scraping**: Integración con MercadoLibre
- **💰 Price Comparison**: Comparación automática de precios
- **📊 Cache**: Optimización con Django cache
- **MongoDB**: Base de datos NoSQL
- **WebSocket**: Notificaciones en tiempo real (solo DEV)
- **Docker**: Containerización completa
- **Hot Reload**: Desarrollo ágil (solo DEV)
- **Dual Mode**: Configuraciones DEV y PROD

## 🚀 **Quick Start**

### **🔥 Modo Desarrollo (CON Hot Reload)**
```bash
cd Chapter-CI/my_first_docker_project
docker-compose -f docker-compose.dev.yml up --build
```

### **🏭 Modo Producción (SIN Hot Reload)**
```bash
cd Chapter-CI/my_first_docker_project
docker-compose -f docker-compose.prod.yml up --build -d
```

## 📋 **API Endpoints**

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| **GET** | `/admin/` | Página principal |
| **POST** | `/api/product/` | Crear producto |
| **GET** | `/api/product/{id}/` | Obtener producto |
| **GET** | `/api/products/` | Listar productos |
| **GET** | `/api/search/mercadolibre/?q={term}` | 🕷️ Buscar en MercadoLibre |
| **POST** | `/api/compare/prices/` | 🕷️ Comparar precios |
| **GET** | `/api/scrape/details/?url={url}` | 🕷️ Detalles de ML |

### **Ejemplo de uso:**
```bash
# Crear producto
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "iPhone 15", "precio": 999.99, "talla": "L"}'

# Listar productos
curl http://localhost:8000/api/products/

# 🕷️ Buscar productos en MercadoLibre
curl "http://localhost:8000/api/search/mercadolibre/?q=iPhone&limit=3"

# 🕷️ Comparar precios (usar ID de producto creado)
curl -X POST http://localhost:8000/api/compare/prices/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": "PRODUCT_ID_HERE"}'
```

## 🕷️ **Web Scraping Features**

### **🔍 Búsqueda en MercadoLibre**
Busca productos directamente en MercadoLibre México:
```bash
curl "http://localhost:8000/api/search/mercadolibre/?q=laptop&limit=5"
```

**Respuesta ejemplo:**
```json
{
  "query": "laptop",
  "results_count": 5,
  "products": [
    {
      "title": "Laptop Gamer Asus ROG Strix G15",
      "price": 25999.0,
      "url": "https://mercadolibre.com.mx/...",
      "free_shipping": true,
      "location": "Distrito Federal",
      "source": "MercadoLibre"
    }
  ]
}
```

### **💰 Comparación de Precios**
Compara productos locales con MercadoLibre:
```bash
# 1. Crear producto local
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "iPhone 15", "precio": 22000, "talla": "128GB"}'

# 2. Comparar precios (usar ID retornado)
curl -X POST http://localhost:8000/api/compare/prices/ \
  -H "Content-Type: application/json" \
  -d '{"product_id": "67e8a4b..."}'
```

**Análisis de respuesta:**
```json
{
  "local_product": {
    "id": "67e8a4b...",
    "name": "iPhone 15",
    "price": 22000.0
  },
  "mercadolibre_results": [...],
  "price_analysis": {
    "our_price": 22000.0,
    "lowest_ml_price": 19999.0,
    "price_difference": 2001.0,
    "is_competitive": false
  }
}
```

### **📊 Cache Inteligente**
- ✅ **Búsquedas**: Cache por 30 minutos
- ✅ **Detalles**: Cache por 10 minutos  
- ✅ **Productos**: Cache por 1 hora
- ✅ **Rate Limiting**: Evita spam a MercadoLibre

## 🔥 **DESARROLLO vs 🏭 PRODUCCIÓN**

| Aspecto | DEV | PROD |
|---------|-----|------|
| **Hot Reload** | ✅ Automático | ❌ Necesita rebuild |
| **WebSocket** | ✅ Habilitado | ❌ Deshabilitado |
| **Servidor** | Django runserver | Gunicorn |
| **Debug** | ✅ Completo | ❌ Mínimo |
| **Volúmenes** | ✅ Montados | ❌ Sin volúmenes |
| **Recursos** | Más uso | Optimizado |

## 🛠️ **Comandos Principales**

### **Desarrollo (DEV):**
```bash
# Iniciar servicios
docker-compose -f docker-compose.dev.yml up --build

# Ver logs en tiempo real
docker-compose -f docker-compose.dev.yml logs -f

# Parar servicios
docker-compose -f docker-compose.dev.yml down

# Restart específico
docker-compose -f docker-compose.dev.yml restart producer
```

### **Producción (PROD):**
```bash
# Deploy en background
docker-compose -f docker-compose.prod.yml up --build -d

# Ver estado
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs producer

# Parar todo
docker-compose -f docker-compose.prod.yml down
```

## 🏗️ **Servicios Incluidos**

### **🔥 DEV - Desarrollo Completo**
- **Producer**: Django API (puerto 8000) + Hot Reload
- **WebSocket Service**: Notificaciones tiempo real (puerto 8765)
- **Consumer**: Cliente WebSocket de prueba
- **MongoDB**: Base de datos (puerto 27017)

### **🏭 PROD - Solo Esencial**
- **Producer**: Django API (puerto 8000) optimizada
- **MongoDB**: Base de datos (puerto 27017)

## 🔧 **Variables de Entorno**

| Variable | DEV | PROD | Descripción |
|----------|-----|------|-------------|
| `DEBUG` | `1` | `0` | Modo debug |
| `WEBSOCKET_ENABLED` | `true` | `false` | WebSocket notifications |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | `yourdomain.com` | Hosts permitidos |
| `WEBSOCKET_URL` | `ws://websocket-service:8765` | - | URL WebSocket |

## 📊 **Base de Datos**

### **MongoDB Connection:**
- **Host**: `localhost:27017`
- **Database**: `my_first_ci_db`
- **Collection**: `product`
- **User**: `admin`
- **Password**: `password`

### **Acceso directo:**
```bash
# Conectar a MongoDB
mongo mongodb://admin:password@localhost:27017/my_first_ci_db

# Desde container
docker exec -it <mongo_container> mongo -u admin -p password my_first_ci_db
```

## 🧪 **Testing**

### **Test básico del API:**
```bash
# Health check
curl http://localhost:8000/admin/

# Crear producto
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "MacBook Pro", "precio": 2499.99, "talla": "L"}'

# Verificar creación
curl http://localhost:8000/api/products/
```

### **Test múltiples productos:**
```bash
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/product/ \
    -H "Content-Type: application/json" \
    -d "{\"nombre\": \"Product $i\", \"precio\": $(($i * 100)).99, \"talla\": \"M\"}"
  sleep 1
done
```

### **🕷️ Test Web Scraping:**
```bash
# Test búsqueda MercadoLibre
curl "http://localhost:8000/api/search/mercadolibre/?q=iPhone&limit=3"

# Test comparación de precios
PRODUCT_ID=$(curl -s -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "iPhone 15", "precio": 25000, "talla": "128GB"}' | jq -r '.id')

curl -X POST http://localhost:8000/api/compare/prices/ \
  -H "Content-Type: application/json" \
  -d "{\"product_id\": \"$PRODUCT_ID\"}"

# Test detalles específicos (necesitas una URL real de ML)
curl "http://localhost:8000/api/scrape/details/?url=https://articulo.mercadolibre.com.mx/MLM-..."
```

## 🔍 **Debugging**

### **Ver logs detallados:**
```bash
# Logs de todos los servicios (DEV)
docker-compose -f docker-compose.dev.yml logs --tail 50

# Logs específicos
docker-compose -f docker-compose.dev.yml logs producer
docker-compose -f docker-compose.dev.yml logs websocket-service

# Logs en tiempo real
docker-compose -f docker-compose.dev.yml logs -f
```

### **Entrar a containers:**
```bash
# Entrar al Producer
docker-compose -f docker-compose.dev.yml exec producer bash

# Entrar a MongoDB
docker-compose -f docker-compose.dev.yml exec mongo mongo -u admin -p password
```

## 🚀 **Flujo de Trabajo Recomendado**

### **1. Desarrollo diario:**
```bash
# Usar DEV para editar código
docker-compose -f docker-compose.dev.yml up --build

# Editar archivos → Cambios automáticos ✨
# WebSocket funcionando para notificaciones
```

### **2. Testing pre-deploy:**
```bash
# Probar configuración de producción
docker-compose -f docker-compose.prod.yml up --build

# Verificar que funciona sin hot reload
# Solo API REST sin WebSocket
```

### **3. Deploy producción:**
```bash
# En servidor final
docker-compose -f docker-compose.prod.yml up --build -d
```

## 📁 **Estructura del Proyecto**

```
my_first_docker_project/
├── api/                           # 📂 Django app
│   ├── models.py                  # 🗃️ Modelo Product
│   ├── views.py                   # 🎯 API endpoints + WebSocket
│   └── urls.py                    # 🛣️ URL routing
├── my_first_docker_project/           # 📂 Django project
│   ├── settings.py                # ⚙️ Configuración
│   └── urls.py                    # 🛣️ URLs principales
├── docker-compose.dev.yml         # 🔥 Configuración DEV
├── docker-compose.prod.yml        # 🏭 Configuración PROD
├── Dockerfile                     # 🐳 Imagen Docker
├── requirements.txt               # 📦 Dependencias Python
├── DEPLOYMENT_GUIDE.md            # 📚 Guía detallada
└── README.md                      # 📖 Este archivo
```

## ⚡ **Hot Reload en Acción**

En **modo DEV**, cuando edites:
- `api/views.py` → Cambios instantáneos en API
- `templates/` → Frontend se actualiza
- `models.py` → Cambios en base de datos
- `requirements.txt` → Necesitas rebuild

## 🔒 **Seguridad**

### **Producción:**
- Debug deshabilitado
- ALLOWED_HOSTS configurados
- Sin volúmenes expuestos
- Gunicorn como servidor

### **Desarrollo:**
- Debug habilitado para troubleshooting
- Hosts permisivos para testing
- Volúmenes para hot reload

## 🎯 **Próximos Pasos**

1. **CI/CD**: Automatizar deploy con GitHub Actions
2. **Load Balancer**: Nginx como reverse proxy
3. **Monitoring**: Prometheus + Grafana
4. **Cache**: Redis para performance
5. **Auth**: Sistema de autenticación

---

## 📖 **Documentación Adicional**

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**: Guía detallada DEV vs PROD
- **[Microservices Architecture](../microservices_architecture/)**: WebSocket service independiente

---

**¡Feliz coding! 🚀** 