import asyncio
import json
import os
import threading
import time

import websockets
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.cache import cache

from api.models import Product
from api.scraper import search_and_cache_products, MercadoLibreScraper


async def send_websocket_notification(message):
    """Send notification to WebSocket service"""
    
    try:
        websocket_url = os.getenv('WEBSOCKET_URL', 'ws://websocket-service:8765')
        async with websockets.connect(websocket_url, timeout=5) as websocket:
            await websocket.send(json.dumps({
                "type": "product_notification",
                "product": message.get('product'),
                "timestamp": message.get('timestamp')
            }))
            print(f"✅ Notified WebSocket service: {message.get('product', {}).get('nombre', 'Unknown')}")
    except Exception as e:
        print(f"❌ Error notifying WebSocket service: {e}")


def notify_websocket_in_thread(message):
    """Run WebSocket notification in separate thread to avoid blocking Django"""
  
    
    def websocket_thread():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_websocket_notification(message))
            loop.close()
        except Exception as e:
            print(f"Error in WebSocket thread: {e}")
    
    thread = threading.Thread(target=websocket_thread)
    thread.daemon = True
    thread.start()


def home(request):
    return HttpResponse("¡Hola desde la app API!")


@api_view(['POST'])
def create_product(request):
    data = request.data
    product = Product(
        nombre=data.get('nombre'),
        precio=data.get('precio'),
        talla=data.get('talla')
    )
    product.save()
    
    product_data = {
        "id": str(product.id),  # Convertir ObjectId a string
        "nombre": product.nombre,
        "precio": float(product.precio),
        "talla": product.talla
    }
    
    # Notify WebSocket server about new product
    message = {
        "type": "product_created",
        "product": product_data,
        "timestamp": time.time()
    }
    notify_websocket_in_thread(message)
    
    return Response(product_data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_product(request, id):
    """Obtener producto con cache"""
    cache_key = f'product_data_{id}'
    product_data = cache.get(cache_key)
    
    if product_data is None:
        # Cache MISS - buscar en DB
        try:
            print(f"🔍 Cache miss for product {id} - querying database")
            product = Product.objects.get(id=id)
            
            # Preparar datos para cache (solo datos simples, no Response)
            product_data = {
                "id": str(product.id),
            "nombre": product.nombre,
            "precio": float(product.precio),
            "talla": product.talla
            }
            
            # Guardar en cache (solo datos simples)
            cache.set(cache_key, product_data, 3600)  # 1 hora
            print(f"💾 Cached product {id} for 1 hour")
        
        except Product.DoesNotExist:
            return Response({
                "error": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            # Cache HIT
            print(f"✅ Cache hit for product {id}")

    # Siempre retornar Response al final
    return Response(product_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_products(request):
    """Listar todos los productos para ver los ObjectIds reales"""
    products = Product.objects.all()
    product_list = []
    for product in products:
        product_list.append({
            "id": str(product.id),  # ObjectId como string
            "nombre": product.nombre,
            "precio": float(product.precio),
            "talla": product.talla
        })
    
    return Response({
        "count": len(product_list),
        "products": product_list
    })


@api_view(['GET'])
def search_mercadolibre(request):
    """Buscar productos en MercadoLibre"""
    product_name = request.GET.get('q', '')
    max_results = int(request.GET.get('limit', 5))
    
    if not product_name:
        return Response({
            "error": "Parameter 'q' (product name) is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if len(product_name) < 3:
        return Response({
            "error": "Product name must be at least 3 characters"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        print(f"🔍 API: Searching for '{product_name}' on MercadoLibre")
        
        # Usar scraper con cache
        results = search_and_cache_products(product_name, max_results)
        
        return Response({
            "query": product_name,
            "results_count": len(results),
            "products": results,
            "source": "MercadoLibre México"
        })
        
    except Exception as e:
        return Response({
            "error": f"Error searching products: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def compare_product_prices(request):
    """Comparar precios de un producto local con MercadoLibre"""
    try:
        product_id = request.data.get('product_id')
        
        if not product_id:
            return Response({
                "error": "product_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Obtener producto local
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({
                "error": "Product not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Buscar en MercadoLibre
        ml_results = search_and_cache_products(product.nombre, 3)
        
        # Encontrar el precio más bajo en ML
        ml_prices = [p['price'] for p in ml_results if p['price'] > 0]
        lowest_ml_price = min(ml_prices) if ml_prices else None
        
        # Comparación
        comparison = {
            "local_product": {
                "id": str(product.id),
                "name": product.nombre,
                "price": float(product.precio),
                "size": product.talla
            },
            "mercadolibre_results": ml_results,
            "price_analysis": {
                "our_price": float(product.precio),
                "lowest_ml_price": lowest_ml_price,
                "price_difference": float(product.precio) - lowest_ml_price if lowest_ml_price else None,
                "is_competitive": float(product.precio) <= lowest_ml_price if lowest_ml_price else None
            }
        }
        
        return Response(comparison)
        
    except Exception as e:
        return Response({
            "error": f"Error comparing prices: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_product_details_ml(request):
    """Obtener detalles específicos de un producto de MercadoLibre"""
    product_url = request.GET.get('url', '')
    
    if not product_url:
        return Response({
            "error": "Parameter 'url' is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if 'mercadolibre.com' not in product_url:
        return Response({
            "error": "URL must be from MercadoLibre"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Cache por URL
        cache_key = f'ml_details_{hash(product_url)}'
        cached_details = cache.get(cache_key)
        
        if cached_details:
            print(f"✅ Cache hit for product details")
            return Response(cached_details)
        
        # Scraper para detalles
        scraper = MercadoLibreScraper()
        details = scraper.get_product_details(product_url)
        
        if details:
            details['url'] = product_url
            # Cache por 10 minutos
            cache.set(cache_key, details, 600)
            return Response(details)
        else:
            return Response({
                "error": "Could not extract product details"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    except Exception as e:
        return Response({
            "error": f"Error getting product details: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)