from django.db import models
from django.utils import timezone
from django.urls import reverse
from apps.core.models import add_pending_money, fulfill_money

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=4, unique=True)
    price = models.IntegerField(help_text="riel")
    unit = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    pending_stock = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'ស្តុកផលិតផល'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.code} {self.name} ({self.price}៛/{self.unit})"
    
    def add_stock(self, amount):
        self.stock += amount
        self.save()
    
    def add_pending_stock(self, amount):
        self.pending_stock += amount
        self.stock -= amount
        self.save()
    
    def fulfill_stock(self, amount):
        self.pending_stock -= amount
        self.save()

class Adjustment(models.Model):
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False, related_name='product_adjustments')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(help_text="ថែម, ដាក់ - ពីមុខដើម្បីថយ")
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'ថែមថយស្តុកផលិតផល'
        verbose_name_plural = verbose_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.product.add_stock(self.quantity)
        super().save(*args, **kwargs)
    
    def delete(self, *args, revert=True, **kwargs):
        if revert:
            self.product.add_stock(-self.quantity)
        super().delete(*args, **kwargs)

class Buyer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'អតិថិជន'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product:detail_buyer', kwargs={'pk': self.pk})

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False)
    created_on = models.DateField(auto_now_add=True, editable=False)
    paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True, editable=False)
    done = models.BooleanField(default=False)
    done_on = models.DateField(null=True, blank=True, editable=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    total_price = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'បុងលក់ចេញ'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs): 
        if not self.pk:
            add_pending_money(self.total_price)
                   
        if self.done and not self.done_on:
            self.done_on = timezone.now().date()
            for item in self.items.all():
                item.fulfill_stock()
        elif not self.done and self.done_on:
            raise ValueError("cannot change from done to undone")
        
        if self.paid and not self.paid_on:
            self.paid_on = timezone.now().date()
            fulfill_money(self.total_price)
        elif not self.paid and self.paid_on:
            raise ValueError("cannot change from paid to unpaid")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if not self.paid: #rm the pending profit
            add_pending_money(-self.total_price)
        if not self.done: #rm the pending stock
            for item in self.items.all():
                item.product.add_pending_stock(-item.quantity)
        super().delete(*args, **kwargs)

class OrderItem(models.Model):
    """
    inline model
    """
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    mfg = models.DateField(null=True, blank=True)
    subtotal = models.IntegerField(blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return f"{self.product.code}: {self.quantity}"

    def save(self, *args, **kwargs):
        creation = not self.pk
        if creation: # add to the pending stock
            self.product.add_pending_stock(self.quantity)
        super().save(*args, **kwargs)
    
    def fulfill_stock(self):
        """
        to be called by its order
        """
        self.product.fulfill_stock(self.quantity)

    
    