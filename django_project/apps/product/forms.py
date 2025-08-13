from django import forms
from .models import OrderItem

class OrderInlineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
    def clean(self):
        data = super().clean()
        # ensure that the quantity is greater than the stock
        if data['quantity'] > data['product'].stock:
            self.add_error('quantity', f"ខ្វះស្តុក(នៅសល់ {data['product'].stock})")
        # if no subtotal is entered, then calculate it
        if not data.get('subtotal'):
            data['subtotal'] = data['quantity'] * data['product'].price
        return data