from django.contrib import admin
from cadastros.models import Membro,TipoDespesa

# Register your models here.


class MembroAdmin(admin.ModelAdmin):

    list_display = ['nome','cpf','cor','corTexto']

    list_editable = ['cor','corTexto']

class TipoDespesaAdmin(admin.ModelAdmin):

    list_display = ['descricao','variavel']

    list_editable = ['variavel']


admin.site.register(Membro, MembroAdmin)
admin.site.register(TipoDespesa, TipoDespesaAdmin)


admin.site.site_header = 'Administração da Casa'
admin.site.site_title = 'Casa de Praia'
admin.site.index_title = 'Gerenciamento Financeiro/Reverva'

