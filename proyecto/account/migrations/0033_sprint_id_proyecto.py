# Generated by Django 4.1 on 2022-09-25 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_alter_miembro_sprint_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='id_proyecto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.proyectos'),
        ),
    ]