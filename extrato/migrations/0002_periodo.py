# Generated by Django 4.2.2 on 2023-07-08 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrato', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.IntegerField()),
                ('descricao', models.TextField()),
            ],
        ),
    ]