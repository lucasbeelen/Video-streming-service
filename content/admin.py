from django.contrib import admin
from .models import Movie, Genre, Serie, Episode
# Register your models here.

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Serie)
admin.site.register(Episode)