from django.db import models
from apps.product.models import Product
from apps.material.models import Material

class Formula(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    expected_quantity = models.IntegerField()

    class Meta:
        verbose_name = 'រូបមន្ត'
        verbose_name_plural = verbose_name
        unique_together = ('product', 'expected_quantity')

    def __str__(self):
        return f"{self.product.name} ({self.product.code} ចេញ{self.expected_quantity}{self.product.unit})"

class FormulaItem(models.Model):
    """
    Inline model for formula
    """
    formula = models.ForeignKey(Formula, on_delete=models.CASCADE, related_name='items')
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.material.code}: {self.quantity}"

    def consume_stock(self):
        self.material.add_stock(-self.quantity)
    
    def undo_stock(self):
        self.material.add_stock(self.quantity)

class ManufacturingLog(models.Model):
    created_on = models.DateField(auto_now_add=True)
    formula = models.ForeignKey(Formula, on_delete=models.PROTECT)
    final_quantity = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'ផលិតកម្ម'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        creation = not self.pk
        if creation:  # consume the material
            for item in self.formula.items.all():
                item.consume_stock()
            # produce the product
            self.formula.product.add_stock(self.final_quantity)
        super().save(*args, **kwargs)
    
    def delete(self, *args, revert=True, **kwargs):
        if revert:
            self.formula.product.add_stock(-self.final_quantity)
            for item in self.formula.items.all():
                item.undo_stock()
        super().delete(*args, **kwargs)