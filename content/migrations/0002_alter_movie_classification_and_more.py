# Generated by Django 5.1 on 2024-09-18 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='classification',
            field=models.IntegerField(choices=[(0, 'Livre'), (10, '10+'), (12, '12+'), (14, '14+'), (16, '16+'), (18, '18+')], default=0, help_text='Classificação etária do conteúdo'),
        ),
        migrations.AlterField(
            model_name='serie',
            name='classification',
            field=models.IntegerField(choices=[(0, 'Livre'), (10, '10+'), (12, '12+'), (14, '14+'), (16, '16+'), (18, '18+')], default=0, help_text='Classificação etária do conteúdo'),
        ),
    ]
