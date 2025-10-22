from django.core.validators import RegexValidator
from usuarios.models import Usuario
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

    def __str__(self):                       
        return f"{self.titulo} - {self.autor}"

class Exemplar(models.Model):
    StatusType = models.TextChoices("Status", "DISPONIVEL EMPRESTADO")

    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    status = models.CharField(choices=StatusType, default=StatusType.DISPONIVEL)

    def __str__(self):                       
        return f"{self.id} - {self.livro}"

class Emprestimo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):                       
        return f"{self.usuario} - {self.exemplar}"

class Multa(models.Model):
    StatusType = models.TextChoices("Status", "EM_ABERTO PAGA")

    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(choices=StatusType, default=StatusType.EM_ABERTO)

    def __str__(self):                       
        return f"{self.emprestimo} - {self.valor}"
