from apps.core.generic_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseImportView, BaseInlineCreateView, BaseDetailView
from .models import Purchase, Material, Adjustment, Supplier, PurchaseItem
from .forms import PurchaseInlineForm

class SupplierListView(BaseListView):
    model = Supplier
    table_fields = ['name', 'contact']
    object_actions = [('✏️', 'material:change_supplier', None), ('❌', 'material:delete_supplier', None)]
    actions = [('+', 'material:add_supplier', None)]

class SupplierDetailView(BaseDetailView):
    model = Supplier
    fields = ['name', 'contact']

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
    table_fields = ['created_by', 'created_on', 'paid', 'paid_on', 'done', 'done_on', 'total_price', 'supplier', 'comment', 'items']
    object_actions = [
        ('✏️', 'material:change_purchase', None), 
        ('ℹ️', 'material:detail_purchase', 'material.view_purchase'),
        ('❌', 'material:delete_purchase', None)
        ]
    actions = [('+', 'material:add_purchase', None)]

class PurchaseDetailView(BaseListView):
    model = PurchaseItem
    table_fields = ['material', 'quantity', 'subtotal']

    def get_queryset(self):
        return super().get_queryset().filter(purchase=self.kwargs['pk'])

class PurchaseCreateView(BaseInlineCreateView):
    model = Purchase
    fields = '__all__'
    inline_model = PurchaseItem
    inline_form_class = PurchaseInlineForm

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if not formset.is_valid():
            return self.form_invalid(form)
        # filter out empty form
        for itemform in formset:
            if not itemform.cleaned_data.get('subtotal'):
                break
            form.instance.total_price += itemform.cleaned_data['subtotal']
        return super().form_valid(form)

class PurchaseUpdateView(BaseUpdateView):
    model = Purchase
    fields = ['paid', 'done']

class PurchaseDeleteView(BaseDeleteView):
    model = Purchase

class MaterialListView(BaseListView):
    model = Material
    table_fields = ['name', 'stock', 'pending_stock', 'price', 'unit']
    object_actions = [('✏️', 'material:change_material', None), ('❌', 'material:delete_material', None)]
    actions = [('+', 'material:add_material', None), ('import', 'material:import_material', 'material:add_material')]

class MaterialCreateView(BaseCreateView):
    model = Material
    fields = '__all__'

class MaterialUpdateView(BaseUpdateView):
    model = Material
    fields = ['code', 'total_price', 'unit']

class MaterialDeleteView(BaseDeleteView):
    model = Material

class MaterialImportView(BaseImportView):
    model = Material

class AdjustmentListView(BaseListView):
    model = Adjustment
    table_fields = ['created_by', 'created_on', 'quantity', 'comment', 'product']
    object_actions = [('❌', 'material:delete_adjustment', None)]
    actions = [('+', 'material:add_adjustment', None)]

class AdjustmentCreateView(BaseCreateView):
    model = Adjustment
    fields = '__all__'

class AdjustmentDeleteView(BaseDeleteView):
    model = Adjustment
