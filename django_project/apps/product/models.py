from django.db import models
from django.utils import timezone
from apps.core.models import add_pending_money, fulfill_money

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="$")
    unit = models.CharField(max_length=255)
    stock = models.IntegerField(default=0, editable=False)
    pending_stock = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return f"{self.name} (${self.price}/{self.unit})"
    
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

class Buyer(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    content = models.JSONField(editable=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False)
    created_on = models.DateField(auto_now_add=True, editable=False)
    paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True, editable=False)
    fulfilled = models.BooleanField(default=False)
    fulfilled_on = models.DateField(null=True, blank=True, editable=False)

    final_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="$", editable=False)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="$")

    def save(self, *args, **kwargs):
        if not self.pk: # make changes only during creation
            # deduct the stock and calculate the price
            for product_name, quantity in self.content.items():
                product = Product.objects.get(name=product_name)
                product.add_pending_stock(quantity)
                self.final_price += product.price * quantity
            self.final_price -= self.discount
            add_pending_money(self.final_price)
            
        if self.paid and not self.paid_on:
            self.paid_on = timezone.now().date()
            fulfill_money(self.final_price)
        elif not self.paid and self.paid_on:
            raise ValueError("cannot change from paid to unpaid")

        if self.fulfilled and not self.fulfilled_on:
            self.fulfilled_on = timezone.now().date()
            for product_name, quantity in self.content.items():
                product = Product.objects.filter(name=product_name).first()
                if not product:
                    continue
                product.fulfill_stock(quantity)
        elif not self.fulfilled and self.fulfilled_on:
            raise ValueError("cannot change from fulfilled to unfulfilled")
                
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        cancelling the order
        """
        if not self.fulfilled: # remove the staging diff stock
            for product_name, quantity in self.content.items():
                product = Product.objects.filter(name=product_name).first()
                if not product:
                    continue
                product.add_pending_stock(-quantity)

        if not self.paid: # rm the pending money
            add_pending_money(-self.final_price)

        super().delete(*args, **kwargs)
    
    