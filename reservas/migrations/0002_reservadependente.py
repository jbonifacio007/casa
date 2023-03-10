# Generated by Django 4.0.2 on 2022-05-11 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_tipodependente_dependente'),
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservaDependente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado', models.DateField(auto_now_add=True, verbose_name='Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Atualização')),
                ('dependente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cadastros.dependente', verbose_name='Dependente')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reservas.reserva', verbose_name='Reserva')),
            ],
            options={
                'verbose_name': 'Reserva Dependente',
                'verbose_name_plural': 'Reserva Dependentes',
            },
        ),
    ]
