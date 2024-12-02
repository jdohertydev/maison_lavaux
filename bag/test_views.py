from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product
from analytics.models import SalesData


class BagViewsTest(TestCase):
    """
    Tests for the views handling bag functionality, including adding,
    adjusting, and removing products from the bag.
    """

    def setUp(self):
        """
        Set up test data for bag views and initialize client and product.
        """
        self.client = Client()

        # Create a test product
        self.product = Product.objects.create(
            name="Luxury Perfume",
            price=100.00,
            description="A premium fragrance.",
            stock_quantity=10,
        )

        # URL endpoints
        self.view_bag_url = reverse("view_bag")
        self.add_to_bag_url = reverse("add_to_bag", args=[self.product.id])
        self.adjust_bag_url = reverse("adjust_bag", args=[self.product.id])
        self.remove_from_bag_url = reverse(
            "remove_from_bag", args=[self.product.id]
        )

    def test_view_bag(self):
        """
        Test rendering the bag page.
        """
        response = self.client.get(self.view_bag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bag/bag.html")

    def test_add_to_bag(self):
        """
        Test adding a product to the bag and updating SalesData.
        """
        response = self.client.post(
            self.add_to_bag_url,
            {"quantity": 2, "redirect_url": self.view_bag_url},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after adding
        bag = self.client.session["bag"]
        self.assertIn(
            str(self.product.id), bag
        )  # Check if product is in the bag
        self.assertEqual(bag[str(self.product.id)], 2)  # Verify quantity

        # Check SalesData increment
        sales_data = SalesData.objects.get(product=self.product)
        self.assertEqual(sales_data.added_to_cart, 2)

    def test_adjust_bag(self):
        """
        Test adjusting the quantity of a product in the bag.
        """
        # Add product to the bag first
        self.client.post(
            self.add_to_bag_url,
            {"quantity": 2, "redirect_url": self.view_bag_url},
        )
        response = self.client.post(self.adjust_bag_url, {"quantity": 5})
        self.assertEqual(response.status_code, 302)
        bag = self.client.session["bag"]
        self.assertEqual(bag[str(self.product.id)], 5)

    def test_adjust_bag_invalid_quantity(self):
        """
        Test adjusting the quantity to an invalid value (exceeds stock).
        """
        # Add product to the bag first
        self.client.post(
            self.add_to_bag_url,
            {"quantity": 2, "redirect_url": self.view_bag_url},
        )

        # Attempt to adjust quantity to an invalid value (exceeds stock_quantity)
        response = self.client.post(self.adjust_bag_url, {"quantity": 20})
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        messages = list(response.wsgi_request._messages)

        # Ensure the correct error message is displayed
        self.assertEqual(
            str(messages[-1]),
            f"Sorry, only {self.product.stock_quantity} of '{self.product.name}' are available.",
        )

        # Check that the quantity in the bag has not been updated to the invalid value
        bag = self.client.session["bag"]
        self.assertEqual(
            bag[str(self.product.id)], 2
        )  # Quantity remains as initially added
