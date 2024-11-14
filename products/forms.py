from django import forms
from .models import Review, Product, Category

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
