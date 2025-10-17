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
        
        # Crear productos de prueba
        self.product1 = Product(
            nombre="Camisa Test",
            precio=25.99,
            talla="L"
        )
        self.product1.save()
        
        self.product2 = Product(
            nombre="Pantalón Test",
            precio=35.50,
            talla="M"
        )
        self.product2.save()

    def tearDown(self):
        """Limpiar después de cada test"""
        mongoengine.disconnect()

    def test_get_product_success(self):
        """Test para obtener un producto existente"""
        response = self.client.get(f'/api/product/{str(self.product1.id)}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.product1.id))
        self.assertEqual(response.data['nombre'], 'Camisa Test')
        self.assertEqual(response.data['precio'], 25.99)
        self.assertEqual(response.data['talla'], 'L')

    def test_get_product_not_found(self):
        """Test para producto que no existe"""
        fake_object_id = "507f1f77bcf86cd799439011"
        response = self.client.get(f'/api/product/{fake_object_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Product not found')

    def test_create_product(self):
        """Test para crear un nuevo producto"""
        data = {
            'nombre': 'Chaqueta',
            'precio': 45.00,
            'talla': 'XL'
        }
        response = self.client.post('/api/product/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], 'Chaqueta')
        self.assertEqual(response.data['precio'], 45.00)
        self.assertEqual(response.data['talla'], 'XL')
        self.assertIn('id', response.data)

    def test_list_products(self):
        """Test para listar todos los productos"""
        response = self.client.get('/api/products/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)  # Tenemos 2 productos del setUp
        self.assertEqual(len(response.data['products']), 2)
        
        # Verificar que ambos productos están en la lista
        nombres = [p['nombre'] for p in response.data['products']]
        self.assertIn('Camisa Test', nombres)
        self.assertIn('Pantalón Test', nombres)
        
        # Verificar estructura de cada producto
        for product in response.data['products']:
            self.assertIn('id', product)
            self.assertIn('nombre', product)
            self.assertIn('precio', product)
            self.assertIn('talla', product)

    def test_list_products_empty(self):
        """Test para listar productos cuando no hay ninguno"""
        # Limpiar todos los productos
        Product.objects.all().delete()
        
        response = self.client.get('/api/products/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(len(response.data['products']), 0)