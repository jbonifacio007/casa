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
        descricao = p.descricao

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


 #   retorno = f'Despesa: {parcelamento_id} - {valor}'

#    return redirect( " url '/admin/financeiro/parcela/' ")
#    return HttpResponse(retorno )

    context = {
        "nome_pagina": "Parcelamento",
        "todas_reservas": parcelamento,
        "despesa_id": parcelamento_id,
        "mes": descricao,

    }
    return render(request, "geracaoparcela.html", context)

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


    valorTotalFinal = valorTotal
    valorTotal = valorTotal - valorVar


    totalvalorVar = valorVar
    valorVar = (valorVar / 30)


    dataatual = datetime.datetime.now()

    membros_qry = Membro.objects.raw(
        'SELECT id, nome, temporario,  sum(dias) dias FROM '
        '( '
        '	SELECT m.id, m.nome, m.temporario, COALESCE((data_final - data_inicio),0) dias '
        '		FROM cadastros_membro m '
        '		left join reservas_reserva r '
        '       on r.membro_id = m.id '
        '       and extract(month from data_inicio) =  ' + str(mes_anterior) + ' '  
        '   where temporario = False '
        ') T '
        'group by id,nome,temporario order by dias desc')

    membros_aux = membros_qry



    quant_membros = 0

    for cq in membros_qry:
        quant_membros = quant_membros + 1

    if quant_membros > 0:
        valor = (valorTotal / quant_membros)


    valorvariaveis = 0

    total_valor_parcela = 0
    with connection.cursor() as cursor:

        cursor.execute("DELETE from financeiro_despesaparcela WHERE despesa_id = %s", [despesa_id])
        valorfinal = 0
        quant_dias_ant = 0
        trinta_dias = 0
        primeira_vez = True
        for m in membros_qry:
            if primeira_vez:
               primeira_vez = False
               if m.dias == 30:
                  trinta_dias = m.dias
            if m.dias > 0:
               qtd_membros_dias = qtd_membros_dias + 1
               valores = []
               for d in range(m.dias):   #Percorre os dias e compara com os outros membros
                   qtd = 1
                   for a in membros_aux:
                       if a.id != m.id:  #Verifica se é um membro difente do atual do loop 'm'
                           if a.dias >= d+1:
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

               dias_para_subtrair = 0
             #  if quant_dias_ant > 0:
             #     dias_para_subtrair = 30 - quant_dias_ant
             #  else:
               dias_para_subtrair = (30 - m.dias)

               val_dias_resto = 0

               if not(trinta_dias == 30):
                  if dias_para_subtrair > 0:
                     val_dias_resto = (valorVar / quant_membros) * dias_para_subtrair

               valorfinal = valor + valor_parcela + val_dias_resto

               valorvariaveis = valorvariaveis + valorfinal


               total_valor_parcela = total_valor_parcela + valor_parcela + val_dias_resto

               cursor.execute("INSERT INTO financeiro_despesaparcela (despesa_id, membro_id, valor, criado, modificado, pago, datapagamento) VALUES (%s, %s, %s, %s, %s, %s, %s)", [despesa_id, membro_id,valorfinal,dataatual,dataatual,False,dataatual])

            quant_dias_ant = m.dias


#        if (quant_membros - qtd_membros_dias) > 0:
#            valorfinal = (valorTotalFinal - valorvariaveis) / (quant_membros - qtd_membros_dias)
#        else:
#            valorfinal = (valorTotalFinal - valorvariaveis) / (quant_membros)

        if (quant_membros - qtd_membros_dias) > 0:
            valorfinal = ((totalvalorVar - total_valor_parcela) / (quant_membros - qtd_membros_dias))


        valorfinal = valorfinal + valor

        if valorfinal < 0:
            valorfinal = 0

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
        "nome_pagina": "Despesas",
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