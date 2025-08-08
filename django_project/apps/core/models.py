from django.db import models

class Money(models.Model):
    """
    singleton to keep track of balance
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="$", default=0)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="$", default=0)
    debt = models.DecimalField(max_digits=10, decimal_places=2, help_text="$", default=0)

def fulfill_money(amount):
    money = Money.objects.first()
    money.amount += amount
    money.pending_amount -= amount
    money.save()

def add_pending_money(amount):
    money = Money.objects.first()
    money.pending_amount += amount
    money.save()

def add_debt(amount):
    money = Money.objects.first()
    money.debt += amount
    money.save()

def fulfill_debt(amount):
    money = Money.objects.first()
    money.debt -= amount
    money.amount -= amount
    money.save()

