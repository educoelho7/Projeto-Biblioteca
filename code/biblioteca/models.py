from django.core.validators import RegexValidator
from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    editora = models.CharField(max_length=255)
    ano = models.IntegerField()
    isbn = models.CharField(
        max_length=13,
        unique=True,
        validators=[
            RegexValidator(r'^\d{13}$', "O ISBN deve conter 13 dígitos.")
        ],
    )
    categoria = models.CharField(max_length=255)

