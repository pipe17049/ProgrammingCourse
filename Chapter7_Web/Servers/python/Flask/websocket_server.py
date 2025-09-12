#!/usr/bin/env python3
"""
Servidor WebSocket para manejo de notificaciones en tiempo real
Recibe y distribuye mensajes a todos los clientes conectados
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Conjunto de conexiones activas
connected_clients = set()

async def register_client(websocket):
    """Registra un nuevo cliente WebSocket"""
    connected_clients.add(websocket)
    logger.info(f"🔗 Nuevo cliente conectado. Total: {len(connected_clients)}")
    
    # Mensaje de bienvenida
    welcome_message = {
        "type": "connection",
        "message": "Conectado al servidor de notificaciones",
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "client_count": len(connected_clients)
    }
    await websocket.send(json.dumps(welcome_message))

async def unregister_client(websocket):
    """Desregistra un cliente WebSocket"""
    connected_clients.discard(websocket)
    logger.info(f"❌ Cliente desconectado. Total: {len(connected_clients)}")

async def broadcast_message(message):
    """Envía un mensaje a todos los clientes conectados"""
    if not connected_clients:
        logger.warning("📢 No hay clientes conectados para enviar mensaje")
        return
    
    # Enviar a todos los clientes conectados
    disconnected_clients = []
    
    for websocket in connected_clients.copy():
        try:
            await websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosed:
            disconnected_clients.append(websocket)
        except Exception as e:
            logger.error(f"Error enviando mensaje a cliente: {e}")
            disconnected_clients.append(websocket)
    
    # Limpiar clientes desconectados
    for websocket in disconnected_clients:
        await unregister_client(websocket)
    
    logger.info(f"📨 Mensaje enviado a {len(connected_clients)} clientes")

async def handle_websocket_connection(websocket, path):
    """Maneja conexiones WebSocket individuales"""
    await register_client(websocket)
    
    try:
        # Escuchar mensajes del cliente
        async for message in websocket:
            try:
                # Parsear mensaje JSON
                data = json.loads(message)
                logger.info(f"📥 Mensaje recibido: {data}")
                
                # Procesar diferentes tipos de mensajes
                if data.get("type") == "task_created":
                    # Mensaje de nueva tarea creada
                    notification = {
                        "type": "task_notification", 
                        "action": "created",
                        "task": data.get("task", {}),
                        "message": f"✅ Nueva tarea creada: {data.get('task', {}).get('title', 'Sin título')}",
                        "timestamp": datetime.utcnow().isoformat() + 'Z'
                    }
                    await broadcast_message(notification)
                
                elif data.get("type") == "task_updated":
                    # Mensaje de tarea actualizada
                    notification = {
                        "type": "task_notification",
                        "action": "updated", 
                        "task": data.get("task", {}),
                        "message": f"🔄 Tarea actualizada: {data.get('task', {}).get('title', 'Sin título')}",
                        "timestamp": datetime.utcnow().isoformat() + 'Z'
                    }
                    await broadcast_message(notification)
                
                elif data.get("type") == "task_deleted":
                    # Mensaje de tarea eliminada
                    notification = {
                        "type": "task_notification",
                        "action": "deleted",
                        "task": data.get("task", {}), 
                        "message": f"🗑️ Tarea eliminada: {data.get('task', {}).get('title', 'Sin título')}",
                        "timestamp": datetime.utcnow().isoformat() + 'Z'
                    }
                    await broadcast_message(notification)
                    
                else:
                    # Mensaje genérico
                    logger.info(f"Mensaje genérico recibido: {data}")
                    
            except json.JSONDecodeError:
                logger.error("❌ Error: Mensaje no es JSON válido")
            except Exception as e:
                logger.error(f"❌ Error procesando mensaje: {e}")
    
    except websockets.exceptions.ConnectionClosed:
        logger.info("🔌 Conexión cerrada por el cliente")
    except Exception as e:
        logger.error(f"❌ Error en conexión WebSocket: {e}")
    finally:
        await unregister_client(websocket)

async def main():
    """Función principal para iniciar el servidor WebSocket"""
    # Configuración del servidor
    host = "localhost"
    port = 8765
    
    logger.info("🚀 Iniciando servidor WebSocket...")
    logger.info(f"📍 Servidor ejecutándose en ws://{host}:{port}")
    logger.info("💡 Para probar: wscat -c ws://localhost:8765")
    logger.info("⏹️  Para detener: Ctrl+C")
    
    # Iniciar servidor WebSocket
    start_server = websockets.serve(
        handle_websocket_connection, 
        host, 
        port
    )
    
    try:
        await start_server
        # Mantener el servidor ejecutándose
        await asyncio.Future()  # Correr indefinidamente
        
    except KeyboardInterrupt:
        logger.info("⏹️ Servidor detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error en servidor: {e}")

if __name__ == "__main__":
    # Ejecutar el servidor WebSocket
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Servidor WebSocket detenido")
