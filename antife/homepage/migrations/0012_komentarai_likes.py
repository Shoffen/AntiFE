# Generated by Django 5.0.2 on 2024-04-22 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0011_recepto_produktai_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='komentarai',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
