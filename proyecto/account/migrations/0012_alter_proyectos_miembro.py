# Generated by Django 4.1 on 2022-09-08 22:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0011_remove_proyectos_miembro_proyectos_miembro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyectos',
            name='miembro',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
