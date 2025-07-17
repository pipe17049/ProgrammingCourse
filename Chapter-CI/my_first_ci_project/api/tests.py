from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import mongoengine
import mongomock
from api.models import Product

class ProductDetailTest(TestCase):
    
    def setUp(self):
        """Configurar datos de prueba con mongomock"""
        self.client = APIClient()
        
        # Configurar mongomock para tests
        mongoengine.disconnect()
        mongoengine.connect('test_db', mongo_client_class=mongomock.MongoClient)
        
        # Crear un producto de prueba (sin _id, deja que MongoDB lo genere)
        self.product = Product(
            nombre="Camisa Test",
            precio=25.99,
            talla="L"
        )
        self.product.save()

    def tearDown(self):
        """Limpiar después de cada test"""
        mongoengine.disconnect()

    def test_get_product_success(self):
        """Test para obtener un producto existente"""
        # Usar el ID real del producto creado
        response = self.client.get(f'/api/product/{str(self.product.id)}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.product.id))
        self.assertEqual(response.data['nombre'], 'Camisa Test')
        self.assertEqual(response.data['precio'], 25.99)
        self.assertEqual(response.data['talla'], 'L')

    def test_get_product_not_found(self):
        """Test para producto que no existe"""
        # Usar un ObjectId falso pero válido
        fake_object_id = "507f1f77bcf86cd799439011"
        response = self.client.get(f'/api/product/{fake_object_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Product not found')

    def test_create_product(self):
        """Test para crear un nuevo producto"""
        data = {
            'nombre': 'Pantalón',
            'precio': 35.50,
            'talla': 'M'
        }
        response = self.client.post('/api/product/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Pantalón')
        self.assertEqual(response.data['precio'], 35.50)
        self.assertEqual(response.data['talla'], 'M')
        self.assertIn('id', response.data)  # Verificar que tiene un ID