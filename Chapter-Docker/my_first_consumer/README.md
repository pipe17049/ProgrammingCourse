# My First Consumer

WebSocket client que consume mensajes en tiempo real del proyecto `my_first_docker_project`.

## ¿Qué hace?

- Se conecta al servidor WebSocket del proyecto Django
- Escucha notificaciones en tiempo real cuando se crean productos
- Muestra información colorizada en la consola
- Se reconecta automáticamente si pierde la conexión

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
cp .env.example .env
```

## Uso

### 1. Escuchar WebSocket (modo básico)
```bash
python websocket_client.py
```

### 2. Probar API y generar eventos
```bash
python test_api.py
```

## Variables de entorno

- `WEBSOCKET_URL`: URL del servidor WebSocket (default: `ws://localhost:8765`)
- `API_URL`: URL de la API REST (default: `http://localhost:8000/api`)

## Funcionalidades

### WebSocket Client
- ✅ Conexión automática con reconexión
- ✅ Manejo de diferentes tipos de mensajes
- ✅ Logging colorizado con timestamps
- ✅ Modo interactivo para enviar comandos

### API Tester
- ✅ Crear productos via REST API
- ✅ Listar productos existentes
- ✅ Modo auto para crear productos de prueba
- ✅ Modo interactivo

## Tipos de mensajes WebSocket

- `connection_established` - Confirmación de conexión
- `product_created` - Nuevo producto creado
- `pong` - Respuesta a ping
- `status` - Estado del servidor
- `error` - Errores del servidor

## Comandos del tester de API

- `create` - Crear producto manualmente
- `list` - Listar todos los productos
- `auto` - Crear productos de prueba automáticamente
- `quit` - Salir 