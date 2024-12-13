import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from random import randint
from django.db.models.aggregates import Count
from rest_framework import generics
from django.utils.dateparse import parse_date
import hashlib
from .models import Artwork
from rest_framework.views import APIView
from .serializers import ArtworkSerializer
from django.db.models import Q

from .models import Collection
from .serializers import CollectionSerializer


logger = logging.getLogger(__name__)

# Home

# Se utiliza para crear un carousel con obras de los últimos 7 días en la página de inicio
# Se usa una función hash para seleccionar una obra de arte para cada día y se puedan recuperar siempre las mismas obras para cada día
class ArtworkList(generics.ListAPIView):
    serializer_class = ArtworkSerializer

    def get_queryset(self):
        queryset = Artwork.objects.all()
        date = self.request.query_params.get('date')
        logger.debug(f"Fetching artwork for date: {date}")
        if date and queryset.exists():

            artwork_id = self.hash_date_to_artwork_id(date, queryset.count())

            try:
                return [queryset[artwork_id]]
            except IndexError:
                logger.debug(f"No artwork found for index: {artwork_id}")
                return []
        return queryset
    
    # Convierte fecha en un índice usando hashing.
    def hash_date_to_artwork_id(self, date, count):
        

        date_bytes = date.encode('utf-8')
        hash_object = hashlib.sha256(date_bytes)

        # convierte el hash en un número entero
        hash_digest = hash_object.hexdigest()
        artwork_index = int(hash_digest, 16) % count
        logger.debug(f"Artwork index for date {date}: {artwork_index}")
        return artwork_index
    
############################################################################

# Búsqueda

# Esta vista se usa para buscar obras de arte por título, artista, cultura, país, periodo y tipo.
# Se utiliza en la página de búsqueda
# Se consulta a la base de datos local
# Devuelve una lista de obras de arte que coinciden con los criterios de búsqueda
# en caso de no encontrar ninguna obra, devuelve una lista vacía
class ArtworkSearchList(generics.ListAPIView):
    serializer_class = ArtworkSerializer

    def get_queryset(self):
        queryset = Artwork.objects.all()
        query = self.request.query_params.get('query')
        types = self.request.query_params.get('types')

        if query:
            if types:
                types_list = types.split(',')
                query_filters = Q()
                for type in types_list:
                    if hasattr(Artwork, type):
                        kwargs = {f'{type}__icontains': query}
                        query_filters |= Q(**kwargs)
                queryset = queryset.filter(query_filters)
            else:
                queryset = queryset.none()

        return queryset
    

#Random art

# Esta vista se utiliza para mostrar una obra de arte aleatoria en la página de búsqueda
# Se consulta a la base de datos local y se elige una obra de arte aleatoria mediante un índice aleatorio
# Cada que se carga esta página se muestra una obra de arte diferente
class RandomArtwork(generics.ListAPIView):
    serializer_class = ArtworkSerializer

    def get_queryset(self):
        count = Artwork.objects.count()
        if count == 0:
            return []

        random_index = randint(0, count - 1)
        artwork = Artwork.objects.all()[random_index]
        return [artwork]



############################################################################


# Colecciones

# Colecciones publicas

# Esta vista se utiliza para mostrar las colecciones públicas en la página de colecciones
# Se consulta a la base de datos local
# Devuelve una lista de colecciones públicas, actualmente está limitada a 20 colecciones por tipo para no sobrecargar la página
# pero se planea cambiar esto en el futuro cuando se implemente la paginación
class CollectionListView(APIView):
    def get(self, request):
        max_collections_per_type = 20

        all_collections = Collection.objects.all()

        # Agrupa por tipo
        collections_by_type = {}
        for collection in all_collections:
            if collection.type not in collections_by_type:
                collections_by_type[collection.type] = []
            collections_by_type[collection.type].append(collection)

        # Limita cada grupo a un máximo
        limited_collections = []
        for ctype, collections in collections_by_type.items():
            limited_collections.extend(collections[:max_collections_per_type])

        serializer = CollectionSerializer(limited_collections, many=True)
        return Response(serializer.data)
    
# Colecion por id
class CollectionDetailView(APIView):
    def get(self, request, id):
        collection = Collection.objects.get(pk=id)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)