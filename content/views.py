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
from .strategies import ParentalControlStrategy, NoParentalControlStrategy

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
    favorite_genres = get_similar_content(user)
    watched_content = WatchHistory.objects.filter(user=user)
    bookmarks = Bookmark.objects.filter(user=user)
    watchhistory = WatchHistory.objects.filter(user=user)

    # Seleciona a estratégia de acordo com o controle parental
    if user.parental_control_enabled:
        strategy = ParentalControlStrategy(user, favorite_genres, watched_content)
    else:
        strategy = NoParentalControlStrategy(user, favorite_genres, watched_content)

    # Usa a estratégia para obter dados filtrados
    content = strategy.get_content()
    bookmarks = strategy.get_bookmarks(bookmarks)
    watchhistory = strategy.get_watch_history(watchhistory)
    recommendations = strategy.get_recommendations()

    context = {
        'content': content,
        'bookmarks': bookmarks,
        'watchhistory': watchhistory,
        'recommendations': recommendations
    }
    return render(request, "homeVideos.html", context)

@login_required
def get_content(request, pk, type):
    try:
        facade = ContentDetailFacade(request.user, type, pk)
        context = facade.get_context(request)

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

