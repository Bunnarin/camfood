from django.db import models
from apps.product.models import Product
from apps.material.models import Material

class ManufacturingLog(models.Model):
    created_on = models.DateField(auto_now_add=True)
    material = models.JSONField(editable=False)
    product = models.JSONField(editable=False)
    comment = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk: # make changes only during creation
            # increase the product stock
            for product_name, quantity in self.product.items():
                Product.objects.get(name=product_name).add_stock(quantity)
            # remove the material
            for material_name, quantity in self.material.items():
                Material.objects.get(name=material_name).add_stock(-quantity)

        super().save(*args, **kwargs)
    
    def delete(self, *args, revert_stock=True, **kwargs):
        if not revert_stock:
            super().delete(*args, **kwargs)
        for product_name, quantity in self.product.items():
            product = Product.objects.filter(name=product_name).first()
            if not product:
                continue
            product.add_stock(-quantity)
        for material_name, quantity in self.material.items():
            material = Material.objects.filter(name=material_name).first()
            if not material:
                continue
            material.add_stock(quantity)

        super().delete(*args, **kwargs)