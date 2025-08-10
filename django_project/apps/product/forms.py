from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Order, Product, Buyer

class OrderForm(forms.ModelForm):
    new_buyer = forms.CharField(required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buyer'].required = False
    
    def clean(self):
        data = super().clean()
        if not data.get('buyer') and not data.get('new_buyer'):
            self.add_error('buyer', 'either select the buyer or fill the new_buyer')
        if not data.get('buyer'):
            data['buyer'], _ = Buyer.objects.get_or_create(name=data['new_buyer'])
        return data

class OrderInlineForm(forms.Form):
    """
    to be used in a formset
    """
    product = forms.ModelChoiceField(Product.objects)
    quantity = forms.IntegerField()
    price = forms.IntegerField(required=False)
    mfg = forms.DateField(required=False)

    def clean(self):
        data = super().clean()

        # ensure that the manufactured_on date is not in the future
        if data.get('mfg') and data['mfg'] > timezone.now().date():
            raise ValidationError({'mfg': 'ថ្ងៃផលិតខុស'})

        if not data.get('product'):
            raise ValidationError({'product': 'invalid'})
        
        if not data.get('quantity'):
            raise ValidationError({'quantity': 'invalid'})

        # check if in stock
        current_stock = data['product'].stock
        if current_stock < data['quantity']:
            raise ValidationError({'quantity': f'not enough stock (នៅសល់ {current_stock})'})
        
        # if price is not provided, calculate
        if not data.get('price'):
            data['price'] = data['product'].price * data['quantity']

        return data