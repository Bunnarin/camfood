from django import forms
from django.core.exceptions import ValidationError
from apps.product.models import Product
from apps.material.models import Material

class ProductInlineForm(forms.Form):
    product = forms.ModelChoiceField(Product.objects)
    product_quantity = forms.IntegerField()

    def clean(self):
        data = super().clean()
        no_both = not data.get('product') and not data.get('product_quantity')
        yes_both = data.get('product') and data.get('product_quantity')
        if not no_both and not yes_both:
            raise ValidationError({'product': 'must have both'})
        return data

class MaterialInlineForm(forms.Form):
    material = forms.ModelChoiceField(Material.objects)
    material_quantity = forms.IntegerField()

    def clean(self):
        data = super().clean()
        no_both = not data.get('material') and not data.get('material_quantity')
        yes_both = data.get('material') and data.get('material_quantity')
        if not no_both and not yes_both:
            raise ValidationError({'material': 'must have both'})
        # check if material stock
        if data['material'].stock < data['material_quantity']:
            raise ValidationError({'material_quantity': 'not enough stock'})
        return data