from django.forms import formset_factory
from apps.core.generic_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
from .models import Order, Product
from .forms import OrderForm, OrderInlineForm

class OrderListView(BaseListView):
    model = Order
    table_fields = ['created_by', 'created_on', 'paid', 'paid_on', 'fulfilled', 'fulfilled_on', 'price', 'buyer', 'content', 'comment']
    object_actions = [
        ('edit', 'product:change_order', None),
        ('delete', 'product:delete_order', None),
    ]
    actions = [
        ('create', 'product:add_order', None),
    ]

class OrderCreateView(BaseCreateView):
    model = Order
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = formset_factory(OrderInlineForm, extra=4)(self.request.POST or None)
        return context
    
    def form_valid(self, form):
        formset = formset_factory(OrderInlineForm)(self.request.POST)
        if not formset.is_valid():
            return super().form_invalid(form)
        content = {}
        for item in formset.cleaned_data:
            try: content[item['product'].name] = item['quantity']
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
    table_fields = ['name', 'stock', 'pending_stock', 'price', 'unit']
    object_actions = [
        ('edit', 'product:change_product', None),
        ('delete', 'product:delete_product', None),
    ]
    actions = [
        ('create', 'product:add_product', None),
    ]

class ProductCreateView(BaseCreateView):
    model = Product
    fields = '__all__'

class ProductUpdateView(BaseUpdateView):
    model = Product
    fields = '__all__'

class ProductDeleteView(BaseDeleteView):
    model = Product
