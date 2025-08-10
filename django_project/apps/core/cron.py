from datetime import timedelta
from django.utils import timezone
from apps.material.models import Purchase, Adjustment as MaterialAdjustment
from apps.product.models import Order, Adjustment as ProductAdjustment
from apps.process.models import ManufacturingLog
from .models import Transaction

def delete_expired_logs():
    expiration_date = timezone.now() - timedelta(days=30)
    Purchase.objects.filter(created_on__lt=expiration_date, paid=True, done=True).delete()
    Order.objects.filter(created_on__lt=expiration_date, paid=True, done=True).delete()
    # revert false because we only clear up these transaction, and we dont want to revert the stock
    MaterialAdjustment.objects.filter(created_on__lt=expiration_date).delete(revert=False)
    ProductAdjustment.objects.filter(created_on__lt=expiration_date).delete(revert=False)
    ManufacturingLog.objects.filter(created_on__lt=expiration_date).delete(revert=False)
    Transaction.objects.filter(created_on__lt=expiration_date).delete(revert=False)