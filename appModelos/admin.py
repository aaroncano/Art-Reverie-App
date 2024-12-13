from django.contrib import admin
from .models import Artwork, Collection, Review, Like

admin.site.register(Artwork)
admin.site.register(Collection)
admin.site.register(Review)
admin.site.register(Like)