# File: <your_app>/management/commands/generate_recommendations.py

import os
import random
import openpyxl
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.http import HttpResponse
from homepage.models import Receptai, Product
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

class Command(BaseCommand):
    help = 'Generates Excel file for recommendations'

    def generate_recommendations(self):
        categories = ['Pusryčiai', 'Pietus', 'Vakarienė', 'Papildomai']
        recommendations = {}

        # Add a recommendation for the "Pusryčiai" category
        recommendation = random.choice(Receptai.objects.filter(visible=True))
        recommendations['Pusryčiai'] = f"Receptas: {recommendation.pavadinimas}"

        for category in categories[1:]:
            if random.choice([True, False]):  # Randomly choose between a recipe or a product
                recommendation = random.choice(Receptai.objects.filter(visible=True))
                recommendations[category.lower()] = f"Receptas: {recommendation.pavadinimas}"
            else:
                recommendation = random.choice(Product.objects.all())
                recommendations[category.lower()] = f"Produktas: {recommendation.name}"

        # Create DataFrame from recommendations
        df = pd.DataFrame(recommendations.items(), columns=['Category', 'Recommendation'])

        # Load the existing Excel file
        file_path = os.path.join(settings.BASE_DIR, 'rekomendacijos.xlsx')
        wb = load_workbook(filename=file_path)

        # Get the existing sheet named "Individualios_rek"
        try:
            ws = wb['Individualios_rek']
        except KeyError:
            # Create a new sheet named "Individualios_rek" if it doesn't exist
            ws = wb.create_sheet("Individualios_rek")

        # Clear the existing sheet
        ws.cell(row=1, column=1, value="").fill = openpyxl.styles.PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

        # Write the DataFrame to the sheet
        for row_num, (_, row) in enumerate(df.iterrows(), start=2):  # Start from row 2
            for col_num, value in enumerate(row):
                ws.cell(row=row_num, column=col_num + 1, value=value)

        # Apply some formatting to the header
        header_font = Font(bold=True)
        for col_num, _ in enumerate(df.columns):
            ws.cell(row=1, column=col_num + 1, value=df.columns[col_num]).font = header_font

        # Save the updated Excel file
        wb.save(filename=file_path)

        return file_path

    def handle(self, *args, **kwargs):
        file_path = self.generate_recommendations()

        # Serve the file for download
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=individual_rekomendations.xlsx'
            self.stdout.write(self.style.SUCCESS('Successfully generated recommendations Excel file'))

