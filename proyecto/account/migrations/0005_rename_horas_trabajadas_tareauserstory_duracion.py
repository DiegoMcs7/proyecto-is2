# Generated by Django 4.1 on 2022-11-03 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_rename_fecha_inicio_tareauserstory_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tareauserstory',
            old_name='horas_trabajadas',
            new_name='duracion',
        ),
    ]