from usuarios.models import WatchHistory
from content.models import Movie, Serie

def get_similar_content(user):
    watched_content = WatchHistory.objects.filter(user=user)
    favorite_genres = set()
    for watch in watched_content:
        if isinstance(watch.content_object, Movie):
            favorite_genres.add(watch.content_object.genre)
        elif isinstance(watch.content_object, Serie):
            favorite_genres.add(watch.content_object.genre)
    return favorite_genres