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

from api.models import Product


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
    try:
        product = Product.objects.get(id=id)  # mongoengine maneja ObjectId automáticamente
        
        return Response({
            "id": str(product.id),  # Convertir ObjectId a string
            "nombre": product.nombre,
            "precio": float(product.precio),
            "talla": product.talla
        }, status=status.HTTP_200_OK)
        
    except Product.DoesNotExist:
        return Response({
            "error": "Product not found"
        }, status=status.HTTP_404_NOT_FOUND)


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