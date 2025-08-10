from django import forms
from django.core.exceptions import ValidationError
from .models import Material, Purchase, Supplier

class PurchaseForm(forms.ModelForm):
    new_supplier = forms.CharField(required=False)
    class Meta:
        model = Purchase
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].required = False
    
    def clean(self):
        data = super().clean()
        if not data.get('supplier') and not data.get('new_supplier'):
            self.add_error('supplier', 'either select the supplier or fill the new_supplier')
        if not data.get('supplier'):
            data['supplier'] = Supplier.objects.create(name=data['new_supplier'])
        return data

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