from django import forms
from .models import Movie,Genre,Serie,Episode


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['genre', 'title', 'classification', 'duration', 'description', 'url', 'thumbnail', 'release_year'] 
        
        
class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['genre', 'title', 'classification', 'seasons', 'description', 'thumbnail', 'release_year']  

class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['serie', 'title', 'description', 'season', 'episode_number', 'duration', 'url']
        
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['genre']
        
