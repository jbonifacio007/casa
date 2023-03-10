# Generated by Django 4.0.2 on 2022-03-20 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('data_inicio', models.DateField(verbose_name='Data Início')),
                ('data_final', models.DateField(verbose_name='Data Final')),
                ('membro', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cadastros.membro', verbose_name='Membro')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'ordering': ['data_inicio'],
            },
        ),
    ]
