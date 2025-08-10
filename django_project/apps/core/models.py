from django.db import models

class Money(models.Model):
    """
    singleton to keep track of balance
    """
    amount = models.IntegerField(help_text="៛", default=0)
    pending_amount = models.IntegerField(help_text="៛", default=0)
    debt = models.IntegerField(help_text="៛", default=0)

    class Meta:
        verbose_name = 'លុយ'
        verbose_name_plural = verbose_name

class Transaction(models.Model):
    created_on = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('user.User', on_delete=models.PROTECT, editable=False)
    amount = models.IntegerField(help_text="៛")
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'ថែមថយលុយ'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        if not self.pk:
            money, _ = Money.objects.get_or_create()
            money.amount += self.amount
            money.save()
        super().save(*args, **kwargs)
    
    def delete(self, *args, revert=True, **kwargs):
        if revert:
            money, _ = Money.objects.get_or_create()
            money.amount -= self.amount
            money.save()
        super().delete(*args, **kwargs)

def add_money(amount):
    money, _ = Money.objects.get_or_create()
    money.amount += amount
    money.save()

def fulfill_money(amount):
    money, _ = Money.objects.get_or_create()
    money.amount += amount
    money.pending_amount -= amount
    money.save()

def add_pending_money(amount):
    money, _ = Money.objects.get_or_create()
    money.pending_amount += amount
    money.save()

def add_debt(amount):
    money, _ = Money.objects.get_or_create()
    money.debt += amount
    money.save()

def fulfill_debt(amount):
    money, _ = Money.objects.get_or_create()
    money.debt -= amount
    money.amount -= amount
    money.save()

