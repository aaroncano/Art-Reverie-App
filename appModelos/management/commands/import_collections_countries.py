from django.core.management.base import BaseCommand
from appModelos.models import Artwork, Collection

# Este script se utiliza para importar las colecciones de los países de la base de datos de obras.
# El script crea una colección por cada país, y agrega las obras de ese país a la colección.
# Para ejecutar el script, se debe usar el comando: python manage.py import_collections_countries

class Command(BaseCommand):
    def handle(self, *args, **options):
        Collection.objects.filter(type='Pais').delete()

        paises = Artwork.objects.values_list('country', flat=True).distinct()
        paises = [pais for pais in paises if pais]

        for pais in paises:
            collection_name = f'{pais}'
            collection, created = Collection.objects.get_or_create(
                name=collection_name,
                type='Pais',
                defaults={'creator': 'Art Reverie'}
            )
            artworks = Artwork.objects.filter(country=pais)
            collection.artworks.set(artworks)
            collection.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Colección creada: {collection.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Colección actualizada: {collection.name}'))
