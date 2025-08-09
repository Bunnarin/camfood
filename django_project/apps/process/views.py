from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseDeleteView, BaseUpdateView, BaseSelectView
from apps.material.forms import PurchaseInlineForm
from apps.material.models import Material
from .models import ManufacturingLog, Formula

class FormulaListView(BaseListView):
    model = Formula
    table_fields = ['product', 'expected_quantity']
    pretty_json_field = 'materials'

    object_actions = [('edit', 'process:change_formula', None), 
    ('delete', 'process:delete_formula', None)]
    actions = [('create', 'process:add_formula', None)]

class FormulaCreateView(BaseCreateView):
    model = Formula
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = formset_factory(PurchaseInlineForm, extra=10)(self.request.POST or None)
        return context
    
    def form_valid(self, form):
        formset = formset_factory(PurchaseInlineForm, extra=10)(self.request.POST or None)
        materials = {}
        for item in formset.cleaned_data:
            try: materials[item['material'].name] = item['quantity']
            except: break
        form.instance.materials = materials
        return super().form_valid(form)

class FormulaUpdateView(FormulaCreateView, BaseUpdateView):
    model = Formula
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # get the initials
        initials = []
        for material_name, quantity in self.object.materials.items():
            material = Material.objects.filter(name=material_name).first()
            if not material:
                continue
            initials.append({'material': material, 'quantity': quantity})

        context = super(BaseUpdateView, self).get_context_data(**kwargs)
        context['formset'] = formset_factory(PurchaseInlineForm, initals=initials, extra=3)(self.request.POST or None)
        return context

class FormulaDeleteView(BaseDeleteView):
    model = Formula

class ManufacturingLogListView(BaseListView):
    model = ManufacturingLog
    table_fields = ['created_on', 'formula', 'final_quantity', 'comment']
    object_actions = [('delete', 'process:delete_manufacturinglog', None)]
    actions = [('create', 'process:add_manufacturinglog', None)]

class ManufacturingLogCreateView(BaseCreateView):
    model = ManufacturingLog
    fields = '__all__'
    
class ManufacturingLogDeleteView(BaseDeleteView):
    model = ManufacturingLog