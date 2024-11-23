from django.test import TestCase
from django.contrib.auth.models import User
from products.forms import ReviewForm, ProductForm
from products.models import Review, Product, Category

class ReviewFormTest(TestCase):
    def setUp(self):
        """Set up test data for ReviewForm."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Fragrances', friendly_name='Luxury Fragrances')
        self.product = Product.objects.create(
            name='Luxury Perfume',
            category=self.category,
            price=100.00,
            description='A premium fragrance.',
            stock_quantity=10
        )
    
    def test_valid_review_form(self):
        """Test that a valid review form passes validation."""
        form_data = {'rating': '5', 'comment': 'Amazing product!'}
        form = ReviewForm(data=form_data, user=self.user, product=self.product)
        self.assertTrue(form.is_valid())
    
    def test_duplicate_review_validation(self):
        """Test that duplicate reviews by the same user for the same product are invalid."""
        Review.objects.create(user=self.user, product=self.product, rating=5, comment='Great!')
        form_data = {'rating': '4', 'comment': 'Still great!'}
        form = ReviewForm(data=form_data, user=self.user, product=self.product)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'],
            ["You have already submitted a review for this product."]
        )

    def test_review_form_missing_rating(self):
        """Test that a review form missing a rating is invalid."""
        form_data = {'comment': 'Nice product!'}
        form = ReviewForm(data=form_data, user=self.user, product=self.product)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)


class ProductFormTest(TestCase):
    def setUp(self):
        """Set up test data for ProductForm."""
        self.category = Category.objects.create(name='Fragrances', friendly_name='Luxury Fragrances')
    
    def test_valid_product_form(self):
        """Test that a valid product form passes validation."""
        form_data = {
            'name': 'Luxury Perfume',
            'category': self.category.id,
            'price': 100.00,
            'discount_price': 80.00,
            'description': 'A premium fragrance.',
            'stock_quantity': 50,
            'is_active': True,
            'size': '50ml',
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_product_form_missing_name(self):
        """Test that a product form missing the name field is invalid."""
        form_data = {
            'category': self.category.id,
            'price': 100.00,
            'description': 'A premium fragrance.',
            'stock_quantity': 50,
            'is_active': True,
            'size': '50ml',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_product_form_invalid_discount_price(self):
        """Test that a discount price higher than the price is invalid."""
        form_data = {
            'name': 'Luxury Perfume',
            'category': self.category.id,
            'price': 100.00,
            'discount_price': 120.00,  # Invalid discount price
            'description': 'A premium fragrance.',
            'stock_quantity': 50,
            'is_active': True,
            'size': '50ml',
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Discount price must be less than the original price.',
            form.errors['__all__']
        )

    def test_product_form_category_choices(self):
        """Test that the category field contains the correct friendly names."""
        form = ProductForm()
        self.assertIn((self.category.id, 'Luxury Fragrances'), form.fields['category'].choices)
