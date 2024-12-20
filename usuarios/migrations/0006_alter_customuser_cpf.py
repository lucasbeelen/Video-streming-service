# Generated by Django 5.1 on 2024-09-18 02:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_alter_customuser_cpf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cpf',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_cpf', regex='^\\d{11}$')]),
        ),
    ]
