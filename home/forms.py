from django import forms
from .models import ContactMessage
from products.models import Product, Category


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    rating = forms.FloatField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'step': '0.1'}
        ),
        help_text="Enter a rating between 1.0 and 5.0 (decimals allowed)."
    )
    name = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Set Name'}
        ),
        required=True
    )
    existing_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select existing category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Text field to add a new category
    new_category = forms.CharField(
        max_length=254,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Or new category'}
        )
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "existing_category",
            "new_category",
            "stock",
            "rating",
            "image"
        ]

    def clean(self):
        cleaned_data = super().clean()
        existing_category = cleaned_data.get("existing_category")
        new_category = cleaned_data.get("new_category")

        if not existing_category and not new_category:
            raise forms.ValidationError("Please select or enter a new one.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
