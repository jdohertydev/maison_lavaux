from django import forms
from .models import Review, Product, Category
from django.core.exceptions import ValidationError

class ReviewForm(forms.ModelForm):
    """
    Form for adding and editing reviews.
    """
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Choices from 1 to 5

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label="Rating",
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review here...',
            }),
        }

    def __init__(self, *args, **kwargs):
        # Capture user and product from view to validate uniqueness
        self.user = kwargs.pop('user', None)
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Custom validation to prevent duplicate reviews by the same user for the same product.
        """
        cleaned_data = super().clean()

        if not self.instance.pk:  # Ensure this is a new review, not an edit
            if self.user and self.product:
                # Check if a review already exists
                if Review.objects.filter(user=self.user, product=self.product).exists():
                    raise ValidationError("You have already submitted a review for this product.")

        return cleaned_data


class ProductForm(forms.ModelForm):
    """
    Form for adding and editing products.
    Dynamically updates the category choices.
    """

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically fetch category choices
        categories = Category.objects.all()
        friendly_names = [(category.id, category.get_friendly_name()) for category in categories]

        self.fields['category'].choices = friendly_names
        # Add a consistent class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'border-black rounded-0'
