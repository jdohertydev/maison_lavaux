from django import forms
from .widgets import CustomClearableFileInput
from .models import Review, Product, Category
from django.core.exceptions import ValidationError


class ReviewForm(forms.ModelForm):
    """
    Form for adding and editing reviews.
    """

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Choices from 1 to 5

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Rating",
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your review here...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with optional user and product for validation."""
        self.user = kwargs.pop("user", None)
        self.product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Custom validation to prevent duplicate reviews by the same user
        for the same product.
        """

        cleaned_data = super().clean()

        if not self.instance.pk:  # Ensure this is a new review, not an edit
            if self.user and self.product:
                # Check if a review already exists
                if Review.objects.filter(
                    user=self.user, product=self.product
                ).exists():
                    raise ValidationError(
                        "You have already submitted a review for this product."
                    )

        return cleaned_data


class ProductForm(forms.ModelForm):
    """
    Form for adding and editing products.
    """

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "price",
            "discount_price",
            "description",
            "stock_quantity",
            "is_active",
            "size",
            "image",
        ]  # Explicitly list fields for better control

    def __init__(self, *args, **kwargs):
        """Initialize form and dynamically fetch category choices."""
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [
            (category.id, category.get_friendly_name())
            for category in categories
        ]
        self.fields["category"].choices = friendly_names

        # Add consistent styling to all fields
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "border-black rounded-0")
