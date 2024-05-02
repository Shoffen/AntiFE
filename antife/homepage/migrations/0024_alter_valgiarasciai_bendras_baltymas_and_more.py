# Generated by Django 4.2.7 on 2024-04-30 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0023_merge_20240422_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='valgiarasciai',
            name='bendras_baltymas',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='valgiarasciai',
            name='bendras_fenilalaninas',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
