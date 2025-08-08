from datetime import timedelta
from django.utils import timezone
from apps.material.models import Purchase
from apps.product.models import Order
from apps.process.models import ManufacturingLog

def delete_expired_logs():
    expiration_date = timezone.now() - timedelta(days=30)
    Purchase.objects.filter(created_on__lt=expiration_date, paid=True, fulfilled=True).delete()
    Order.objects.filter(created_on__lt=expiration_date, paid=True, fulfilled=True).delete()
    ManufacturingLog.objects.filter(created_on__lt=expiration_date).delete(revert_stock=False)