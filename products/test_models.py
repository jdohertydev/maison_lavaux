from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Luxury Perfume",
            price=49.99,
            description="A premium luxury fragrance."
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Luxury Perfume")
        self.assertEqual(self.product.price, 49.99)

    def test_product_str_method(self):
        self.assertEqual(str(self.product), "Luxury Perfume")
