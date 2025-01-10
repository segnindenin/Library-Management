# Generated by Django 5.1.4 on 2025-01-09 14:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_rename_achats_achat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='telephone',
            field=models.CharField(max_length=14, validators=[django.core.validators.RegexValidator(message='Ce champ doit contenir uniquement des chiffres.', regex='^\\d+$')]),
        ),
        migrations.AlterField(
            model_name='emprunt',
            name='etat',
            field=models.CharField(choices=[('emprunté', 'Emprunté'), ('non rendu', 'Non Rendu'), ('rendu', 'Rendu')], max_length=20),
        ),
    ]