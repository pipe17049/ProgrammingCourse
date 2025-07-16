from django.shortcuts import render

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