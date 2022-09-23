from django.db import models
from cadastros.models import Base,Membro,Dependente
from django.utils import timezone
# Create your models here.
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model

#id_membro = 4

def RetornaId(m):
    id = m.membro.nome
    print('passou no retorna',m)
    return 0

class Reserva(Base):
    membro = models.ForeignKey(Membro, on_delete=models.RESTRICT, verbose_name='Membro', limit_choices_to={'temporario': False} )
    data_inicio = models.DateField(verbose_name='Data Início',auto_now=False, auto_now_add=False)
    data_final = models.DateField(verbose_name='Data Final',auto_now=False, auto_now_add=False)
    usuario = models.ForeignKey(get_user_model(), verbose_name='Usuário',on_delete=models.RESTRICT)
    divisaoproporcional = models.BooleanField('Divisão Proporcional', default=False)


    def gerar(self):

        global id_membro
        id_membro = self.membro.id

        return mark_safe(
             """<a href=\"/proposta/%s/\" target="_blank"> Gerar </a>""" % self.id)


    def clean(self):

        if self.data_inicio > self.data_final :
            raise ValidationError({'data_inicio': ('Data Início não pode ser maior que a final!')})


    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['data_inicio']

    def __str__(self):
        return f' {self.membro.nome} '



class ReservaDependente(Base):


    reserva = models.ForeignKey(Reserva, on_delete=models.RESTRICT, verbose_name='Reserva')
#    dependente = models.ForeignKey(Dependente, on_delete=models.RESTRICT, verbose_name='Dependente',limit_choices_to= limit_pub_date_choices(Reserva.membro))
#    dependente = models.ForeignKey(Dependente, on_delete=models.RESTRICT, verbose_name='Dependente',limit_choices_to={'membro_id': id_membro})
#    dependente = models.ForeignKey(Dependente, on_delete=models.RESTRICT, verbose_name='Dependente',limit_choices_to=Q(membro_id=id_membro))
    dependente = models.ForeignKey(Dependente, on_delete=models.RESTRICT, verbose_name='Dependente')


    class Meta:
        verbose_name = 'Reserva Dependente'
        verbose_name_plural = 'Reserva Dependentes'

    def __str__(self):
        return f'Dep:{self.dependente.nome}'



