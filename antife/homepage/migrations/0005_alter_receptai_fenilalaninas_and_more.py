# Generated by Django 5.0.2 on 2024-03-15 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_alter_receptai_fenilalaninas_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receptai',
            name='fenilalaninas',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='receptai',
            name='kalorijos',
            field=models.FloatField(default=0.0),
        ),
    ]