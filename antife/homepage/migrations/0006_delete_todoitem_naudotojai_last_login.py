# Generated by Django 5.0.2 on 2024-03-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_alter_receptai_fenilalaninas_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TodoItem',
        ),
        migrations.AddField(
            model_name='naudotojai',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
