import requests
import json
import time
import os
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama
init()

# Load environment variables
load_dotenv()

class APITester:
    def __init__(self):
        self.base_url = os.getenv('API_URL', 'http://localhost:8000/api')
        
    def log_message(self, message, color=Fore.WHITE):
        """Log message with color"""
        print(f"{color}{message}{Style.RESET_ALL}")
    
    def create_product(self, nombre, precio, talla):
        """Create a new product via REST API"""
        url = f"{self.base_url}/product/"
        data = {
            "nombre": nombre,
            "precio": precio,
            "talla": talla
        }
        
        try:
            self.log_message(f"🚀 Creating product: {nombre}", Fore.YELLOW)
            response = requests.post(url, json=data)
            
            if response.status_code == 201:
                product = response.json()
                self.log_message("✅ Product created successfully!", Fore.GREEN)
                self.log_message(f"   📦 ID: {product.get('id')}", Fore.WHITE)
                self.log_message(f"   🏷️  Name: {product.get('nombre')}", Fore.WHITE)
                self.log_message(f"   💰 Price: ${product.get('precio')}", Fore.WHITE)
                self.log_message(f"   📏 Size: {product.get('talla')}", Fore.WHITE)
                return product
            else:
                self.log_message(f"❌ Error creating product: {response.status_code}", Fore.RED)
                self.log_message(f"   Response: {response.text}", Fore.RED)
                return None
                
        except Exception as e:
            self.log_message(f"❌ Connection error: {e}", Fore.RED)
            return None
    
    def list_products(self):
        """List all products"""
        url = f"{self.base_url}/products/"
        
        try:
            self.log_message("📋 Fetching products list...", Fore.CYAN)
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', [])
                count = data.get('count', 0)
                
                self.log_message(f"📊 Found {count} products:", Fore.GREEN)
                for product in products:
                    self.log_message(f"   • {product.get('nombre')} - ${product.get('precio')} ({product.get('talla')})", Fore.WHITE)
                return products
            else:
                self.log_message(f"❌ Error fetching products: {response.status_code}", Fore.RED)
                return []
                
        except Exception as e:
            self.log_message(f"❌ Connection error: {e}", Fore.RED)
            return []

def run_interactive_test():
    """Interactive testing mode"""
    tester = APITester()
    
    print(f"{Fore.CYAN}{'='*60}")
    print(f"🧪 API Tester - Interactive Mode")
    print(f"📡 API Server: {tester.base_url}")
    print(f"{'='*60}{Style.RESET_ALL}")
    print("\nCommands:")
    print("  'create' - Create a new product")
    print("  'list' - List all products")
    print("  'auto' - Auto-create test products")
    print("  'quit' - Exit")
    print("-" * 30)
    
    while True:
        try:
            command = input(f"{Fore.GREEN}API> {Style.RESET_ALL}").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'create':
                nombre = input("Product name: ").strip()
                precio = float(input("Price: ").strip())
                talla = input("Size: ").strip()
                
                tester.create_product(nombre, precio, talla)
                
            elif command == 'list':
                tester.list_products()
                
            elif command == 'auto':
                print(f"{Fore.YELLOW}🤖 Auto-creating test products...{Style.RESET_ALL}")
                test_products = [
                    ("T-Shirt Red", 25.99, "M"),
                    ("Jeans Blue", 79.50, "L"),
                    ("Sneakers White", 120.00, "42"),
                    ("Hoodie Black", 55.99, "XL"),
                    ("Cap Green", 18.75, "One Size")
                ]
                
                for nombre, precio, talla in test_products:
                    tester.create_product(nombre, precio, talla)
                    time.sleep(1)  # Wait 1 second between creations
                    
            elif command == 'help':
                print("Commands: create, list, auto, quit")
            else:
                print(f"Unknown command: {command}")
                
        except KeyboardInterrupt:
            break
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except EOFError:
            break
    
    print(f"{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")

if __name__ == "__main__":
    run_interactive_test() 