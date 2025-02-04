from django import forms
from .models import LegoSet, ContactMessage


class LegoSetForm(forms.ModelForm):
    class Meta:
        model = LegoSet
        fields = ['title', 'description', 'piece_count', 'image', 'availability', 'theme']


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']