from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .forms import MovieForm, GenreForm,SerieForm,EpisodeForm
from .models import Movie,Serie,Episode
from django.contrib.auth.decorators import login_required
from usuarios.models import CustomUser,Bookmark, WatchHistory, Review
from django.contrib.contenttypes.models import ContentType
from usuarios.forms import ReviewForm
from django.db import IntegrityError,transaction
from django.contrib.admin.views.decorators import staff_member_required
from .factories import ContentFactory

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
    else:  # POST
        form = MovieForm(request.POST, request.FILES)
        movie = ContentFactory.create_movie(form)
        if movie:
            return HttpResponse('Novo filme adicionado com sucesso!')

    context = {'form': form}
    return render(request, "add_movie.html", context)


@staff_member_required
def addSerie(request):
    
    if request.method == 'GET':
        form = SerieForm()
    else:  # POST
        form = SerieForm(request.POST, request.FILES)
        serie = ContentFactory.create_serie(form)
        if serie:
            return redirect('add-episode')

    context = {'form': form}
    return render(request, "add_serie.html", context)


@staff_member_required
def addEpisode(request):
    if request.method == 'GET':
        form = EpisodeForm()
    else:  # POST
        form = EpisodeForm(request.POST)
        episode = ContentFactory.create_episode(form)
        if episode:
            if 'add_another' in request.POST:
                form = EpisodeForm() 
            else:
                return HttpResponse('Episódio adicionado com sucesso!')

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
    user = request.user
    
    if type == 'movie':
        movie = get_object_or_404(Movie, pk=pk)
        content_type = ContentType.objects.get_for_model(movie)
        is_bookmarked = Bookmark.objects.filter(user=user, content_type=content_type, object_id=movie.pk).exists()
        reviews = Review.objects.filter(content_type=content_type, object_id=movie.pk)
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.content_type = content_type
                review.object_id = movie.pk
                review.save()
        else:
            review_form = ReviewForm()
        
        template_name = 'movieDetail.html'
        context = {'content': movie,
                   'is_bookmarked': is_bookmarked,
                   'review_form': review_form,
                   'reviews': reviews,
                }
        
    elif type == 'serie':
        serie = get_object_or_404(Serie, pk=pk)
        episodes = serie.episodes.all()  
        content_type = ContentType.objects.get_for_model(serie)
        is_bookmarked = Bookmark.objects.filter(user=user, content_type=content_type, object_id=serie.pk).exists()
        reviews = Review.objects.filter(content_type=content_type, object_id=serie.pk)
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.content_type = content_type
                review.object_id = serie.pk
                review.save()
        else:
            review_form = ReviewForm()
        template_name = 'serieDetail.html'
        context = {
            'content': serie,
            'episodes': episodes,
            'is_bookmarked': is_bookmarked,
            'review_form': review_form,
            'reviews': reviews,
        }
    return render(request, template_name, context)

@login_required
def playMovie(request, pk, type):
    if request.user.subscription_level != 'premium':
        messages.error(request, 'Você precisa de uma assinatura premium para assistir este conteúdo.')

    if type == 'movie':
        item = get_object_or_404(Movie, pk=pk)
    elif type == 'episode':
        item = get_object_or_404(Episode, pk=pk)
    return render(request, 'playVideo.html', {'content': item})

