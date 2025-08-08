from django import forms
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