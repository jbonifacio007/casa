# Generated by Django 4.0.2 on 2022-05-24 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0005_reserva_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='divisaoproporcional',
            field=models.BooleanField(default=False, verbose_name='Divisão Proporcional'),
        ),
    ]
