from django.core.management.base import BaseCommand
import requests
from appModelos.models import Artwork
import random
import time


# Este script se utiliza para importar los datos de las obras de la API de The Metropolitan Museum of Art.
# Actualmente importa unicamente las pinturas, pero se puede modificar para importar otros tipos de obras.
# Los datos se guardan en la base de datos local, en la tabla Artwork.
# Para ejecutar el script, se debe usar el comando:
# python manage.py import_artworks


class Command(BaseCommand):
    def fetch_url(self, url, max_retries=3, timeout=5):
        """ Realiza solicitudes HTTP con reintento en caso de fallos. """
        for i in range(max_retries):
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                self.stdout.write(self.style.WARNING(f'Retry {i+1} for URL: {url}'))
                time.sleep(2)  
        raise

    def handle(self, *args, **options):
        Artwork.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All existing artworks have been deleted.'))

        search_url = 'https://collectionapi.metmuseum.org/public/collection/v1/search?hasImages=true&medium=Paintings&q=*'
        
        try:
            search_response = self.fetch_url(search_url)
            search_data = search_response.json()

            if search_data['total'] > 0:
                object_ids = search_data['objectIDs']
                for object_id in object_ids:
                    details_url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}'
                    try:
                        details_response = self.fetch_url(details_url)
                        details_data = details_response.json()

                        if details_data.get('primaryImage') or (details_data.get('additionalImages') and len(details_data['additionalImages']) > 0):
                            if not details_data.get('primaryImage') and details_data.get('additionalImages'):
                                details_data['primaryImage'] = details_data['additionalImages'][0]
                            
                            Artwork.objects.create(
                                object_id=object_id,
                                title=details_data.get('title'),
                                artist=details_data.get('artistDisplayName'),
                                date=details_data.get('objectDate'),
                                dimensions=details_data.get('dimensions'),
                                medium=details_data.get('medium'),
                                culture=details_data.get('culture'),
                                period=details_data.get('period'),
                                country=details_data.get('country'),
                                department=details_data.get('department'),
                                accession_number=details_data.get('accessionNumber'),
                                accession_year=details_data.get('accessionYear'),
                                primary_image=details_data.get('primaryImage'),
                                object_url=details_data.get('objectURL')
                            )

                            self.stdout.write(self.style.SUCCESS(f'Successfully imported artwork ID: {object_id}'))

                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Failed to fetch details for object ID {object_id}: {str(e)}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch search data: {str(e)}'))
