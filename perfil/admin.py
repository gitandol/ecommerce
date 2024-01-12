from django.contrib import admin
from .models import Perfil, Endereco


class EnderecoInLine(admin.TabularInline):
    model = Endereco
    extra = 1


class PerfilAdmin(admin.ModelAdmin):
    inlines = [
        EnderecoInLine
    ]


admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Endereco)
