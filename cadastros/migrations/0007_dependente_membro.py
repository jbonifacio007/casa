# Generated by Django 4.0.2 on 2022-05-11 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_tipodependente_dependente'),
    ]

    operations = [
        migrations.AddField(
            model_name='dependente',
            name='membro',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='cadastros.membro', verbose_name='Membro'),
            preserve_default=False,
        ),
    ]
