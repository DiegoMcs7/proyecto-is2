# Generated by Django 4.0.1 on 2022-10-30 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_loguserstory_logtipo_user_story_logsprint_logrol_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logestados',
            name='usuario_responsable',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logmiembro_sprint',
            name='usuario_responsable',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logmiembros',
            name='usuario_responsable',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logproyectos',
            name='fecha_creacion',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logproyectos',
            name='usuario_responsable',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logrol',
            name='usuario_responsable',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logsprint',
            name='usuario_responsable',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='logtipo_user_story',
            name='usuario_responsable',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='loguserstory',
            name='usuario_responsable',
            field=models.TextField(),
        ),
    ]
