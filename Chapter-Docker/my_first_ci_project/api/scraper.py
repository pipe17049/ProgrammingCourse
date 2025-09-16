import requests
from bs4 import BeautifulSoup
import re
import time
from django.core.cache import cache

class MercadoLibreScraper:
    def __init__(self):
        self.base_url = "https://listado.mercadolibre.com.mx"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search_product(self, product_name, max_results=5):
        """Buscar productos en MercadoLibre"""
        try:
            # Crear URL de búsqueda
            search_query = product_name.replace(' ', '-').lower()
            url = f"{self.base_url}/{search_query}"
            
            print(f"🔍 Buscando '{product_name}' en: {url}")
            
            # Realizar request
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar contenedores de productos
            products = []
            product_containers = soup.find_all('div', class_='ui-search-result__wrapper')
            
            for container in product_containers[:max_results]:
                product_data = self._extract_product_data(container)
                if product_data:
                    products.append(product_data)
            
            print(f"✅ Encontrados {len(products)} productos")
            return products
            
        except Exception as e:
            print(f"❌ Error scraping MercadoLibre: {e}")
            return []
    
    def _extract_product_data(self, container):
        """Extraer datos de un producto específico"""
        try:
            # Título
            title_element = container.find('h2', class_='ui-search-item__title')
            title = title_element.text.strip() if title_element else "Sin título"
            
            # Precio
            price_element = container.find('span', class_='andes-money-amount__fraction')
            price = 0.0
            if price_element:
                price_text = price_element.text.replace(',', '').replace('.', '')
                price = float(price_text) if price_text.isdigit() else 0.0
            
            # URL del producto
            link_element = container.find('a', class_='ui-search-link')
            product_url = link_element.get('href') if link_element else ""
            
            # Envío gratis
            shipping_element = container.find('span', class_='ui-search-item__shipping')
            free_shipping = "Envío gratis" in shipping_element.text if shipping_element else False
            
            # Ubicación
            location_element = container.find('span', class_='ui-search-item__group__element')
            location = location_element.text.strip() if location_element else "No especificado"
            
            return {
                'title': title[:100],  # Limitar título
                'price': price,
                'url': product_url,
                'free_shipping': free_shipping,
                'location': location,
                'source': 'MercadoLibre'
            }
            
        except Exception as e:
            print(f"⚠️ Error extrayendo datos del producto: {e}")
            return None
    
    def get_product_details(self, product_url):
        """Obtener detalles específicos de un producto"""
        try:
            response = requests.get(product_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Precio actual
            price_element = soup.find('span', class_='andes-money-amount__fraction')
            current_price = 0.0
            if price_element:
                price_text = price_element.text.replace(',', '').replace('.', '')
                current_price = float(price_text) if price_text.isdigit() else 0.0
            
            # Disponibilidad
            stock_element = soup.find('span', class_='ui-pdp-buybox__quantity__available')
            in_stock = stock_element is not None
            
            # Vendedor
            seller_element = soup.find('span', class_='ui-pdp-seller__header__title')
            seller = seller_element.text.strip() if seller_element else "Vendedor no especificado"
            
            return {
                'current_price': current_price,
                'in_stock': in_stock,
                'seller': seller,
                'last_checked': time.time()
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo detalles: {e}")
            return None

def search_and_cache_products(product_name, max_results=5):
    """Función helper con cache"""
    cache_key = f'ml_search_{product_name.replace(" ", "_")}'
    cached_results = cache.get(cache_key)
    
    if cached_results:
        print(f"✅ Cache hit para búsqueda: {product_name}")
        return cached_results
    
    # Cache miss - hacer scraping
    scraper = MercadoLibreScraper()
    results = scraper.search_product(product_name, max_results)
    
    # Cache por 30 minutos
    cache.set(cache_key, results, 1800)
    
    return results 