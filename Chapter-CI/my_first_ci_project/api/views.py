from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Product
# Create your views here.
from django.http import HttpResponse, JsonResponse

def home(request):
    return HttpResponse("¡Hola desde la app API!")

# http://127.0.0.1:8000/api/product/1/
def product_detail(request, id):
    data = {
        "product": "random-name",
        "id": id,
        "price": 19.99
    }
    return JsonResponse(data)


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
        "message": "Product created successfully",
        "id": str(product.id),  # Convierte a string
        "nombre": product.nombre,
        "precio": float(product.precio) if product.precio else None,  # Asegura que sea float
        "talla": product.talla
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def create_product(request):
    data = request.data
    product = Product(
        nombre=data.get('nombre'),
        precio=data.get('precio'),
        talla=data.get('talla')
    )
    product.save()
    
    return Response({
        "message": "Product created successfully",
        "id": str(product.id),  # Convierte a string
        "nombre": product.nombre,
        "precio": float(product.precio) if product.precio else None,  # Asegura que sea float
        "talla": product.talla
    }, status=status.HTTP_201_CREATED)