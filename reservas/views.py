from django.shortcuts import render,redirect
from django.http import HttpResponse
from reservas.models import Reserva
from django.conf import settings
from reservas.forms import ReservaForm
from django.contrib import messages
# Create your views here.


def calendario(request):


    todas_reservas = Reserva.objects.raw(
        '	SELECT id, data_final + 1 as data_final, data_inicio '
        '		FROM reservas_reserva ')



    context = {
        "nome_pagina":"Calendario",
        "todas_reservas": todas_reservas,

    }

    return render(request,"calendario.html",context)

def incluir_reserva(request):

    form = ReservaForm()

    if request.method == "POST":
        form = ReservaForm(request.POST)

        if form.is_valid():
            visitante = form.save(commit=False)

  #          visitante.registrado_por = request.user.porteiro
            visitante.save()

            messages.success(
                request,
                "Reserva incluida com sucesso!"
            )

            return redirect("incluir_reserva")


    todos_visitantes = Reserva.objects.all()

    context = {
        "nome_pagina":"Incluir Reserva",
        "form": form,
        "todos_visitantes": todos_visitantes,

    }

    return render(request, "incluir_reserva.html", context)





