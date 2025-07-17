from django.test import TestCase

# Create your tests here.

class ProductDetailTest(TestCase):
    def test_product_detail(self):
        response = self.client.get('/api/product/1/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"product": "random-name",   "price": 19.99, "id": 1}
        )