# loja/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer

@receiver(post_save, sender=User)
def criar_cliente(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            usuario=instance,
            nome=instance.username,
            email=instance.email,
        )

@receiver(post_save, sender=User)
def salvar_cliente(sender, instance, **kwargs):
    instance.customer.save()
