from datetime import timedelta
from django.utils import timezone
from apps.material.models import Purchase, Adjustment as MaterialAdjustment
from apps.product.models import Order, Adjustment as ProductAdjustment
from apps.process.models import ManufacturingLog
from .models import Transaction

def delete_expired_logs():
    expiration_date = timezone.now() - timedelta(days=30)
    Purchase.objects.filter(created_on__lt=expiration_date, paid=True, fulfilled=True).delete()
    Order.objects.filter(created_on__lt=expiration_date, paid=True, fulfilled=True).delete()
    MaterialAdjustment.objects.filter(created_on__lt=expiration_date).delete()
    ProductAdjustment.objects.filter(created_on__lt=expiration_date).delete()
    ManufacturingLog.objects.filter(created_on__lt=expiration_date).delete(revert_stock=False)
    Transaction.objects.filter(created_on__lt=expiration_date).delete(revert=True)