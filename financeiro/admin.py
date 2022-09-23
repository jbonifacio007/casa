from django.contrib import admin
from financeiro.models import TipoDespesa,Despesa,Parcela,DespesaItem,Parcelamento,DespesaParcela
from django.db import connection
from . import models
from django.contrib.admin.views.main import ChangeList
from django.db.models import Sum, Avg
from django.utils.html import format_html
# Register your models here.



class DespesaItemInline(admin.TabularInline):
    model = models.DespesaItem
    list_display = ['descricao','tipodespesa','valor','gerar']
    exclude = ['usuario']
#    readonly_fields = ('lote','cliente','corretor','valor','formapagamento','quitado','usuario','obs')
    extra = 0

class DespesaParcelaInline(admin.TabularInline):
    model = models.DespesaParcela
    list_display = ['datapagamento','valor','pago']
#    readonly_fields = ('lote','cliente','corretor','valor','formapagamento','quitado','usuario','obs')
    extra = 0


class TotalChangeList(ChangeList):
    fields_to_total = ['valor', ]

    def get_total_values(self, queryset):
        total = DespesaItem()
        total.custom_alias_name = "Totais"
        total.descricao = "Total"
        for field in self.fields_to_total:
            setattr(total, field, queryset.aggregate(total=Sum('valor'))['total'])

        return total

    def get_results(self, request):
        super(TotalChangeList, self).get_results(request)
        total = self.get_total_values(self.queryset)
        len(self.result_list)
        self.result_list._result_cache.append(total)


class DespesaItemAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return TotalChangeList

    list_display = ['despesa','despesa_id','descricao','tipodespesa','valor','gerar']

    def save_model(self, request, obj, form, change):
        despesaitem_banco = getIdDespesaBanco(obj.id) #Pega o id da despesa direto do banco antes que altere o objeto
        id_despesa_anterior = 0
        if despesaitem_banco:
            id_despesa_anterior = despesaitem_banco[0]['despesa_id']

#        print(obj.despesa_id,id_despesa_anterior)

        obj.usuario = request.user
        super().save_model(request, obj, form, change)

        altera = AddDespesa(obj.despesa_id)
        if not(obj.despesa_id == id_despesa_anterior) and not(id_despesa_anterior == 0): #se tiver mudado a despesa altera o total da despesa anterior
            altera = AddDespesa(id_despesa_anterior)

    def delete_model(self, request, obj):
        deleta = DelDespesa(obj.valor, obj.despesa_id)
        obj.delete()




class DespesaAdmin(admin.ModelAdmin):

    inlines = [
        DespesaItemInline,
        DespesaParcelaInline
    ]


    list_display = ['__str__','total','gerar','status']
    exclude = ['usuario']
    readonly_fields = ('total',)


    def status(self, obj):
        vStatus = ''
        vGerado = SomaDespesas(obj.id)
        if vGerado == 1:
            color = 'green'
            vStatus = 'Gerado'
        elif vGerado == 2:
            color = 'red'
            vStatus = 'Precisa Gerar'
        else:
            vStatus = 'Gerando'
            color = 'orange'
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, vStatus))

    id_despesa = 0

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        self.id_despesa = obj.id
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            list_despesaitem = formset.save(commit=False)
            if not(list_despesaitem == []):
                for despesaitem in list_despesaitem:
                    despesaitem.usuario = request.user
#        return super().save_related(request, form, formsets, change)
        super().save_related(request, form, formsets, change)
        altera = AddDespesa(self.id_despesa)




class ParcelaAdmin(admin.ModelAdmin):
    list_display = ['parcelamento','membro','numero','vencimento','valor','pago']

    list_editable = ['numero','pago']



def SomaDespesas(despesa_id):

    despesa = Despesa.objects.all().filter(id=despesa_id)

    despesaparcela = DespesaParcela.objects.all().filter(despesa_id=despesa_id)



    totalItem = 0
    for d in despesa:
        mes = d.mes
        valorTotal = (d.total)

    for i in despesaparcela:
        totalItem = totalItem + i.valor

    retorno = 0

    if valorTotal > 0:
        if round(valorTotal) == round(totalItem):
            retorno = 1
        else:
            retorno = 2

    return retorno


def AddDespesa( despesa_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE financeiro_despesa set total = (SELECT COALESCE(SUM(Valor),0) valor from financeiro_despesaitem where despesa_id = %s) where id= %s",
            [despesa_id, despesa_id])
    return True

def DelDespesa( valor, despesa_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE financeiro_despesa set total = total - %s where id = %s",
            [valor, despesa_id])
    return True


def getIdDespesaBanco(item_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT despesa_id FROM financeiro_despesaitem where id = %s", [item_id])
        row = dictfetchall(cursor)
        class Meta:
            model = DespesaItem
            fields = ['despesa_id']
    return row

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]



class ParcelaInline(admin.TabularInline):
    model = models.Parcela
    list_display = ['membro','numero','datavencimento','valor','pago']
#    exclude = ['usuario']
#    readonly_fields = ('lote','cliente','corretor','valor','formapagamento','quitado','usuario','obs')
    readonly_fields = ('numero','valor',)
    extra = 0


class ParcelamentoAdmin(admin.ModelAdmin):
    inlines = [
        ParcelaInline
    ]

    list_display = ['descricao','quantidade', 'vencimento', 'valor','gerar']



admin.site.register(Parcelamento, ParcelamentoAdmin)

admin.site.register(Despesa, DespesaAdmin)

#admin.site.register(DespesaItem, DespesaItemAdmin)


admin.site.register(Parcela, ParcelaAdmin)

