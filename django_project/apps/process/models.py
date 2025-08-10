from django.db import models
from apps.product.models import Product
from apps.material.models import Material

class Formula(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    materials = models.JSONField(editable=False)
    expected_quantity = models.IntegerField()

    class Meta:
        verbose_name = 'រូបមន្ត'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.product.name} ({self.product.code} ចេញ{self.expected_quantity}{self.product.unit})"

class ManufacturingLog(models.Model):
    created_on = models.DateField(auto_now_add=True)
    formula = models.ForeignKey(Formula, on_delete=models.PROTECT)
    final_quantity = models.IntegerField()
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'ផលិតកម្ម'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.pk: # make changes only during creation
            # remove the material
            for material_name, quantity in self.formula.materials.items():
                Material.objects.get(name=material_name).add_stock(-quantity)

            # increase the product
            self.formula.product.add_stock(self.final_quantity)

        super().save(*args, **kwargs)
    
    def delete(self, *args, revert=True, **kwargs):
        if not revert:
            return super().delete(*args, **kwargs)

        self.formula.product.add_stock(-self.final_quantity)

        for material_name, quantity in self.formula.materials.items():
            material = Material.objects.filter(name=material_name).first()
            if not material:
                continue
            material.add_stock(quantity)

        super().delete(*args, **kwargs)