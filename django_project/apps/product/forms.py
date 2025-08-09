from django import forms
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

    def clean(self):
        data = super().clean()

        no_both = not data.get('product') and not data.get('quantity')
        yes_both = data.get('product') and data.get('quantity')
        if not no_both and not yes_both:
            raise ValidationError('product', 'must have both')

        # check if in stock
        if data['product'].stock < data['quantity']:
            self.add_error('quantity', 'not enough stock')

        return data