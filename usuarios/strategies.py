from abc import ABC, abstractmethod
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from content.models import Movie, Serie

class ContentStrategy(ABC):
    @abstractmethod
    def get_content_object(self, pk):
        pass

    @abstractmethod
    def get_content_type(self):
        pass

class MovieStrategy(ContentStrategy):
    def get_content_object(self, pk):
        return get_object_or_404(Movie, pk=pk)

    def get_content_type(self):
        return ContentType.objects.get_for_model(Movie)

class SerieStrategy(ContentStrategy):
    def get_content_object(self, pk):
        return get_object_or_404(Serie, pk=pk)

    def get_content_type(self):
        return ContentType.objects.get_for_model(Serie)