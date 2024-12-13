from django.core.management.base import BaseCommand
from appModelos.models import Artwork, Collection

# Este script se utiliza para importar las colecciones de los periodos de la base de datos de obras.
# El script crea una colección por cada periodo, y agrega las obras de ese periodo a la colección.
# Para ejecutar el script, se debe usar el comando: python manage.py import_collections_periods

class Command(BaseCommand):
    def handle(self, *args, **options):
        Collection.objects.filter(type='Periodo').delete()

        periodos = Artwork.objects.values_list('period', flat=True).distinct()
        periodos = [periodo for periodo in periodos if periodo] 

        for periodo in periodos:
            collection_name = f'{periodo}'
            collection, created = Collection.objects.get_or_create(
                name=collection_name,
                type='Periodo',
                defaults={'creator': 'Art Reverie'}
            )
            artworks = Artwork.objects.filter(period=periodo)
            collection.artworks.set(artworks)
            collection.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Colección creada: {collection.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Colección actualizada: {collection.name}'))
