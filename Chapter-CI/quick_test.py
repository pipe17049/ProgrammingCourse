#!/usr/bin/env python3
"""
Script rápido para verificar que el sistema Producer-Consumer funciona
"""
import requests
import time
import json
from colorama import init, Fore, Style

init()

def log(message, color=Fore.WHITE):
    timestamp = time.strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] {message}{Style.RESET_ALL}")

def test_system():
    """Test rápido del sistema"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"🧪 Quick System Test")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    # Test 1: Verificar Django
    log("🔍 Testing Django API...", Fore.YELLOW)
    try:
        response = requests.get("http://localhost:8000/api/", timeout=5)
        if response.status_code == 200:
            log("✅ Django API is running!", Fore.GREEN)
        else:
            log(f"❌ Django API error: {response.status_code}", Fore.RED)
            return False
    except Exception as e:
        log(f"❌ Cannot reach Django: {e}", Fore.RED)
        log("💡 Make sure you ran: cd Chapter-CI && docker-compose up", Fore.CYAN)
        return False
    
    # Test 2: Crear producto
    log("🚀 Creating test product via API...", Fore.YELLOW)
    product_data = {
        "nombre": f"Test Product {int(time.time())}",
        "precio": 25.99,
        "talla": "M"
    }
    
    try:
        response = requests.post("http://localhost:8000/api/product/", 
                               json=product_data, timeout=5)
        if response.status_code == 201:
            product = response.json()
            log("✅ Product created successfully!", Fore.GREEN)
            log(f"   📦 ID: {product['id']}", Fore.WHITE)
            log(f"   🏷️  Name: {product['nombre']}", Fore.WHITE)
            log(f"   💰 Price: ${product['precio']}", Fore.WHITE)
            
            log("📡 WebSocket notification should appear in consumer now!", Fore.MAGENTA)
            log("👀 Check your docker-compose logs or WebSocket client!", Fore.CYAN)
            return True
        else:
            log(f"❌ Failed to create product: {response.status_code}", Fore.RED)
            log(f"   Response: {response.text}", Fore.RED)
            return False
            
    except Exception as e:
        log(f"❌ Error creating product: {e}", Fore.RED)
        return False

def show_postman_instructions():
    """Mostrar instrucciones para Postman"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"📮 How to test with Postman:")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. Create new POST request{Style.RESET_ALL}")
    print(f"   URL: {Fore.GREEN}http://localhost:8000/api/product/{Style.RESET_ALL}")
    print()
    print(f"{Fore.YELLOW}2. Set Headers:{Style.RESET_ALL}")
    print(f"   Content-Type: application/json")
    print()
    print(f"{Fore.YELLOW}3. Body (raw JSON):{Style.RESET_ALL}")
    print(f'{Fore.GREEN}{{\n    "nombre": "Producto desde Postman",\n    "precio": 35.99,\n    "talla": "L"\n}}{Style.RESET_ALL}')
    print()
    print(f"{Fore.YELLOW}4. Send request and check:{Style.RESET_ALL}")
    print(f"   ✅ Postman shows 201 Created response")
    print(f"   ✅ WebSocket consumer shows new product notification")
    print()
    
def show_websocket_instructions():
    """Mostrar instrucciones para ver WebSocket"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"👁️  How to see WebSocket messages:")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Option 1 - Docker logs (easiest):{Style.RESET_ALL}")
    print(f"   docker-compose logs -f consumer")
    print()
    print(f"{Fore.YELLOW}Option 2 - Separate terminal:{Style.RESET_ALL}")
    print(f"   cd Chapter-CI/my_first_consumer")
    print(f"   python websocket_client.py")
    print()
    print(f"{Fore.YELLOW}Option 3 - WebSocket client in browser:{Style.RESET_ALL}")
    print(f"   URL: {Fore.GREEN}ws://localhost:8765{Style.RESET_ALL}")
    print()

if __name__ == "__main__":
    show_websocket_instructions()
    show_postman_instructions()
    
    print(f"\n{Fore.MAGENTA}Press Enter to run API test...{Style.RESET_ALL}")
    input()
    
    result = test_system()
    
    if result:
        print(f"\n{Fore.GREEN}✅ System is working! Create more products in Postman to see WebSocket magic!{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}❌ System has issues. Check if docker-compose is running.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Try: cd Chapter-CI && docker-compose up --build{Style.RESET_ALL}") 