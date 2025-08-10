from django.db import models
from django.utils import timezone
from apps.core.models import add_debt, fulfill_debt
from django.urls import reverse

class Material(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=4, unique=True)
    price = models.IntegerField(help_text="៛")
    unit = models.CharField(max_length=255)
    stock = models.IntegerField(default=0)
    pending_stock = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'ស្តុកគ្រឿង'
        verbose_name_plural = verbose_name

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
    quantity = models.IntegerField(help_text="ថែម, ដាក់ - ពីមុខដើម្បីថយ")
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'ថែមថយស្តុកគ្រឿង'
        verbose_name_plural = verbose_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.material.add_stock(self.quantity)
        super().save(*args, **kwargs)
    
    def delete(self, *args, revert=True, **kwargs):
        if revert:
            self.material.add_stock(-self.quantity)
        super().delete(*args, **kwargs)

class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'អ្នកផ្គត់ផ្គង់'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('material:change_supplier', kwargs={'pk': self.pk})

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)

    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False)
    created_on = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True, editable=False)
    done = models.BooleanField(default=False)
    done_on = models.DateField(null=True, blank=True, editable=False)

    content = models.JSONField(editable=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = 'បុងទិញចូល'
        verbose_name_plural = 'បុងទិញចូល'

    def save(self, *args, **kwargs):    
        if not self.pk:
            for material_name, (quantity, final_price) in self.content.items():
                material = Material.objects.get(name=material_name)
                material.add_pending_stock(quantity)
                self.price += final_price
            add_debt(self.price)

        if self.paid and not self.paid_on:
            self.paid_on = timezone.now().date()
            fulfill_debt(self.price)
        elif not self.paid and self.paid_on:
            raise ValueError("cannot change from paid to unpaid")

        if self.done and not self.done_on:
            self.done_on = timezone.now().date()
            for material_name, (quantity, _) in self.content.items():
                material = Material.objects.filter(name=material_name).first()
                if not material:
                    continue
                material.fulfill_stock(quantity)
        elif not self.done and self.done_on:
            raise ValueError("cannot change from done to undone")
                
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """
        cancelling the purchase
        """
        if not self.done: # remove the staging diff stock
            for material_name, (quantity, _) in self.content.items():
                material = Material.objects.filter(name=material_name).first()
                if not material:
                    continue
                material.add_pending_stock(-quantity)

        if not self.paid: # rm the debt
            add_debt(-self.price)

        super().delete(*args, **kwargs)
    
    