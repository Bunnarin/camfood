from extra_views import InlineFormSetView
from apps.core.generic_views import BaseListView, BaseCreateView, BaseDeleteView, BaseUpdateView, BaseInlineCreateView
from .models import ManufacturingLog, Formula, FormulaItem

class FormulaListView(BaseListView):
    model = Formula
    table_fields = ['product', 'expected_quantity']
    object_actions = [
        ('✏️', 'process:change_formula', None), 
        ('ℹ️', 'process:detail_formula', 'process:view_formula'),
        ('❌', 'process:delete_formula', None)
        ]
    actions = [('+', 'process:add_formula', None)]

class FormulaDetailView(BaseListView):
    model = FormulaItem
    table_fields = ['material', 'quantity']

    def get_queryset(self):
        return super().get_queryset().filter(formula=self.kwargs['pk'])

class FormulaCreateView(BaseInlineCreateView):
    model = Formula
    inline_model = FormulaItem
    fields = '__all__'
    inline_fields = '__all__'

class FormulaUpdateView(InlineFormSetView, BaseUpdateView):
    model = Formula
    inline_model = FormulaItem

class FormulaDeleteView(BaseDeleteView):
    model = Formula

class ManufacturingLogListView(BaseListView):
    model = ManufacturingLog
    table_fields = ['created_on', 'formula', 'final_quantity', 'comment', 'items']
    object_actions = [('❌', 'process:delete_manufacturinglog', None)]
    actions = [('+', 'process:add_manufacturinglog', None)]

class ManufacturingLogCreateView(BaseCreateView):
    model = ManufacturingLog
    fields = '__all__'
    
class ManufacturingLogDeleteView(BaseDeleteView):
    model = ManufacturingLog