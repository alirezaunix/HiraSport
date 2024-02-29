import os
import csv
import apps
from datetime import datetime
import csv
#from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
from  apps.home.models import Person  # Replace with your actual model

# Get the field names from the model
field_names = [field.name for field in Person._meta.fields]

# Now `field_names` contains a list of field names from your model
print(field_names)
'''

def import_books(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            Person.objects.create(
                title=row['title'],
                author=row['author'],
                published_date=datetime.strptime(
                    row['published_date'], '%Y-%m-%d').date(),
                price=row['price']
            )


if __name__ == '__main__':
    csv_file_path = 'path/to/books.csv'  # Replace with your actual file path
    import_books(csv_file_path)
'''