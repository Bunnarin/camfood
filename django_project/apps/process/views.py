from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseDeleteView
from apps.material.forms import PurchaseInlineForm
from .models import ManufacturingLog
from .forms import OrderInlineForm

class ManufacturingLogListView(BaseListView):
    model = ManufacturingLog
    table_fields = ['created_on', 'material', 'product', 'comment']
    object_actions = [
        ('delete', 'process:delete_manufacturinglog', None),
    ]
    actions = [
        ('create', 'process:add_manufacturinglog', None),
    ]

class ManufacturingLogCreateView(BaseCreateView):
    model = ManufacturingLog
    fields = ['comment']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formsets'] = [
            formset_factory(PurchaseInlineForm, extra=4)(self.request.POST or None),
            formset_factory(OrderInlineForm, extra=4)(self.request.POST or None),
            ]
        return context
    
    def form_valid(self, form):
        material_formset = formset_factory(PurchaseInlineForm)(self.request.POST)
        product_formset = formset_factory(OrderInlineForm)(self.request.POST)
        if not material_formset.is_valid() or not product_formset.is_valid():
            return super().form_invalid(form)

        material = {}
        for item in material_formset.cleaned_data:
            try: material[item['material'].name] = item['quantity']
            except: break
        form.instance.material = material

        product = {}
        for item in product_formset.cleaned_data:
            try: product[item['product'].name] = item['quantity']
            except: break
        form.instance.product = product

        return super().form_valid(form)

class ManufacturingLogDeleteView(BaseDeleteView):
    model = ManufacturingLog