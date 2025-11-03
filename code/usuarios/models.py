from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    telefone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                r'^.{14,15}$',
                "O telefone deve conter entre 14 e 15 caracteres."
            )
        ]
    )
    pendencia = models.BooleanField(default=False)