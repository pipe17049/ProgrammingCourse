#!/usr/bin/env python3
"""
Consumidor WebSocket que escucha notificaciones del servidor de tareas
Muestra en tiempo real las actualizaciones de tareas
"""

import asyncio
import websockets
import json
from datetime import datetime

class TaskNotificationConsumer:
    """Clase para manejar las notificaciones de tareas via WebSocket"""
    
    def __init__(self, websocket_url="ws://localhost:8765"):
        self.websocket_url = websocket_url
        self.is_running = False
        
    async def connect_and_listen(self):
        """Conecta al servidor WebSocket y escucha mensajes"""
        print("🚀 Iniciando consumidor de notificaciones de tareas...")
        print(f"📍 Conectando a: {self.websocket_url}")
        print("⏹️  Para detener: Ctrl+C")
        print("-" * 50)
        
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                self.is_running = True
                print("✅ Conectado al servidor WebSocket")
                
                # Escuchar mensajes continuamente
                async for message in websocket:
                    await self.process_message(message)
                    
        except websockets.exceptions.ConnectionClosed:
            print("❌ Conexión cerrada por el servidor")
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            print("💡 Asegúrate de que el servidor WebSocket esté ejecutándose")
        finally:
            self.is_running = False
            print("👋 Desconectado del servidor WebSocket")
    
    async def process_message(self, message):
        """Procesa y muestra los mensajes recibidos"""
        try:
            data = json.loads(message)
            message_type = data.get("type", "unknown")
            timestamp = datetime.fromisoformat(data.get("timestamp", "").replace('Z', ''))
            formatted_time = timestamp.strftime("%H:%M:%S")
            
            print(f"\n[{formatted_time}] ", end="")
            
            if message_type == "connection":
                # Mensaje de conexión inicial
                print(f"🔗 {data.get('message')}")
                print(f"👥 Clientes conectados: {data.get('client_count', 1)}")
                
            elif message_type == "task_notification":
                # Notificación de tarea
                action = data.get("action", "unknown")
                task = data.get("task", {})
                message_text = data.get("message", "")
                
                print(f"📋 {message_text}")
                
                # Mostrar detalles de la tarea
                if task:
                    print(f"   📝 ID: {task.get('id', 'N/A')}")
                    print(f"   📋 Título: {task.get('title', 'Sin título')}")
                    
                    if task.get('description'):
                        description = task['description'][:50] + "..." if len(task.get('description', '')) > 50 else task.get('description')
                        print(f"   📄 Descripción: {description}")
                    
                    status = "✅ Completada" if task.get('completed') else "⏳ Pendiente"
                    print(f"   📊 Estado: {status}")
                    
                    if action == "created":
                        print(f"   🕐 Creada: {task.get('created_at', 'N/A')}")
            
            else:
                # Mensaje genérico
                print(f"📨 {data}")
            
            print("-" * 30)
            
        except json.JSONDecodeError:
            print(f"❌ Mensaje no válido (no JSON): {message}")
        except Exception as e:
            print(f"❌ Error procesando mensaje: {e}")

    async def run(self):
        """Ejecuta el consumidor con reconexión automática"""
        retry_count = 0
        max_retries = 5
        
        while retry_count < max_retries:
            try:
                await self.connect_and_listen()
                break  # Conexión exitosa, salir del bucle
                
            except KeyboardInterrupt:
                print("\n⏹️ Detenido por el usuario")
                break
                
            except Exception as e:
                retry_count += 1
                print(f"❌ Error de conexión (intento {retry_count}/{max_retries}): {e}")
                
                if retry_count < max_retries:
                    print(f"🔄 Reintentando en 3 segundos...")
                    await asyncio.sleep(3)
                else:
                    print("❌ Máximo número de reintentos alcanzado")

def main():
    """Función principal"""
    print("🎯 Consumidor de Notificaciones de Tareas")
    print("=" * 50)
    
    # Crear y ejecutar el consumidor
    consumer = TaskNotificationConsumer()
    
    try:
        asyncio.run(consumer.run())
    except KeyboardInterrupt:
        print("\n👋 Consumidor detenido por el usuario")

if __name__ == "__main__":
    main()
