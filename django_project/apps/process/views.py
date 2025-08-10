from types import SimpleNamespace as obj
from django.urls import reverse_lazy
from extra_views import FormSetView
from apps.core.generic_views import BaseListView, BaseCreateView, BaseDeleteView, PermissionRequiredMixin
from apps.material.forms import PurchaseInlineForm
from apps.material.models import Material
from .models import ManufacturingLog, Formula

class FormulaListView(BaseListView):
    model = Formula
    table_fields = ['product', 'expected_quantity']
    pretty_json_field = 'materials'
    object_actions = [
        ('✏️', 'process:change_formula', None), 
        ('❌', 'process:delete_formula', None),
        ('view', 'process:detail_formula', 'process.view_formula')
        ]
    actions = [('+', 'process:add_formula', None)]

class FormulaDetailView(BaseListView):
    model = Formula

    def get_context_data(self, **kwargs):
        formula = Formula.objects.get(pk=self.kwargs['pk'])
        context = {
            'object_list': [obj(name=name, quantity=quantity) for name, quantity in formula.materials.items()],
            'table_fields': ['name', 'quantity']
        }
        return context

class FormulaCreateView(BaseCreateView):
    model = Formula
    fields = '__all__'

class FormulaUpdateView(PermissionRequiredMixin, FormSetView):
    model = Formula
    form_class = PurchaseInlineForm
    template_name = 'core/generic_form.html'
    permission_required = 'process.change_formula'
    success_url = reverse_lazy('process:view_formula')
    
    def get_initial(self):
        self.formula = Formula.objects.get(pk=self.kwargs['pk'])
        initials = []
        for name, quantity in self.formula.materials.items():
            initials.append({'material': Material.objects.get(name=name), 'quantity': quantity})
        return initials
    
    def formset_valid(self, formset):
        if not formset.is_valid():
            return super().formset_invalid(formset)
        materials = {}
        for item in formset.cleaned_data:
            try: materials[item['material'].name] = item['quantity']
            except: break
        self.formula.materials = materials
        self.formula.save()
        return super().formset_valid(formset)

class FormulaDeleteView(BaseDeleteView):
    model = Formula

class ManufacturingLogListView(BaseListView):
    model = ManufacturingLog
    table_fields = ['created_on', 'formula', 'final_quantity', 'comment']
    object_actions = [('❌', 'process:delete_manufacturinglog', None)]
    actions = [('+', 'process:add_manufacturinglog', None)]

class ManufacturingLogCreateView(BaseCreateView):
    model = ManufacturingLog
    fields = '__all__'
    
class ManufacturingLogDeleteView(BaseDeleteView):
    model = ManufacturingLog