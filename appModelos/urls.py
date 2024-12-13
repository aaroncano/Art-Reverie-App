from django.urls import path
from .views import ArtworkList, ArtworkSearchList, CollectionDetailView, RandomArtwork, CollectionListView

# Este archivo se usa para definir las rutas de la API.

urlpatterns = [
    path('artworks', ArtworkList.as_view(), name='artwork-list'),
    path('search/', ArtworkSearchList.as_view(), name='artwork-search-list'),
    path('random/', RandomArtwork.as_view(), name='random-artwork'),
    path('collections/', CollectionListView.as_view(), name='collection-list'),
    path('collections/<int:id>/', CollectionDetailView.as_view(), name='collection-detail'),
]