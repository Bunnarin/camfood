from django.db import models
from django.utils import timezone
from apps.core.models import add_debt, fulfill_debt

class Material(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="in USD")
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
        self.save()
    
    def fulfill_stock(self, amount):
        self.pending_stock -= amount
        self.stock += amount
        self.save()

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    content = models.JSONField(editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    comment = models.CharField(max_length=255, null=True, blank=True)

    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False)
    created_on = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True, editable=False)
    fulfilled = models.BooleanField(default=False)
    fulfilled_on = models.DateField(null=True, blank=True, editable=False)

    final_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="$", editable=False)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="$")

    def save(self, *args, **kwargs):
        if not self.pk: # make changes only during creation
            # deduct the stock and calculate the price
            for material_name, quantity in self.content.items():
                material = Material.objects.get(name=material_name)
                material.add_pending_stock(quantity)
                self.final_price += material.price * quantity
            self.final_price -= self.discount
            add_debt(self.final_price)
            
        if self.paid and not self.paid_on:
            self.paid_on = timezone.now().date()
            fulfill_debt(self.final_price)
        elif not self.paid and self.paid_on:
            raise ValueError("cannot change from paid to unpaid")

        if self.fulfilled and not self.fulfilled_on:
            self.fulfilled_on = timezone.now().date()
            for material_name, quantity in self.content.items():
                material = Material.objects.filter(name=material_name).first()
                if not material:
                    continue
                material.fulfill_stock(quantity)
        elif not self.fulfilled and self.fulfilled_on:
            raise ValueError("cannot change from fulfilled to unfulfilled")
                
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        cancelling the purchase
        """
        if not self.fulfilled: # remove the staging diff stock
            for material_name, quantity in self.content.items():
                material = Material.objects.filter(name=material_name).first()
                if not material:
                    continue
                material.add_pending_stock(-quantity)

        if not self.paid: # rm the debt
            add_debt(-self.final_price)

        super().delete(*args, **kwargs)
    
    