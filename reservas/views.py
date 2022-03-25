from django.shortcuts import render,redirect
from django.http import HttpResponse
from reservas.models import Reserva
from django.conf import settings
# Create your views here.


def calendario(request):

    todas_reservas = Reserva.objects.all()

    context = {
        "nome_pagina":"Calendario",
        "todas_reservas": todas_reservas,

    }

    return render(request,"calendario.html",context)


