from apps.core.generic_views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseImportView, BaseInlineCreateView, BaseDetailView
from .models import Order, Product, Adjustment, Buyer, OrderItem
from .forms import OrderInlineForm

class BuyerListView(BaseListView):
    model = Buyer
    table_fields = ['name', 'contact', 'location']
    object_actions = [('✏️', 'product:change_buyer', None), ('❌', 'product:delete_buyer', None)]
    actions = [('+', 'product:add_buyer', None)]

class BuyerDetailView(BaseDetailView):
    model = Buyer
    fields = ['name', 'contact', 'location']

class BuyerCreateView(BaseCreateView):
    model = Buyer
    fields = '__all__'

class BuyerUpdateView(BaseUpdateView):
    model = Buyer
    fields = ['name', 'contact', 'location']

class BuyerDeleteView(BaseDeleteView):
    model = Buyer

class OrderListView(BaseListView):
    model = Order
    table_fields = ['created_by', 'created_on', 'paid', 'paid_on', 'done', 'done_on', 'total_price', 'buyer', 'comment', 'items']
    object_actions = [
        ('🖨️', 'product:print_order', 'product.view_order'), 
        ('ℹ️', 'product:detail_order', 'product.view_order'),
        ('✏️', 'product:change_order', None), 
        ('❌', 'product:delete_order', None)
    ]
    actions = [('+', 'product:add_order', None)]

class OrderDetailView(BaseListView):
    model = OrderItem
    table_fields = ['product', 'quantity', 'subtotal', 'mfg']

    def get_queryset(self):
        return super().get_queryset().filter(order_id=self.kwargs['pk'])

class OrderPrintView(BaseListView):
    model = OrderItem
    template_name = 'product/invoice.html'
    table_fields = ['product.name', 'quantity', 'subtotal']

    def get_queryset(self):
        return super().get_queryset().filter(order_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context.update({
            'id': order.id,
            'created_by': order.created_by,
            'created_on': order.created_on,
            'total_price': order.total_price,
            'buyer': order.buyer,
        })
        return context

class OrderCreateView(BaseInlineCreateView):
    model = Order
    inline_model = OrderItem
    fields = '__all__'
    inline_form_class = OrderInlineForm

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        # aggreagate price from the formset
        if not formset.is_valid():
            return self.form_invalid(form)
        # filter out empty form
        for itemform in formset:
            if not itemform.cleaned_data.get('subtotal'):
                break
            form.instance.total_price += itemform.cleaned_data['subtotal']
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
        ('✏️', 'product:change_product', None),
        ('❌', 'product:delete_product', None),
    ]
    actions = [
        ('+', 'product:add_product', None),
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
    fields = ['name', 'code', 'stock', 'price', 'unit']

class AdjustmentListView(BaseListView):
    model = Adjustment
    table_fields = ['created_by', 'created_on', 'quantity', 'comment', 'product']
    object_actions = [('❌', 'product:delete_adjustment', None)]
    actions = [('+', 'product:add_adjustment', None)]


class AdjustmentCreateView(BaseCreateView):
    model = Adjustment
    fields = '__all__'

class AdjustmentDeleteView(BaseDeleteView):
    model = Adjustment