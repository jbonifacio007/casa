# Generated by Django 4.0.2 on 2022-03-21 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0007_alter_parcela_membro_alter_parcela_vencimento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='despesaparcela',
            name='datapagamento',
        ),
    ]
