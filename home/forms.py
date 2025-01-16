from django import forms
from .models import LegoSet

class LegoSetForm(forms.ModelForm):
    class Meta:
        model = LegoSet
        fields = ['title', 'description', 'piece_count', 'image', 'availability', 'theme']