from django.db import models

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length = 200)
    completed = models.BooleanField(default = False)

class Product(models.Model):
    name = models.CharField(max_length=255)
    calories = models.DecimalField(max_digits=5, decimal_places=2)
    total_fat = models.DecimalField(max_digits=5, decimal_places=2)
    fiber = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    phenylalanine = models.DecimalField(max_digits=5, decimal_places=3)
    def __str__(self):
        return self.name

