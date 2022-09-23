# Generated by Django 4.0.2 on 2022-05-11 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_remove_membro_extra_remove_tipodespesa_extra'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDependente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('fixo', models.BooleanField(default=False, verbose_name='Fixo')),
            ],
            options={
                'verbose_name': 'Tipo Dependente',
                'verbose_name_plural': 'Tipo Dependentes',
                'ordering': ['descricao'],
            },
        ),
        migrations.CreateModel(
            name='Dependente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('cpf', models.CharField(max_length=11, verbose_name='CPF')),
                ('tipodependente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cadastros.tipodependente', verbose_name='Tipo Dependente')),
            ],
            options={
                'verbose_name': 'Dependente',
                'verbose_name_plural': 'Dependentes',
                'ordering': ['nome'],
            },
        ),
    ]