from django.db import models
from django.utils import timezone
from apps.core.models import add_debt, fulfill_debt

class Material(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=4, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="in USD")
    unit = models.CharField(max_length=255)
    stock = models.IntegerField(default=0, editable=False)
    pending_stock = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

    def __str__(self):
        return f"{self.name} (${self.price}/{self.unit}) ({self.code})"
    
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

class Adjustment(models.Model):
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False, related_name='material_adjustments')
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity = models.IntegerField(help_text="ដកចេញ")
    comment = models.CharField(max_length=255, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.material.add_stock(-self.quantity)
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.material.add_stock(self.quantity)
        super().delete(*args, **kwargs)

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    BOOL_CHOICES = [(True, 'Yes'),(False, 'No')]
    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False)
    created_on = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False, choices=BOOL_CHOICES)
    paid_on = models.DateField(null=True, blank=True, editable=False)
    fulfilled = models.BooleanField(default=False, choices=BOOL_CHOICES)
    fulfilled_on = models.DateField(null=True, blank=True, editable=False)

    content = models.JSONField(editable=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2,
        help_text="បើមិនដាក់ វានឹងគណនាឲ្យ")
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):    
        if not self.pk:
            calculate_price = not self.price
            for material_name, quantity in self.content.items():
                material = Material.objects.get(name=material_name)
                material.add_pending_stock(quantity)
                if calculate_price:
                    self.price += material.price * quantity
            add_debt(self.price)

            
        if self.paid and not self.paid_on:
            self.paid_on = timezone.now().date()
            fulfill_debt(self.price)
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
            add_debt(-self.price)

        super().delete(*args, **kwargs)
    
    