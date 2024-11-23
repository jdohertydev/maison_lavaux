from django.test import TestCase
from django.urls import reverse

class ProductViewsTest(TestCase):
    def test_product_list_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
