from django.contrib import admin
from .models import Livro, Exemplar, Emprestimo, Multa

class LivroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "isbn", "autor", "ano")

class ExemplarAdmin(admin.ModelAdmin):
    def titulo(self, obj):
        return obj.livro.titulo

    def isbn(self, obj):
        return obj.livro.isbn

    titulo.admin_order_field = "livro__titulo"
    isbn.admin_order_field = "livro__isbn"

    list_display = ("id", "titulo", "isbn", "status")
    list_select_related = ("livro",)

class EmprestimoAdmin(admin.ModelAdmin):
    def email(self, obj):
        return obj.usuario.email

    def exemplar_id(self, obj):
        return obj.exemplar.id

    def livro_isbn(self, obj):
        return obj.exemplar.livro.isbn

    email.admin_order_field = "usuario__email"
    exemplar_id.admin_order_field = "exemplar__id"
    livro_isbn.admin_order_field = "exemplar__livro__isbn"

    list_display = ("email", "livro_isbn", "exemplar_id", "data_emprestimo", "data_devolucao")
    list_select_related = ("usuario", "exemplar", "exemplar__livro")

class MultaAdmin(admin.ModelAdmin):
    def emprestimo_id(self, obj):
        return obj.emprestimo.id

    emprestimo_id.admin_order_field = "emprestimo__id"
    list_display = ("emprestimo_id", "valor", "status")

admin.site.register(Livro, LivroAdmin)
admin.site.register(Exemplar, ExemplarAdmin)
admin.site.register(Emprestimo, EmprestimoAdmin)
admin.site.register(Multa, MultaAdmin)
