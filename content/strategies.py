from .models import Movie, Serie
from abc import ABC, abstractmethod

class RecommendationStrategy(ABC):
    def __init__(self, user, favorite_genres, watched_content):
        self.user = user
        self.favorite_genres = favorite_genres
        self.watched_content = watched_content

    @abstractmethod
    def get_content(self):
        pass

    @abstractmethod
    def get_bookmarks(self, bookmarks):
        pass

    @abstractmethod
    def get_watch_history(self, watchhistory):
        pass

    @abstractmethod
    def get_recommendations(self):
        pass

class ParentalControlStrategy(RecommendationStrategy):
    def get_content(self):
        movies = Movie.objects.filter(classification__lte=self.user.age)
        series = Serie.objects.filter(classification__lte=self.user.age)
        return list(movies) + list(series)

    def get_bookmarks(self, bookmarks):
        filtered_bookmarks = []
        for bookmark in bookmarks:
            if isinstance(bookmark.content_object, Movie) and bookmark.content_object.classification <= self.user.age:
                filtered_bookmarks.append(bookmark)
            elif isinstance(bookmark.content_object, Serie) and bookmark.content_object.classification <= self.user.age:
                filtered_bookmarks.append(bookmark)
        return filtered_bookmarks

    def get_watch_history(self, watchhistory):
        filtered_watchhistory = []
        for watch in watchhistory:
            if isinstance(watch.content_object, Movie) and watch.content_object.classification <= self.user.age:
                filtered_watchhistory.append(watch)
            elif isinstance(watch.content_object, Serie) and watch.content_object.classification <= self.user.age:
                filtered_watchhistory.append(watch)
        return filtered_watchhistory

    def get_recommendations(self):
        recommended_movies = Movie.objects.filter(genre__in=self.favorite_genres, classification__lte=self.user.age).exclude(
            id__in=[watch.content_object.id for watch in self.watched_content if isinstance(watch.content_object, Movie)]
        )
        recommended_series = Serie.objects.filter(genre__in=self.favorite_genres, classification__lte=self.user.age).exclude(
            id__in=[watch.content_object.id for watch in self.watched_content if isinstance(watch.content_object, Serie)]
        )
        return list(recommended_movies) + list(recommended_series)

class NoParentalControlStrategy(RecommendationStrategy):
    def get_content(self):
        return list(Movie.objects.all()) + list(Serie.objects.all())

    def get_bookmarks(self, bookmarks):
        return bookmarks

    def get_watch_history(self, watchhistory):
        return watchhistory

    def get_recommendations(self):
        recommended_movies = Movie.objects.filter(genre__in=self.favorite_genres).exclude(
            id__in=[watch.content_object.id for watch in self.watched_content if isinstance(watch.content_object, Movie)]
        )
        recommended_series = Serie.objects.filter(genre__in=self.favorite_genres).exclude(
            id__in=[watch.content_object.id for watch in self.watched_content if isinstance(watch.content_object, Serie)]
        )
        return list(recommended_movies) + list(recommended_series)