# Generated by Django 4.1 on 2022-08-30 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_kanban_permisos_reportes_reuniones_sprint_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembros',
            name='id_rol',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.roles'),
        ),
    ]
