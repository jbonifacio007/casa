from django.contrib import admin
from reservas.models import Reserva

# Register your models here.


class ReservaAdmin(admin.ModelAdmin):

    list_display = ['membro','data_inicio','data_final']


admin.site.register(Reserva, ReservaAdmin)

