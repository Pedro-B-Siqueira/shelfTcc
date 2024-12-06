# Generated by Django 5.1.2 on 2024-11-28 12:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0009_solicitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitation',
            name='data_solicitacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='solicitation',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes', to='shelf.product'),
        ),
        migrations.AlterField(
            model_name='solicitation',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('aceito', 'Aceito'), ('rejeitado', 'Rejeitado')], default='pendente', max_length=20),
        ),
    ]