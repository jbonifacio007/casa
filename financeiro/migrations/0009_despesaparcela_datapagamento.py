# Generated by Django 4.0.2 on 2022-03-21 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financeiro', '0008_remove_despesaparcela_datapagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesaparcela',
            name='datapagamento',
            field=models.DateField(null=True, verbose_name='Data Pagamento'),
        ),
    ]
