import asyncio
import websockets
import json
import time
from datetime import datetime
from colorama import init, Fore, Style
import os
from dotenv import load_dotenv

# Initialize colorama for colored output
init()

# Load environment variables
load_dotenv()

class ProductConsumer:
    def __init__(self):
        self.websocket_url = os.getenv('WEBSOCKET_URL', 'ws://localhost:8765')
        self.reconnect_interval = 5  # seconds
        self.max_reconnect_attempts = 10
        self.connected = False
        
    def log_message(self, message, color=Fore.WHITE):
        """Log message with timestamp and color"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] {message}{Style.RESET_ALL}")
    
    async def connect_and_listen(self):
        """Connect to WebSocket and listen for messages"""
        attempts = 0
        
        while attempts < self.max_reconnect_attempts:
            try:
                self.log_message(f"Attempting to connect to {self.websocket_url}", Fore.YELLOW)
                
                async with websockets.connect(self.websocket_url) as websocket:
                    self.connected = True
                    attempts = 0  # Reset attempts on successful connection
                    self.log_message("✅ Connected to WebSocket server!", Fore.GREEN)
                    
                    # Send a ping to test connection
                    await websocket.send(json.dumps({"type": "ping"}))
                    
                    # Listen for messages
                    async for message in websocket:
                        await self.handle_message(message)
                        
            except websockets.exceptions.ConnectionClosed:
                self.connected = False
                self.log_message("❌ Connection closed by server", Fore.RED)
                break
                
            except Exception as e:
                attempts += 1
                self.connected = False
                self.log_message(f"❌ Connection failed: {e}", Fore.RED)
                
                if attempts < self.max_reconnect_attempts:
                    self.log_message(f"🔄 Retrying in {self.reconnect_interval} seconds... (Attempt {attempts}/{self.max_reconnect_attempts})", Fore.YELLOW)
                    await asyncio.sleep(self.reconnect_interval)
                else:
                    self.log_message("💥 Max reconnection attempts reached. Giving up.", Fore.RED)
                    break
    
    async def handle_message(self, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'connection_established':
                self.log_message(f"🎉 {data.get('message')}", Fore.GREEN)
                
            elif message_type == 'pong':
                self.log_message("🏓 Pong received - Server is alive", Fore.CYAN)
                
            elif message_type == 'product_created':
                product = data.get('product', {})
                timestamp = data.get('timestamp', time.time())
                self.log_message("🆕 NEW PRODUCT CREATED!", Fore.MAGENTA)
                self.log_message(f"   📦 ID: {product.get('id')}", Fore.WHITE)
                self.log_message(f"   🏷️  Name: {product.get('nombre')}", Fore.WHITE)
                self.log_message(f"   💰 Price: ${product.get('precio')}", Fore.WHITE)
                self.log_message(f"   📏 Size: {product.get('talla')}", Fore.WHITE)
                self.log_message(f"   ⏰ Created at: {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')}", Fore.WHITE)
                self.log_message("-" * 50, Fore.WHITE)
                
            elif message_type == 'status':
                clients = data.get('connected_clients', 0)
                self.log_message(f"📊 Server Status: {clients} clients connected", Fore.BLUE)
                
            elif message_type == 'error':
                self.log_message(f"⚠️  Server Error: {data.get('message')}", Fore.RED)
                
            else:
                self.log_message(f"📨 Unknown message type: {message_type}", Fore.YELLOW)
                self.log_message(f"   Data: {data}", Fore.WHITE)
                
        except json.JSONDecodeError:
            self.log_message(f"❌ Invalid JSON received: {message}", Fore.RED)
        except Exception as e:
            self.log_message(f"❌ Error handling message: {e}", Fore.RED)

    async def interactive_mode(self):
        """Interactive mode to send commands"""
        print(f"\n{Fore.CYAN}=== Interactive Mode ==={Style.RESET_ALL}")
        print("Commands:")
        print("  'ping' - Send ping to server")
        print("  'status' - Get server status")
        print("  'quit' - Exit application")
        print("  'help' - Show this help")
        print("-" * 30)
        
        while self.connected:
            try:
                command = input(f"{Fore.GREEN}> {Style.RESET_ALL}").strip().lower()
                
                if command == 'quit':
                    break
                elif command == 'help':
                    print("Available commands: ping, status, quit, help")
                elif command == 'ping':
                    self.log_message("Sending ping...", Fore.CYAN)
                elif command == 'status':
                    self.log_message("Requesting server status...", Fore.CYAN)
                else:
                    print(f"Unknown command: {command}")
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break

async def main():
    """Main function"""
    consumer = ProductConsumer()
    
    print(f"{Fore.CYAN}{'='*60}")
    print(f"🚀 Product WebSocket Consumer Starting...")
    print(f"📡 Server: {consumer.websocket_url}")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    try:
        await consumer.connect_and_listen()
    except KeyboardInterrupt:
        consumer.log_message("👋 Shutting down gracefully...", Fore.YELLOW)
    except Exception as e:
        consumer.log_message(f"💥 Unexpected error: {e}", Fore.RED)

if __name__ == "__main__":
    asyncio.run(main()) 