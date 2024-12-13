from django.core.management.base import BaseCommand
from appModelos.models import Artwork, Collection

# se usa para importar las colecciones de las culturas de la base de datos de obras.
# El script crea una colección por cada cultura, y agrega las obras de esa cultura a la colección.
# Para ejecutar el script, se debe usar el comando: python manage.py import_collections_cultures

class Command(BaseCommand):
    def handle(self, *args, **options):
        Collection.objects.filter(type='Cultura').delete()

        culturas = Artwork.objects.values_list('culture', flat=True).distinct()
        culturas = [cultura for cultura in culturas if cultura]

        for cultura in culturas:
            collection_name = f'{cultura}'
            collection, created = Collection.objects.get_or_create(
                name=collection_name,
                type='Cultura',
                defaults={'creator': 'Art Reverie'}
            )
            artworks = Artwork.objects.filter(culture=cultura)
            collection.artworks.set(artworks)
            collection.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Colección creada: {collection.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Colección actualizada: {collection.name}'))
