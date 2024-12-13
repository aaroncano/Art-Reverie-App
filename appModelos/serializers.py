from rest_framework import serializers
from .models import Artwork
from .models import Collection

class ArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'



class CollectionSerializer(serializers.ModelSerializer):
    artworks = ArtworkSerializer(many=True)

    class Meta:
        model = Collection
        fields = '__all__'
        