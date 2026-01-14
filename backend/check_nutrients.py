import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('USDA_API_KEY')
url = f'https://api.nal.usda.gov/fdc/v1/food/173945?api_key={api_key}'

response = requests.get(url)
data = response.json()
nutrients = data.get('foodNutrients', [])

print('All energy-related nutrients:')
for n in nutrients:
    name = n.get('nutrient', {}).get('name', '')
    if 'energy' in name.lower():
        print(f"  - '{name}': {n.get('amount')}")
