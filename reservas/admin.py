from django.contrib import admin
from reservas.models import Reserva

# Register your models here.


class ReservaAdmin(admin.ModelAdmin):

    list_display = ['membro','data_inicio','data_final','get_data_dif']

    def get_data_dif(self,obj):
        diferenca = (obj.data_final - obj.data_inicio)
        return diferenca.days
    get_data_dif.short_description = 'Dias'

admin.site.register(Reserva, ReservaAdmin)

