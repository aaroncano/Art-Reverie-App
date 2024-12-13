from django.core.management.base import BaseCommand
from appModelos.models import Artwork, Collection

# Este script se utiliza para importar las colecciones de los artistas de la base de datos de obras.
# El script crea una colección por cada artista, y agrega las obras de ese artista a la colección.
# Para ejecutar el script, se debe usar el comando: python manage.py import_collections_artists


class Command(BaseCommand):
    def handle(self, *args, **options):
        Collection.objects.all().delete()
        artistas = Artwork.objects.values_list('artist', flat=True).distinct()
        artistas = [artista for artista in artistas if artista]

        for artista in artistas:
            collection_name = f'{artista}'
            collection, created = Collection.objects.get_or_create(
                name=collection_name,
                type='Artista',
                defaults={'creator': 'Art Reverie'}
            )
            artworks = Artwork.objects.filter(artist=artista)
            collection.artworks.set(artworks)
            collection.save()
            if created:
                self.stdout.write(f'Colección creada: {collection.name}')
            else:
                self.stdout.write(f'Colección actualizada: {collection.name}')