from django.core.management.base import BaseCommand
from appModelos.models import Artwork, Collection

# importa las colecciones de los departamentos de la base de datos de obras.
# crea una colección por cada departamento, y agrega las obras de ese departamento a la colección.
# Para ejecutar el script, se debe usar el comando: python manage.py import_collections_departments

class Command(BaseCommand):
    def handle(self, *args, **options):
        Collection.objects.filter(type='Departamento').delete()

        departamentos = Artwork.objects.values_list('department', flat=True).distinct()
        departamentos = [departamento for departamento in departamentos if departamento] 

        for departamento in departamentos:
            collection_name = f'{departamento}'
            collection, created = Collection.objects.get_or_create(
                name=collection_name,
                type='Departamento',
                defaults={'creator': 'Art Reverie'}
            )
            artworks = Artwork.objects.filter(department=departamento)
            collection.artworks.set(artworks)
            collection.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f'Colección creada: {collection.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Colección actualizada: {collection.name}'))
