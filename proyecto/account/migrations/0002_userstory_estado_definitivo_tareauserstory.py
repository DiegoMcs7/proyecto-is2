# Generated by Django 4.1 on 2022-11-03 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='estado_definitivo',
            field=models.TextField(choices=[('Pendiente', 'Pendiente'), ('Finalizado', 'Finalizado')], default='Pendiente', max_length=11),
        ),
        migrations.CreateModel(
            name='TareaUserStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('desc_daily', models.TextField()),
                ('horas_trabajadas', models.IntegerField(default=0)),
                ('id_user_story', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.userstory')),
            ],
        ),
    ]
