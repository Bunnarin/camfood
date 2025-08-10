from types import SimpleNamespace as obj
from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseImportView
from .models import Purchase, Material, Adjustment, Supplier
from .forms import PurchaseInlineForm

class SupplierListView(BaseListView):
    model = Supplier
    table_fields = ['name', 'contact']
    object_actions = [
        ('✏️', 'material:change_supplier', None),
        ('❌', 'material:delete_supplier', None),
    ]
    actions = [
        ('+', 'material:add_supplier', None),
    ]

class SupplierCreateView(BaseCreateView):
    model = Supplier
    fields = '__all__'

class SupplierUpdateView(BaseUpdateView):
    model = Supplier
    fields = '__all__'

class SupplierDeleteView(BaseDeleteView):
    model = Supplier

class PurchaseListView(BaseListView):
    model = Purchase
    table_fields = ['created_by', 'created_on', 'paid', 'paid_on', 'done', 'done_on', 'price', 'supplier', 'content', 'comment']
    object_actions = [
        ('✏️', 'material:change_purchase', None),
        ('❌', 'material:delete_purchase', None),
        ('view', 'material:detail_purchase', 'material.view_purchase'),
    ]
    actions = [
        ('+', 'material:add_purchase', None),
    ]

class PurchaseDetailView(BaseListView):
    model = Purchase
    template_name = 'product/invoice.html'
    def get_context_data(self, **kwargs):
        purchase = Purchase.objects.get(pk=self.kwargs['pk'])
        context = {
            'object_dict': {
                'id': purchase.id,
                'created_by': purchase.supplier,
                'created_on': purchase.created_on,
                'price': purchase.price,
                'buyer': purchase.created_by,
            },
            'object_list': [obj(name=name, quantity=quantity, price="៛ "+str(price)) for name, (quantity, price) in purchase.content.items()],
            'table_fields': ['name', 'quantity', 'price']
        }
        return context

class PurchaseCreateView(BaseCreateView):
    model = Purchase
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = formset_factory(PurchaseInlineForm)
        return context
    
    def form_valid(self, form):
        formset = formset_factory(PurchaseInlineForm)(self.request.POST)
        if not formset.is_valid():
            return super().form_invalid(form)
        content = {} 
        for item in formset.cleaned_data:
            content[item['material'].name] = (item['quantity'], item['price'])
        form.instance.content = content
        return super().form_valid(form)

class PurchaseUpdateView(BaseUpdateView):
    model = Purchase
    fields = ['paid', 'done']

class PurchaseDeleteView(BaseDeleteView):
    model = Purchase

class MaterialListView(BaseListView):
    model = Material
    table_fields = ['name', 'stock', 'pending_stock', 'price', 'unit']
    object_actions = [
        ('✏️', 'material:change_material', None),
        ('❌', 'material:delete_material', None),
    ]
    actions = [
        ('+', 'material:add_material', None),
        ('import', 'material:import_material', 'material:add_material'),
    ]

class MaterialCreateView(BaseCreateView):
    model = Material
    fields = '__all__'

class MaterialUpdateView(BaseUpdateView):
    model = Material
    fields = ['code', 'price', 'unit']

class MaterialDeleteView(BaseDeleteView):
    model = Material

class MaterialImportView(BaseImportView):
    model = Material

class AdjustmentListView(BaseListView):
    model = Adjustment
    table_fields = ['created_by', 'created_on', 'quantity', 'comment', 'product']
    object_actions = [
        ('❌', 'material:delete_adjustment', None),
    ]
    actions = [
        ('+', 'material:add_adjustment', None),
    ]


class AdjustmentCreateView(BaseCreateView):
    model = Adjustment
    fields = '__all__'

class AdjustmentDeleteView(BaseDeleteView):
    model = Adjustment
