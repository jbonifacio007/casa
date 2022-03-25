from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Parcelamento,Membro,Despesa,DespesaItem
from django.db import connection
import datetime
from dateutil.relativedelta import *


from django.conf import settings
# Create your views here.





def gerarparcela(request, parcelamento_id):

    membros = Membro.objects.all().filter(temporario=False)
    parcelamento = Parcelamento.objects.all().filter(id=parcelamento_id)

    for p in parcelamento:
        valor = (p.valor)
        vencimento = (p.vencimento)

    valor = (valor / 10)

    numero_parcela = 0

    dataatual = vencimento

    with connection.cursor() as cursor:

        cursor.execute("DELETE from financeiro_parcela WHERE parcelamento_id = %s", [parcelamento_id])

        for m in membros:
           dataatual = dataatual + relativedelta(months=+1)
           membro_id = (m.id)
           numero_parcela = numero_parcela + 1


           cursor.execute("INSERT INTO financeiro_parcela (parcelamento_id, membro_id, numero, vencimento, valor, criado, modificado, pago) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", [parcelamento_id, membro_id,numero_parcela,dataatual,valor,datetime.datetime.now(),datetime.datetime.now(), False])


    retorno = f'Despesa: {parcelamento_id} - {valor}'

#    return redirect( " url '/admin/financeiro/parcela/' ")
    return HttpResponse(retorno )


def gerardespesaparcela(request, despesa_id):

#    membros = Membro.objects.all().filter(temporario=False)

    despesa = Despesa.objects.all().filter(id=despesa_id)

    despesaitem = DespesaItem.objects.all().filter(despesa_id=despesa_id)

    valorTotal = 0
    valor = 0
    valorVar = 0
    mes = 0
    mes_anterior = 0
    qtd_membros_dias = 0

    for d in despesa:
        mes = d.mes
        valorTotal = (d.total)

    for i in despesaitem:
        if i.tipodespesa.variavel:
            valorVar = valorVar + (i.valor)


    if mes > 1:
        mes_anterior = mes - 1
    else:
        if mes == 1:
            mes_anterior = 12


    valorVar = (valorVar / 30)
    valor = (valorTotal / 10)


    dataatual = datetime.datetime.now()

    membros_qry = Membro.objects.raw(
        'SELECT id, nome, sum(dias) dias FROM '
        '( '
        '	SELECT m.id, m.nome, COALESCE((data_final - data_inicio),0) dias '
        '		FROM cadastros_membro m '
        '		left join reservas_reserva r '
        '       on r.membro_id = m.id '
        '       and extract(month from data_inicio) =  ' + str(mes_anterior) + ' '  
        '   where temporario = False '
        ') T '
        'group by id,nome order by nome')

    membros_aux = membros_qry

    valorvariaveis = 0

    with connection.cursor() as cursor:

        cursor.execute("DELETE from financeiro_despesaparcela WHERE despesa_id = %s", [despesa_id])
        valorfinal = 0
        for m in membros_qry:
            if m.dias > 0:
               qtd_membros_dias = qtd_membros_dias + 1
               valores = []
               for d in range(m.dias):   #Percorre os dias e compara com os outros membros

                   qtd = 1
                   for a in membros_aux:
                       if a.id != m.id:  #Verifica se é um membro difente do atual do loop 'm'
                           if a.dias > d+1:
                              qtd = qtd + 1

                   valores.append({d:qtd})  #Preenche o dicionário a quantidade de membros a ser dividido de cada dia

               j = 0
               valor_parcela = 0
               for v in valores:

                   if v[j] != 0:
                      valor_parcela = valor_parcela + (valorVar / v[j])
                   else:
                      valor_parcela = valor_parcela + valorVar
                   j = j + 1

               membro_id = (m.id)

               valorfinal = (valor - valorVar) + valor_parcela

               valorvariaveis = valorvariaveis + valorfinal

               cursor.execute("INSERT INTO financeiro_despesaparcela (despesa_id, membro_id, valor, criado, modificado, pago, datapagamento) VALUES (%s, %s, %s, %s, %s, %s, %s)", [despesa_id, membro_id,valorfinal,dataatual,dataatual,False,dataatual])

        valorfinal = (valorTotal - valorvariaveis) / (10 - qtd_membros_dias)

        for m in membros_qry:
            membro_id = (m.id)

            if m.dias == 0:
                cursor.execute(
                    "INSERT INTO financeiro_despesaparcela (despesa_id, membro_id, valor, criado, modificado, pago, datapagamento) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    [despesa_id, membro_id, valorfinal, dataatual, dataatual, False, dataatual])


    retorno = f'Despesa: {despesa_id} - {valor} - {membros_qry}'

#    return redirect( " url '/admin/financeiro/parcela/' ")
#    return HttpResponse(retorno )


    context = {
        "nome_pagina": "Calendario",
        "todas_reservas": retorno,
        "despesa_id": despesa_id,
        "mes": mes,

    }

    return render(request, "geracaoparcela.html", context)


def fazBackupProva(self, materia_id, user_id, usuario, nome_materia):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO alunos_respostashistory (prova_id, data, materia_id, pergunta_id, resposta, user_id, resultado, peso, nr_pergunta, pergunta) SELECT prova_id, data, materia_id, pergunta_id, resposta, user_id, resultado, peso, nr_pergunta, pergunta from view_provas where materia_id = %s and user_id = %s", [materia_id, user_id])
        cursor.execute("INSERT INTO alunos_provashistory (prova_id, user_id, materia_id, qtde_perguntas, status, nota) SELECT prova_id, user_id, materia_id, qtde_perguntas, status, nota FROM view_provas_resumo where materia_id = %s and user_id = %s", [materia_id, user_id])
        cursor.execute("DELETE FROM alunos_respostas WHERE materia_id = %s and usuario = %s", [materia_id, usuario])
        cursor.execute("DELETE FROM alunos_alunomaterianota WHERE materia = %s and user_id = %s", [nome_materia, user_id])
    return True