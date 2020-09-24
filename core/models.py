from django.db import models
from django.contrib.auth.models import User


class Account(User):
    name = models.CharField(verbose_name="nome", max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

    def __str__(self):
        return self.name
