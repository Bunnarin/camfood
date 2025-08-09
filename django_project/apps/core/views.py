from apps.core.generic_views import BaseListView, BaseCreateView, BaseDeleteView
from apps.core.models import Money, Transaction

class MoneyView(BaseListView):
    model = Money
    template_name = 'core/generic_detail.html'

    def get_queryset(self):
        return Money.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        money = Money.objects.first()
        context['object_dict'] = {
            'Amount': money.amount,
            'Pending Amount': money.pending_amount,
            'Debt': money.debt,
        }
        context['title'] = 'Money'
        return context

class TransactionListView(BaseListView):
    model = Transaction
    table_fields = ['created_on', 'created_by', 'amount', 'comment']
    actions = [('create', 'core:add_transaction', None)]
    object_actions = [('delete', 'core:delete_transaction', None)]

class TransactionCreateView(BaseCreateView):
    model = Transaction
    fields = '__all__'

class TransactionDeleteView(BaseDeleteView):
    model = Transaction
