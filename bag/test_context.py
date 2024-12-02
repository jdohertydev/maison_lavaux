from django.test import TestCase, RequestFactory
from django.conf import settings
from products.models import Product
from your_app.contexts import bag_contents


class BagContentsTests(TestCase):
    """
    Tests for the bag_contents function to verify context data accuracy.
    """

    def setUp(self):
        """
        Set up test data and configurations for bag_contents tests.
        """
        self.factory = RequestFactory()
        self.product = Product.objects.create(
            name="Test Product",
            price=10.00,
            stock_quantity=100,
        )
        settings.FREE_DELIVERY_THRESHOLD = 50.00
        settings.STANDARD_DELIVERY_PERCENTAGE = 10.00

    def test_bag_contents_empty(self):
        """
        Test that the context is accurate when the bag is empty.
        """
        request = self.factory.get("/")
        request.session = {"bag": {}}
        context = bag_contents(request)
        self.assertEqual(context["product_count"], 0)
        self.assertEqual(context["grand_total"], 0)

    def test_bag_contents_with_items(self):
        """
        Test that the context reflects correct data with items in the bag.
        """
        request = self.factory.get("/")
        request.session = {"bag": {str(self.product.id): 2}}
        context = bag_contents(request)
        self.assertEqual(context["product_count"], 2)
        self.assertEqual(context["total"], 20.00)
        self.assertGreater(context["delivery"], 0)

    def test_bag_contents_free_delivery(self):
        """
        Test that delivery cost is zero when the total exceeds the free delivery threshold.
        """
        request = self.factory.get("/")
        request.session = {"bag": {str(self.product.id): 5}}
        context = bag_contents(request)
        self.assertEqual(context["delivery"], 0)
