from apps.core.generic_views import BaseListView, BaseCreateView, BaseDeleteView
from apps.core.models import Money, Transaction

class TransactionListView(BaseListView):
    model = Transaction
    table_fields = ['created_on', 'created_by', 'amount', 'comment']
    actions = [('+', 'core:add_transaction', None)]
    object_actions = [('❌', 'core:delete_transaction', None)]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'fields': ['amount', 'pending_amount', 'debt'],
            'object': Money.objects.first(),
        })
        return context

class TransactionCreateView(BaseCreateView):
    model = Transaction
    fields = '__all__'

class TransactionDeleteView(BaseDeleteView):
    model = Transaction
