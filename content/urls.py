from django.urls import path
from . import views


urlpatterns = [
    path("add_movie", views.addMovie, name="add-movie"),
    path("add_genre", views.addGenre, name="add-genre"),
    path("add_serie", views.addSerie, name="add-serie"),
    path("add_episode", views.addEpisode, name="add-episode"),
    path("<int:pk>/<str:type>/", views.get_content, name="get-content"),
    path("<int:pk>/<str:type>/playing", views.playMovie, name="play-movie"),
    
]