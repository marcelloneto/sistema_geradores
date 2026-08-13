
from django.contrib import admin
from .models import TipoEnsaio, RegistroEnsaio, DadosTensaoAplicada, DadosSurgeTest, DadosBumpTest

@admin.register(TipoEnsaio)
class TipoEnsaioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'norma_referencia')
    search_fields = ('nome',)

# Aproveitando para registrar os outros também
admin.site.register(RegistroEnsaio)
admin.site.register(DadosTensaoAplicada)
admin.site.register(DadosSurgeTest)
admin.site.register(DadosBumpTest)