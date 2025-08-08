from django import forms
from apps.product.models import Product

class OrderInlineForm(forms.Form):
    """
    to be used in a formset (forked from the original bcuz I don't want its clean method here)
    """
    product = forms.ModelChoiceField(Product.objects)
    quantity = forms.IntegerField()