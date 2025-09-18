# 🚀 Deployment Guide - DEV vs PROD

Este proyecto tiene **dos configuraciones** para diferentes entornos:

## 🔥 **DESARROLLO (DEV) - Con Hot Reload**

### **Características:**
- ✅ **Hot Reload**: Cambios en código se reflejan automáticamente
- ✅ **WebSocket**: Notificaciones en tiempo real habilitadas  
- ✅ **Debug**: Logs detallados y error pages
- ✅ **Live Development**: No necesitas rebuilds

### **Comando:**
```bash
cd Chapter-CI/my_first_docker_project
docker-compose -f docker-compose.dev.yml up --build
```

### **¿Qué incluye?**
- **Django**: Puerto 8000 con `runserver` (hot reload)
- **WebSocket Service**: Puerto 8765 con hot reload
- **Consumer**: Cliente de prueba
- **MongoDB**: Base de datos local

### **💡 Ventajas DEV:**
- Editas código → Cambios instantáneos
- No necesitas parar/reiniciar containers
- Logs en tiempo real
- WebSocket notifications funcionando

---

## 🏭 **PRODUCCIÓN (PROD) - Optimizada**

### **Características:**
- ❌ **Sin Hot Reload**: Código empaquetado en imagen
- ❌ **Sin WebSocket**: Solo REST API
- ✅ **Gunicorn**: Servidor de producción
- ✅ **Optimizada**: Menor uso de recursos

### **Comando:**
```bash
cd Chapter-CI/my_first_docker_project
docker-compose -f docker-compose.prod.yml up --build -d
```

### **¿Qué incluye?**
- **Django**: Puerto 8000 con `gunicorn` (producción)
- **MongoDB**: Base de datos

### **💡 Ventajas PROD:**
- Menor uso de memoria y CPU
- Sin volúmenes montados
- Configuración de producción
- Sin dependencias de desarrollo

---

## 🛠️ **Comandos Útiles**

### **Desarrollo:**
```bash
# Iniciar en modo desarrollo
docker-compose -f docker-compose.dev.yml up --build

# Ver logs en tiempo real
docker-compose -f docker-compose.dev.yml logs -f

# Parar servicios
docker-compose -f docker-compose.dev.yml down

# Test API
curl -X POST http://localhost:8000/api/product/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "iPhone 15", "precio": 999.99, "talla": "L"}'
```

### **Producción:**
```bash
# Deploy en producción
docker-compose -f docker-compose.prod.yml up --build -d

# Ver estado
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs

# Parar servicios
docker-compose -f docker-compose.prod.yml down
```

---

## 🔧 **Variables de Entorno**

| Variable | DEV | PROD | Descripción |
|----------|-----|------|-------------|
| `DEBUG` | `1` | `0` | Modo debug Django |
| `WEBSOCKET_ENABLED` | `true` | `false` | Notificaciones WebSocket |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | `yourdomain.com` | Hosts permitidos |

---

## 🚀 **Flujo de Trabajo Recomendado**

### **1. Desarrollo Local:**
```bash
# Usar DEV para desarrollo diario
docker-compose -f docker-compose.dev.yml up --build

# Editar código → Cambios automáticos
# Test con WebSocket funcionando
```

### **2. Testing Pre-Producción:**
```bash
# Probar en modo PROD antes del deploy
docker-compose -f docker-compose.prod.yml up --build

# Verificar que funciona sin hot reload
# Test solo REST API
```

### **3. Deploy Producción:**
```bash
# En servidor de producción
docker-compose -f docker-compose.prod.yml up --build -d
```

---

## 📋 **Diferencias Técnicas**

| Aspecto | DEV | PROD |
|---------|-----|------|
| **Servidor** | `runserver` | `gunicorn` |
| **Volúmenes** | ✅ Montados | ❌ Sin volúmenes |
| **WebSocket** | ✅ Habilitado | ❌ Deshabilitado |
| **Hot Reload** | ✅ Activo | ❌ Inactivo |
| **Recursos** | Más uso | Optimizado |
| **Debug** | ✅ Completo | ❌ Mínimo |

¡Perfecto para desarrollo ágil y deploy seguro! 🎉 