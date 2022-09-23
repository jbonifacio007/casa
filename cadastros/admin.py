from django.contrib import admin
from cadastros.models import Membro,TipoDespesa,Dependente,TipoDependente

# Register your models here.



class DependenteInline(admin.TabularInline):
    model = Dependente
    list_display = ['nome','cpf','tipodependente']
#    readonly_fields = ('lote','cliente','corretor','valor','formapagamento','quitado','usuario','obs')
    extra = 0

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        kwargs['queryset'] = Dependente.objects.filter(fixo=self.type)
#        kwargs['queryset'] = Dependente.objects.filter(fixo=True)



class MembroAdmin(admin.ModelAdmin):

    inlines = [
        DependenteInline,
    ]


    list_display = ['nome','cpf','cor','corTexto']

    list_editable = ['cor','corTexto']





class TipoDespesaAdmin(admin.ModelAdmin):

    list_display = ['descricao','variavel','proporcional']

    list_editable = ['variavel','proporcional']





admin.site.register(Membro, MembroAdmin)
admin.site.register(TipoDespesa, TipoDespesaAdmin)
admin.site.register(TipoDependente)


admin.site.site_header = 'Administração da Casa'
admin.site.site_title = 'Casa de Praia'
admin.site.index_title = 'Gerenciamento Financeiro/Reverva'

