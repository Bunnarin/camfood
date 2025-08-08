from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Purchase, Material
from .forms import PurchaseForm, PurchaseInlineForm

class PurchaseListView(BaseListView):
    model = Purchase
    table_fields = ['created_by', 'created_on', 'paid', 'paid_on', 'fulfilled', 'fulfilled_on', 'discount', 'final_price', 'supplier', 'content', 'comment']
    object_actions = [
        ('edit', 'material:change_purchase', None),
        ('delete', 'material:delete_purchase', None),
    ]
    actions = [
        ('create', 'material:add_purchase', None),
    ]

class PurchaseCreateView(BaseCreateView):
    model = Purchase
    form_class = PurchaseForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = formset_factory(PurchaseInlineForm, extra=4)
        return context
    
    def form_valid(self, form):
        formset = formset_factory(PurchaseInlineForm)(self.request.POST)
        if not formset.is_valid():
            return super().form_invalid(form)
        content = {}
        for item in formset.cleaned_data:
            try: content[item['material'].name] = item['quantity']
            except: break
        form.instance.content = content
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PurchaseUpdateView(BaseUpdateView):
    model = Purchase
    fields = ['paid', 'fulfilled']

class PurchaseDeleteView(BaseDeleteView):
    model = Purchase

class MaterialListView(BaseListView):
    model = Material
    table_fields = ['name', 'stock', 'pending_stock', 'price', 'unit']
    object_actions = [
        ('edit', 'material:change_material', None),
        ('delete', 'material:delete_material', None),
    ]
    actions = [
        ('create', 'material:add_material', None),
    ]

class MaterialCreateView(BaseCreateView):
    model = Material
    fields = '__all__'

class MaterialUpdateView(BaseUpdateView):
    model = Material
    fields = '__all__'

class MaterialDeleteView(BaseDeleteView):
    model = Material
