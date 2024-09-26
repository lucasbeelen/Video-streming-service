from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from embed_video.fields import EmbedVideoField

# Create your models here.

class Genre(models.Model):
    genre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.genre
    

class Movie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    title = models.CharField(max_length=260)
    duration = models.PositiveIntegerField()
    description = models.TextField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    url = EmbedVideoField()
    thumbnail = models.FileField(upload_to='uploads/thumbnails') 
    date_added = models.DateTimeField(auto_now_add=True)
    classification = models.IntegerField(choices=[
        (0, 'Livre'),
        (10, '10+'),
        (12, '12+'),
        (14, '14+'),
        (16, '16+'),
        (18, '18+')
    ], default=0, help_text="Classificação etária do conteúdo")
    type = models.CharField(max_length=10, default='movie')
    
    def __str__(self):
        return self.title
    

class Serie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.FileField(upload_to='uploads/thumbnails') 
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    classification = models.IntegerField(choices=[
        (0, 'Livre'),
        (10, '10+'),
        (12, '12+'),
        (14, '14+'),
        (16, '16+'),
        (18, '18+')
    ], default=0, help_text="Classificação etária do conteúdo")
    seasons = models.PositiveIntegerField()
    release_year = models.PositiveIntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, default='serie')
    
    def __str__(self):
        return self.title

class Episode(models.Model):
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='episodes')  # Relacionamento de um para muitos com 'Serie'
    title = models.CharField(max_length=255)
    description = models.TextField()
    season = models.PositiveIntegerField()
    episode_number = models.PositiveIntegerField()
    duration = models.IntegerField(blank=True, null=True)
    url = EmbedVideoField()

    def __str__(self):
        return f"{self.title} (Temporada {self.season}, Episódio {self.episode_number})"
    
    