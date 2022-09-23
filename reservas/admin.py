from django.contrib import admin
from reservas.models import Reserva,ReservaDependente
from cadastros.models import Membro

# Register your models here.


class ReservaDependenteInline(admin.TabularInline):
    model = ReservaDependente
    list_display = ['reserva','dependente']
#    readonly_fields = ('lote','cliente','corretor','valor','formapagamento','quitado','usuario','obs')
    extra = 0




class ReservaAdmin(admin.ModelAdmin):


    inlines = [
        ReservaDependenteInline,
    ]


    list_display = ['membro','data_inicio','data_final','get_data_dif','divisaoproporcional','gerar']
    exclude = ['usuario']

    def get_data_dif(self,obj):
        diferenca = (obj.data_final - obj.data_inicio)
        return diferenca.days
    get_data_dif.short_description = 'Dias'

    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        super().save_model(request, obj, form, change)



admin.site.register(Reserva, ReservaAdmin)

