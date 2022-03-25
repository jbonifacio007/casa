from django.shortcuts import render
from cadastros.models import Membro
from reservas.models import Reserva
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):

    todos_visitantes = Membro.objects.all()
    todas_reservas = Reserva.objects.all()

    membros_qry = Membro.objects.raw(
        '	SELECT m.id, m.nome,data_inicio,data_final,COALESCE((data_final - data_inicio),0) dias '
        '		FROM cadastros_membro m '
        '		inner join reservas_reserva r '
        '       on r.membro_id = m.id '
        '   where temporario = False '
        '   order by data_inicio desc ')



    context = {
        "nome_pagina":"Início Dashboard",
        "todos_visitantes": todos_visitantes,
        "todas_reservas": todas_reservas,
        "reservas": membros_qry,

    }

    return render(request,"index.html",context)