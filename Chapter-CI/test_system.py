#!/usr/bin/env python3
"""
Quick test script for the Producer-Consumer WebSocket system
"""
import requests
import time
import asyncio
import websockets
import json
from colorama import init, Fore, Style

init()

class SystemTester:
    def __init__(self):
        self.api_url = "http://localhost:8000/api"
        self.websocket_url = "ws://localhost:8765"
        
    def log(self, message, color=Fore.WHITE):
        timestamp = time.strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] {message}{Style.RESET_ALL}")
    
    def test_api_connection(self):
        """Test if Django API is accessible"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=5)
            if response.status_code == 200:
                self.log("✅ Django API is accessible", Fore.GREEN)
                return True
            else:
                self.log(f"❌ Django API returned status {response.status_code}", Fore.RED)
                return False
        except Exception as e:
            self.log(f"❌ Cannot reach Django API: {e}", Fore.RED)
            return False
    
    async def test_websocket_connection(self):
        """Test if WebSocket server is accessible"""
        try:
            async with websockets.connect(self.websocket_url, timeout=5) as websocket:
                self.log("✅ WebSocket server is accessible", Fore.GREEN)
                
                # Send ping
                await websocket.send(json.dumps({"type": "ping"}))
                response = await websocket.recv()
                data = json.loads(response)
                
                if data.get('type') == 'pong':
                    self.log("✅ WebSocket ping-pong successful", Fore.GREEN)
                    return True
                else:
                    self.log(f"❌ Unexpected WebSocket response: {data}", Fore.RED)
                    return False
                    
        except Exception as e:
            self.log(f"❌ Cannot reach WebSocket server: {e}", Fore.RED)
            return False
    
    def create_test_product(self):
        """Create a test product via API"""
        try:
            data = {
                "nombre": f"Test Product {int(time.time())}",
                "precio": 99.99,
                "talla": "M"
            }
            
            response = requests.post(f"{self.api_url}/product/", json=data, timeout=5)
            
            if response.status_code == 201:
                product = response.json()
                self.log(f"✅ Product created: {product['nombre']}", Fore.GREEN)
                return product
            else:
                self.log(f"❌ Failed to create product: {response.status_code}", Fore.RED)
                return None
                
        except Exception as e:
            self.log(f"❌ Error creating product: {e}", Fore.RED)
            return None
    
    async def listen_websocket_messages(self, duration=10):
        """Listen for WebSocket messages for a specific duration"""
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                self.log(f"🎧 Listening for WebSocket messages for {duration} seconds...", Fore.CYAN)
                
                end_time = time.time() + duration
                message_count = 0
                
                while time.time() < end_time:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(message)
                        message_count += 1
                        
                        if data.get('type') == 'product_created':
                            product = data.get('product', {})
                            self.log(f"📦 Received product notification: {product.get('nombre')}", Fore.MAGENTA)
                        else:
                            self.log(f"📨 Received message: {data.get('type')}", Fore.YELLOW)
                            
                    except asyncio.TimeoutError:
                        continue  # No message received, continue listening
                
                self.log(f"📊 Received {message_count} messages in {duration} seconds", Fore.BLUE)
                return message_count > 0
                
        except Exception as e:
            self.log(f"❌ Error listening to WebSocket: {e}", Fore.RED)
            return False

async def run_full_test():
    """Run complete system test"""
    tester = SystemTester()
    
    print(f"{Fore.CYAN}{'='*60}")
    print(f"🧪 Producer-Consumer System Test")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    # Test 1: API Connection
    tester.log("🔍 Testing API connection...", Fore.YELLOW)
    api_ok = tester.test_api_connection()
    
    # Test 2: WebSocket Connection
    tester.log("🔍 Testing WebSocket connection...", Fore.YELLOW)
    ws_ok = await tester.test_websocket_connection()
    
    if not (api_ok and ws_ok):
        tester.log("❌ Basic connectivity tests failed. Check if services are running.", Fore.RED)
        return False
    
    # Test 3: End-to-end flow
    tester.log("🔍 Testing end-to-end producer-consumer flow...", Fore.YELLOW)
    
    # Start listening in background
    listen_task = asyncio.create_task(tester.listen_websocket_messages(15))
    
    # Wait a bit for WebSocket to be ready
    await asyncio.sleep(2)
    
    # Create some test products
    for i in range(3):
        tester.create_test_product()
        await asyncio.sleep(1)
    
    # Wait for listening task to complete
    messages_received = await listen_task
    
    if messages_received:
        tester.log("✅ End-to-end test successful!", Fore.GREEN)
        tester.log("🎉 Producer-Consumer system is working correctly!", Fore.GREEN)
        return True
    else:
        tester.log("❌ No WebSocket messages received", Fore.RED)
        return False

def print_usage():
    """Print usage instructions"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"🚀 How to run the complete system:")
    print(f"{'='*60}{Style.RESET_ALL}")
    print()
    print("1. Start all services:")
    print(f"   {Fore.YELLOW}cd Chapter-CI && docker-compose up{Style.RESET_ALL}")
    print()
    print("2. In another terminal, run this test:")
    print(f"   {Fore.YELLOW}python test_system.py{Style.RESET_ALL}")
    print()
    print("3. Or run the consumer manually:")
    print(f"   {Fore.YELLOW}cd my_first_consumer && python websocket_client.py{Style.RESET_ALL}")
    print()
    print("4. Generate events with the API tester:")
    print(f"   {Fore.YELLOW}cd my_first_consumer && python test_api.py{Style.RESET_ALL}")
    print()

if __name__ == "__main__":
    print_usage()
    
    try:
        result = asyncio.run(run_full_test())
        exit_code = 0 if result else 1
        exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Test interrupted by user{Style.RESET_ALL}")
        exit(1) 