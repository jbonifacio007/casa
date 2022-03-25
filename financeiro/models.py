from django.db import models
from cadastros.models import Base,Membro,TipoDespesa
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime
import locale


# Create your models here.

def anoAtual():

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")

    return year

def mesAtual():

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    mes = date.strftime("%m")

    return mes

def nomeMesAtual():
    # Configurações do usuário
    locale.setlocale(locale.LC_ALL, '')

    # Obtém um datatime da data e hora atual
    hoje = datetime.datetime.today()

    # Exibe o nome do mês no formato curto

    return hoje.strftime("O mês é: %b")



class Despesa(Base):
    mes = models.IntegerField('Mês', default=mesAtual())
    ano = models.IntegerField('Ano', default=anoAtual())
    total = models.DecimalField('Total', default=0, decimal_places=2,max_digits=12)
    usuario = models.ForeignKey(get_user_model(), verbose_name='Usuário',on_delete=models.RESTRICT)

    def gerar(self):
        return mark_safe(
            """<a href=\"/gerardespesaparcela/%s/\" target="_blank"> Gerar </a>""" % self.id)

#            """<a href=\"/gerarparcela/\" target="_blank"> Gerar </a>""" )

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
#        return f'Mes: {self.mes} / {self.ano}  - {nomeMesAtual()}'
        return f'Mes: {self.mes} / {self.ano} '


class DespesaItem(Base):
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE, verbose_name='Despesa' )
    descricao = models.CharField('Descrição', max_length=100)
    tipodespesa = models.ForeignKey(TipoDespesa, on_delete=models.RESTRICT, verbose_name='Tipo Despesa' )
    valor = models.DecimalField('Valor', default=0, decimal_places=2,max_digits=12)
    usuario = models.ForeignKey(get_user_model(), verbose_name='Usuário',on_delete=models.RESTRICT)

    def gerar(self):
        return mark_safe(
            """<a href=\"/proposta/%s/\" target="_blank"> Gerar </a>""" % self.id)


    def clean(self):

        if not(self.despesa.id):
            raise ValidationError({'descricao': ('Despesa Ainda Não Gravada!')})


    class Meta:
        verbose_name = 'Despesa Item'
        verbose_name_plural = 'Despesas Itens'
        ordering = ['descricao']

    def __str__(self):
        if self.descricao:
          return self.descricao
        else:
          return self.custom_alias_name



class DespesaParcela(Base):
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE, verbose_name='Despesa' )
    membro = models.ForeignKey(Membro, on_delete=models.RESTRICT, verbose_name='Membro')
    datapagamento = models.DateField(verbose_name='Data Pagamento',auto_now=False, auto_now_add=False, null=True)
    valor = models.DecimalField('Valor', default=0, decimal_places=2,max_digits=12)
    pago = models.BooleanField('Pago', default=False)

    class Meta:
        verbose_name = 'Despesa Parcela'
        verbose_name_plural = 'Despesa Parcelas'
        ordering = ['despesa']
    def __str__(self):
          return self.membro.nome





class Parcelamento(Base):
    descricao = models.CharField('Descrição', max_length=100)
    quantidade = models.IntegerField('Quantidade', default=0)
    vencimento = models.DateField(verbose_name='Data Vencimento',auto_now=False, auto_now_add=False)
    valor = models.DecimalField('Valor', default=0, decimal_places=2,max_digits=12)

    def gerar(self):
        return mark_safe(
            """<a href=\"/gerarparcela/%s/\" target="_blank"> Gerar </a>""" % self.id)


    class Meta:
        verbose_name = 'Parcelamento'
        verbose_name_plural = 'Parcelamentos'

    def __str__(self):
          return self.descricao


class Parcela(Base):
    parcelamento = models.ForeignKey(Parcelamento, on_delete=models.RESTRICT, verbose_name='Parcelamento')
    membro = models.ForeignKey(Membro, on_delete=models.RESTRICT, verbose_name='Membro')
    numero = models.IntegerField('Numero da Parcela', default=0)
#    vencimento = models.DateField(verbose_name='Data Vencimento',auto_now=False, auto_now_add=False, default= datetime.datetime.now())
    vencimento = models.DateField(verbose_name='Data Vencimento',auto_now=False, auto_now_add=False)
    valor = models.DecimalField('Valor', default=0, decimal_places=2,max_digits=12)
    pago = models.BooleanField('Pago', default=False)

    class Meta:
        verbose_name = 'Parcela'
        verbose_name_plural = 'Parcelas'
        ordering = ['parcelamento','numero']
    def __str__(self):
          return self.parcelamento.descricao




