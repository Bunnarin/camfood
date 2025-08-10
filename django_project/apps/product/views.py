from types import SimpleNamespace as obj
from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseImportView
from .models import Order, Product, Adjustment
from .forms import OrderForm, OrderInlineForm

class OrderListView(BaseListView):
    model = Order
    table_fields = ['created_by', 'created_on', 'paid', 'paid_on', 'fulfilled', 'fulfilled_on', 'price', 'buyer', 'comment']
    pretty_json_field = 'content'
    object_actions = [
        ('view', 'product:detail_order', 'product.view_order'),
        ('edit', 'product:change_order', None),
        ('delete', 'product:delete_order', None),
    ]
    actions = [
        ('create', 'product:add_order', None),
    ]

class OrderDetailView(BaseListView):
    model = Order

    def get_context_data(self, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        context = {
            'object_list': [obj(code=code, quantity=quantity, mfg=mfg) for code, (quantity, mfg) in order.content.items()],
            'table_fields': ['code', 'quantity', 'mfg']
        }
        return context

class OrderCreateView(BaseCreateView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = formset_factory(OrderInlineForm)(self.request.POST or None)
        return context
    
    def form_valid(self, form):
        formset = formset_factory(OrderInlineForm)(self.request.POST)
        if not formset.is_valid():
            return super().form_invalid(form)
        content = {}
        print(formset.cleaned_data)
        for item in formset.cleaned_data:
            try: 
                content[item['product'].code] = (item['quantity'], str(item['mfg'] or ""))
            except: break
        form.instance.content = content
        return super().form_valid(form)

class OrderUpdateView(BaseUpdateView):
    model = Order
    fields = ['paid', 'fulfilled']

class OrderDeleteView(BaseDeleteView):
    model = Order

class ProductListView(BaseListView):
    model = Product
    table_fields = ['name', 'code', 'stock', 'pending_stock', 'price', 'unit']
    object_actions = [
        ('edit', 'product:change_product', None),
        ('delete', 'product:delete_product', None),
    ]
    actions = [
        ('create', 'product:add_product', None),
        ('import', 'product:import_product', 'product.add_product'),
    ]

class ProductCreateView(BaseCreateView):
    model = Product
    fields = '__all__'

class ProductUpdateView(BaseUpdateView):
    model = Product
    fields = ['code', 'price', 'unit']

class ProductDeleteView(BaseDeleteView):
    model = Product

class ProductImportView(BaseImportView):
    model = Product
    fields = ['name', 'code', 'price', 'unit']

class AdjustmentListView(BaseListView):
    model = Adjustment
    table_fields = ['created_by', 'created_on', 'quantity', 'comment', 'product']
    object_actions = [
        ('delete', 'product:delete_adjustment', None),
    ]
    actions = [
        ('create', 'product:add_adjustment', None),
    ]


class AdjustmentCreateView(BaseCreateView):
    model = Adjustment
    fields = '__all__'

class AdjustmentDeleteView(BaseDeleteView):
    model = Adjustment