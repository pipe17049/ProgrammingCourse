from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Product
from django.http import HttpResponse

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
    
    return Response({
        "id": str(product.id),  # Convertir ObjectId a string
        "nombre": product.nombre,
        "precio": float(product.precio),
        "talla": product.talla
    }, status=status.HTTP_201_CREATED)

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