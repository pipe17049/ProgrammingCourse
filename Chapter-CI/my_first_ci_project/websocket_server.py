import asyncio
import json
import threading
import time
from queue import Queue

import websockets

# Queue to receive messages from Django (currently unused but kept for potential expansion)
message_queue = Queue()

# Set of connected WebSocket clients
connected_clients = set()


async def handle_client(websocket, path):
    """Handle new WebSocket connections"""
    print(f"New client connected: {websocket.remote_address}")
    connected_clients.add(websocket)
    
    # Send welcome message
    await websocket.send(json.dumps({
        "type": "connection_established",
        "message": "Connected to product updates WebSocket server"
    }))
    
    try:
        async for message in websocket:
            # Handle incoming messages from clients
            try:
                data = json.loads(message)
                message_type = data.get('type')
                
                if message_type == 'ping':
                    await websocket.send(json.dumps({
                        "type": "pong",
                        "message": "Server is alive"
                    }))
                elif message_type == 'get_status':
                    await websocket.send(json.dumps({
                        "type": "status",
                        "connected_clients": len(connected_clients),
                        "message": "WebSocket server running"
                    }))
                elif message_type == 'product_created':
                    # Handle product notifications from Django
                    print(f"📦 Broadcasting product created: {data}")
                    await broadcast_message(data)
                    
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
                
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"Client disconnected: {websocket.remote_address}")


async def broadcast_message(message):
    """Broadcast message to all connected clients"""
    if connected_clients:
        print(f"Broadcasting to {len(connected_clients)} clients: {message}")
        # Create a copy of the set to avoid issues with concurrent modification
        clients_copy = connected_clients.copy()
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in clients_copy],
            return_exceptions=True
        )


def message_processor():
    """Process messages from Django in a separate thread (currently unused)"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def process_queue():
        while True:
            try:
                if not message_queue.empty():
                    message = message_queue.get_nowait()
                    await broadcast_message(message)
                await asyncio.sleep(0.1)  # Small delay to prevent busy waiting
            except Exception as e:
                print(f"Error processing message: {e}")
                await asyncio.sleep(1)
    
    loop.run_until_complete(process_queue())


def add_message_to_queue(message):
    """Add message to queue (currently unused but kept for potential expansion)"""
    message_queue.put(message)


async def main():
    """Start the WebSocket server"""
    print("Starting WebSocket server on localhost:8765")
    
    # Start message processor in a separate thread (currently not used but kept for future)
    processor_thread = threading.Thread(target=message_processor, daemon=True)
    processor_thread.start()
    
    # Start WebSocket server
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    print("WebSocket server is running on ws://localhost:8765")
    
    await server.wait_closed()


if __name__ == "__main__":
    asyncio.run(main()) 