# Generated by Django 4.0.1 on 2022-11-02 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_logproyectos_id_proyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='logsprint',
            name='id_sprint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='account.sprint'),
        ),
    ]