# Generated by Django 5.0.3 on 2024-03-26 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0010_remove_naudotojai_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recepto_produktai',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
