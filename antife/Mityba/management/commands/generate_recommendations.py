# File: <your_app>/management/commands/generate_recommendations.py

import os
import random
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from homepage.models import Receptai, Product

class Command(BaseCommand):
    help = 'Generates Excel file for recommendations'

    def generate_recommendations(self):
        categories = ['Pusryčiai', 'Pietus', 'Vakarienė', 'Papildomai']
        recommendations = {}

        for category in categories:
            if random.choice([True, False]):  # Randomly choose between a recipe or a product
                recommendation = random.choice(Receptai.objects.filter(visible=True))
                recommendations[category.lower()] = f"Receptas: {recommendation.pavadinimas}"
            else:
                recommendation = random.choice(Product.objects.all())
                recommendations[category.lower()] = f"Produktas: {recommendation.name}"

        # Create DataFrame from recommendations
        df = pd.DataFrame(recommendations.items(), columns=['Category', 'Recommendation'])

        # Save DataFrame to Excel file
        file_path = os.path.join(settings.BASE_DIR, 'individual_rekomendations.xlsx')  # Use BASE_DIR to get the project directory
        df.to_excel(file_path, index=False)

        return file_path

    def handle(self, *args, **kwargs):
        file_path = self.generate_recommendations()

        # Serve the file for download
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=individual_rekomendations.xlsx'
            self.stdout.write(self.style.SUCCESS('Successfully generated recommendations Excel file'))

