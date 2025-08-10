from types import SimpleNamespace as obj
from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseImportView
from .models import Order, Product, Adjustment
from .forms import OrderForm, OrderInlineForm

class OrderListView(BaseListView):
    model = Order
    table_fields = ['created_by', 'created_on', 'paid', 'paid_on', 'done', 'done_on', 'price', 'buyer', 'comment']
    pretty_json_field = 'content'
    object_actions = [
        ('print', 'product:detail_order', 'product.view_order'),
        ('edit', 'product:change_order', None),
        ('delete', 'product:delete_order', None),
    ]
    actions = [
        ('create', 'product:add_order', None),
    ]

class OrderDetailView(BaseListView):
    model = Order
    template_name = 'product/invoice.html'

    def get_context_data(self, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        context = {
            'object_dict': {
                'id': order.id,
                'created_by': order.created_by,
                'created_on': order.created_on,
                'price': order.price,
                'buyer': order.buyer,
            },
            'object_list': [obj(code=code, quantity=quantity, price="៛ "+str(price)) for code, (quantity, _, price) in order.content.items()],
            'table_fields': ['code', 'quantity', 'price']
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
        for item in formset.cleaned_data:
            # convert cleaned_data into into the model json
            content[item['product'].code] = (item['quantity'], str(item['mfg'] or ""), item['price'])
        form.instance.content = content
        form.instance.price = sum(item['price'] * item['quantity'] for item in formset.cleaned_data)
        return super().form_valid(form)

class OrderUpdateView(BaseUpdateView):
    model = Order
    fields = ['paid', 'done']

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