import asyncio
import json
import websockets
from datetime import datetime

# Set of connected WebSocket clients
connected_clients = set()

async def handle_client(websocket, path):
    """Handle new WebSocket connections"""
    client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔌 New client connected: {client_info}")
    connected_clients.add(websocket)
    
    # Send welcome message
    await websocket.send(json.dumps({
        "type": "connection_established",
        "message": "Connected to standalone WebSocket service",
        "service": "websocket-service",
        "connected_clients": len(connected_clients)
    }))
    
    try:
        async for message in websocket:
            await handle_message(websocket, message)
                
    except websockets.exceptions.ConnectionClosed:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔌 Client disconnected: {client_info}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Client error: {e}")
    finally:
        connected_clients.discard(websocket)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Connected clients: {len(connected_clients)}")

async def handle_message(websocket, message):
    """Handle incoming messages from clients"""
    try:
        data = json.loads(message)
        message_type = data.get('type')
        
        if message_type == 'ping':
            await websocket.send(json.dumps({
                "type": "pong",
                "message": "WebSocket service is alive",
                "timestamp": datetime.now().isoformat(),
                "connected_clients": len(connected_clients)
            }))
            
        elif message_type == 'get_status':
            await websocket.send(json.dumps({
                "type": "status",
                "service": "websocket-service",
                "connected_clients": len(connected_clients),
                "uptime": "Service running"
            }))
            
        elif message_type == 'broadcast':
            # Broadcast message to all clients (used by producer)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📡 Broadcasting message from producer")
            await broadcast_to_all_clients(data.get('data', {}))
            
        elif message_type == 'product_notification':
            # Handle product notifications from Django producer
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 📦 Product notification received")
            await broadcast_to_all_clients({
                "type": "product_created",
                "product": data.get('product'),
                "timestamp": data.get('timestamp'),
                "source": "django-producer"
            })
            
    except json.JSONDecodeError:
        await websocket.send(json.dumps({
            "type": "error",
            "message": "Invalid JSON format"
        }))
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Message handling error: {e}")

async def broadcast_to_all_clients(message):
    """Broadcast message to all connected clients"""
    if connected_clients:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📢 Broadcasting to {len(connected_clients)} clients")
        # Create a copy to avoid concurrent modification issues
        clients_copy = connected_clients.copy()
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in clients_copy],
            return_exceptions=True
        )
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📭 No clients connected to broadcast to")

async def main():
    """Start the standalone WebSocket service"""
    host = "0.0.0.0"
    port = 8765
    
    print("🚀 Starting Standalone WebSocket Service")
    print("=" * 50)
    print(f"📡 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🌐 URL: ws://{host}:{port}")
    print("=" * 50)
    
    # Start WebSocket server
    async def websocket_handler(websocket):
        await handle_client(websocket, "/")  # Default path
    
    server = await websockets.serve(websocket_handler, host, port)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ WebSocket service running on ws://{host}:{port}")
    
    # Keep server running
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 👋 WebSocket service shutting down gracefully...")
    except Exception as e:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 💥 WebSocket service error: {e}") 