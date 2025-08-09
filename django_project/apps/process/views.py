from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseDeleteView
from .models import ManufacturingLog
from .forms import MaterialInlineForm, ProductInlineForm

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
            formset_factory(MaterialInlineForm, extra=4)(self.request.POST or None),
            formset_factory(ProductInlineForm, extra=4)(self.request.POST or None),
            ]
        return context
    
    def form_valid(self, form):
        material_formset = formset_factory(MaterialInlineForm, extra=4)(self.request.POST)
        product_formset = formset_factory(ProductInlineForm, extra=4)(self.request.POST)
        if not material_formset.is_valid() or not product_formset.is_valid():
            return super().form_invalid(form)

        materials = {}
        for item in material_formset.cleaned_data:
            try: materials[item['material'].name] = item['material_quantity']
            except: break
        form.instance.material = materials

        products = {}
        for item in product_formset.cleaned_data:
            try: products[item['product'].name] = item['product_quantity']
            except: break
        form.instance.product = products

        return super().form_valid(form)

class ManufacturingLogDeleteView(BaseDeleteView):
    model = ManufacturingLog