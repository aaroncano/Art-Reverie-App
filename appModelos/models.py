from django.db import models

class Artwork(models.Model):
    object_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    artist = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=100, null=True, blank=True)
    dimensions = models.CharField(max_length=255, null=True, blank=True)
    medium = models.CharField(max_length=255, null=True, blank=True)
    culture = models.CharField(max_length=255, null=True, blank=True)
    period = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    accession_number = models.CharField(max_length=100, null=True, blank=True)
    accession_year = models.CharField(max_length=100, null=True, blank=True)
    primary_image = models.URLField(null=True, blank=True)
    object_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Collection(models.Model):
    name = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)  # Cambiar esto a ForeignKey cuando se implementen usuarios
    artworks = models.ManyToManyField('Artwork', related_name='collections')
    type = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    artwork = models.ForeignKey('Artwork', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # Cuando implemente usuarios, añadir: user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reseña de {self.artwork.title}'

class Like(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    # Cuando implemente usuarios, añadir: user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Like en {self.artwork.title}'
