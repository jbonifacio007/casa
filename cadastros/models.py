from django.db import models
from colorfield.fields import ColorField
import datetime

# Create your models here.

class Base(models.Model):
    criado = models.DateField('Criação', auto_now_add=True)
    modificado = models.DateField('Atualização', auto_now=True)

    class Meta:
        abstract = True


class Membro(Base):
    nome = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', max_length=11)
    endereco = models.TextField('Endereço', max_length=200)
    temporario = models.BooleanField('Temporário?', default=False)
    cor = ColorField('Cor',default='#FF0000')
    corTexto = ColorField('Cor do Texto',default='#FF0000')

    class Meta:
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'
        ordering = ['nome']

    def __str__(self):
        return self.nome

class TipoDespesa(Base):
    descricao = models.CharField('Descrição', max_length=100)
    variavel = models.BooleanField('Variável', default=False)


    class Meta:
        verbose_name = 'Tipo Despesa'
        verbose_name_plural = 'Tipo Despesas'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao
