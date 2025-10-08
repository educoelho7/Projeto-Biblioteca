from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefone = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(r'^\d{10,11}$', "São aceitos somente números (10 ou 11 dígitos).")
        ]
    )
    pendencia = models.BooleanField(default=False)