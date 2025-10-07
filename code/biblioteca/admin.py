from django.contrib import admin
from .models import Livro

class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "isbn", "autor", "ano")

admin.site.register(Livro, LivroAdmin)
