from django.db import models
from cadastros.models import Base,Membro
from django.utils import timezone
# Create your models here.
from django.core.exceptions import ValidationError


class Reserva(Base):
    membro = models.ForeignKey(Membro, on_delete=models.RESTRICT, verbose_name='Membro' )
    data_inicio = models.DateField(verbose_name='Data Início',auto_now=False, auto_now_add=False)
    data_final = models.DateField(verbose_name='Data Final',auto_now=False, auto_now_add=False)

    def clean(self):

        if self.data_inicio > self.data_final :
            raise ValidationError({'data_inicio': ('Data Início não pode ser maior que a final!')})


    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['data_inicio']

    def __str__(self):
        return f'Membro: {self.membro.nome} '
