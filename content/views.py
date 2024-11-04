from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import MovieForm, GenreForm,SerieForm,EpisodeForm
from .models import Movie,Serie,Episode
from django.contrib.auth.decorators import login_required
from usuarios.models import CustomUser,Bookmark, WatchHistory, Review
from django.db import IntegrityError,transaction
from django.contrib.admin.views.decorators import staff_member_required
from .facade import ContentDetailFacade


# Create your views here.
def get_similar_content(user):
    watched_content = WatchHistory.objects.filter(user=user)
    favorite_genres = set()
    for watch in watched_content:
        if isinstance(watch.content_object, Movie):
            favorite_genres.add(watch.content_object.genre)
        elif isinstance(watch.content_object, Serie):
            favorite_genres.add(watch.content_object.genre)
    return favorite_genres


@staff_member_required
def addMovie(request):
    
    if request.method == 'GET':
        form = MovieForm()
        
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('novo filme adicionado com sucesso!')
                  
    context = {'form': form}
    return render(request, "add_movie.html", context)


@staff_member_required
def addSerie(request):
    
    if request.method == 'GET':
        form = SerieForm()
        
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add-episode')
                  
    context = {'form': form}
    return render(request, "add_serie.html", context)


@staff_member_required
def addEpisode(request):
    if request.method == 'GET':
        form = EpisodeForm()
        
    if request.method == 'POST':
        form = EpisodeForm(request.POST)
        if form.is_valid():
            form.save()
            if 'add_another' in request.POST:
                form = EpisodeForm() 
            else:
                return HttpResponse('episodio adicionado com sucesso!')
                              
    context = {'form': form}
    return render(request, "add_episode.html", context)


@staff_member_required
def addGenre(request):
    if request.method == 'GET':
        form = GenreForm()
        
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                return HttpResponse('Novo gênero adicionado com sucesso!')
            except IntegrityError:
                return HttpResponse('Erro ao adicionar o gênero! Verifique se há problemas com as referências.')
                  
    context = {'form': form}
    return render(request, "add_genre.html", context)

@login_required
def homeVideos(request):
    user = request.user
    favorite_genres = get_similar_content(request.user)
    watched_content = WatchHistory.objects.filter(user=user)
    bookmarks = Bookmark.objects.filter(user=user)
    watchhistory = WatchHistory.objects.filter(user=user)
    if user.parental_control_enabled:
        movies =  Movie.objects.filter(classification__lte = user.age)
        series = Serie.objects.filter(classification__lte = user.age)
        content = list(movies) + list(series)
        
        recommended_movies = Movie.objects.filter(genre__in=favorite_genres, classification__lte = user.age).exclude(
        id__in=[watch.content_object.id for watch in watched_content if isinstance(watch.content_object, Movie)]
        )
    
        recommended_series = Serie.objects.filter(genre__in=favorite_genres,classification__lte = user.age).exclude(
        id__in=[watch.content_object.id for watch in watched_content if isinstance(watch.content_object, Serie)]
        )
        recommendations = list(recommended_movies) + list(recommended_series)
        
        
        filtered_bookmarks = []
        for bookmark in bookmarks:
            if isinstance(bookmark.content_object, Movie) and bookmark.content_object.classification <= user.age:
                filtered_bookmarks.append(bookmark)
            elif isinstance(bookmark.content_object, Serie) and bookmark.content_object.classification <= user.age:
                filtered_bookmarks.append(bookmark)
        bookmarks = filtered_bookmarks
        
        
        filtered_watchhistory = []
        for watch in watchhistory:
            if isinstance(watch.content_object, Movie) and watch.content_object.classification <= user.age:
                filtered_watchhistory.append(watch)
            elif isinstance(watch.content_object, Serie) and watch.content_object.classification <= user.age:
                filtered_watchhistory.append(watch)
        watchhistory = filtered_watchhistory
                
        
    else:
        movies = Movie.objects.all()
        series = Serie.objects.all()
        content = list(movies) + list(series)
        
        bookmarks = Bookmark.objects.filter(user=user)
        watchhistory = WatchHistory.objects.filter(user=user)
        recommended_movies = Movie.objects.filter(genre__in=favorite_genres).exclude(
        id__in=[watch.content_object.id for watch in watched_content if isinstance(watch.content_object, Movie)]
        )
    
        recommended_series = Serie.objects.filter(genre__in=favorite_genres).exclude(
        id__in=[watch.content_object.id for watch in watched_content if isinstance(watch.content_object, Serie)]
        )
        recommendations = list(recommended_movies) + list(recommended_series)
        
        
    
    
    context={
         'content': content,
         'bookmarks': bookmarks,
         'watchhistory': watchhistory,
         'recomandations': recommendations
    }
    return render(request, "homeVideos.html", context)

@login_required
def get_content(request, pk, type):
    try:
        facade = ContentDetailFacade(request.user, type, pk)
        context = facade.get_context(request)

        # Seleciona o template correto com base no tipo de conteúdo
        template_name = 'movieDetail.html' if type == 'movie' else 'serieDetail.html'
        return render(request, template_name, context)

    except ValueError:
        return HttpResponse("Tipo de conteúdo inválido", status=400)

@login_required
def playMovie(request, pk, type):
    if request.user.subscription_level != 'premium':
        messages.error(request, 'Você precisa de uma assinatura premium para assistir este conteúdo.')

    if type == 'movie':
        item = get_object_or_404(Movie, pk=pk)
    elif type == 'episode':
        item = get_object_or_404(Episode, pk=pk)
    return render(request, 'playVideo.html', {'content': item})

