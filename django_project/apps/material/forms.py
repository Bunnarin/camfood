from django import forms
from django.core.exceptions import ValidationError
from .models import Material

class PurchaseInlineForm(forms.Form):
    material = forms.ModelChoiceField(Material.objects)
    quantity = forms.IntegerField()
    price = forms.IntegerField(required=False)

    def clean(self):
        data = super().clean()
        if not data.get('material'):
            raise ValidationError({'material': 'invalid'})
        if not data.get('quantity'):
            raise ValidationError({'quantity': 'invalid'})
        
        # if price is not provided, calculate
        if not data.get('price'):
            data['price'] = data['material'].price * data['quantity']

        return data