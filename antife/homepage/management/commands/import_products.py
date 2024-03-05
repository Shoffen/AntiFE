import csv
from django.core.management.base import BaseCommand
from homepage.models import Product

class Command(BaseCommand):
    help = 'Import data from Produktai_data.csv'

    def handle(self, *args, **options):
        file_path = 'C:\\Users\\Rokan\\Documents\\GitHub\\AntiFE\\Produktai_data.csv'  # Replace with the actual path to your CSV file

        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Product.objects.create(
                    name=row['name'],
                    calories=row['calories'],
                    total_fat=row['total_fat'],
                    fiber=row['fiber'],
                    protein=row['protein'],
                    phenylalanine=row['phenylalanine'],
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
