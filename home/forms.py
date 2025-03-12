from django import forms
from .models import ContactMessage
from products.models import Product, Category


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    rating = forms.FloatField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        help_text="Enter a rating between 1.0 and 5.0 (decimals allowed)."
    )
    name = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter LEGO set name'}),
        required=True
    )
    category = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter or select a category'}),
        required=False
    )

    class Meta:
        model = Product
        fields = [
            "name", "description", "category", "stock", "rating", "image"
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
