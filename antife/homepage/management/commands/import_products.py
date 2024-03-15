import pandas as pd
from homepage.models import Product

# Load the .csv data set
data = pd.read_csv('C:\\Users\\Rokan\\Documents\\GitHub\\AntiFE\\Produktai_data_lt.csv')

# Iterate over each row in the data set
for index, row in data.iterrows():
    # Create a new Product instance for each row
    product = Product(
        name=row['Name'],
        calories=row['Calories'],
        total_fat=row['Total_fat'],
        fiber=row['Fiber'],
        protein=row['Protein'],
        phenylalanine=row['Phenylalanine']
    )
    # Save the new Product instance to the database
    product.save()