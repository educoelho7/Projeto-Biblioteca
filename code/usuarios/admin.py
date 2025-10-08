from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    def nome_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    nome_completo.short_description = "Nome"

    list_display = ('username', 'nome_completo', 'email', 'telefone', 'pendencia', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'email', 'telefone', 'pendencia')}),
        ('Permissões', {'fields': ('is_active', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'first_name',
                'last_name',
                'email',
                'telefone',
                'password1',
                'password2',
            ),
        }),
    )

