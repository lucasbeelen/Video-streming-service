from django.db import transaction, IntegrityError
from .models import Movie, Serie, Episode, Genre
from .forms import MovieForm, SerieForm, EpisodeForm, GenreForm


class ContentFactory:
    @staticmethod
    def create_content(content_type, post_data=None, files_data=None):
        form_class = ContentFactory.get_form_class(content_type)
        if post_data:
            form = form_class(post_data, files_data)
        else:
            form = form_class()

        return form

    @staticmethod
    def get_form_class(content_type):
        if content_type == 'movie':
            return MovieForm
        elif content_type == 'serie':
            return SerieForm
        elif content_type == 'episode':
            return EpisodeForm
        elif content_type == 'genre':
            return GenreForm
        else:
            raise ValueError("Tipo de conteúdo inválido")