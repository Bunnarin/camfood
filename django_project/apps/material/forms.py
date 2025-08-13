from django import forms
from .models import PurchaseItem

class PurchaseInlineForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = '__all__'

    def clean(self):
        data = super().clean()
        # if no subtotal is entered, then calculate it
        if not data.get('subtotal'):
            data['subtotal'] = data['quantity'] * data['material'].price
        return data