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
from .utils import get_similar_content
from .factories import ContentFactory

# Create your views here.
@staff_member_required
def addMovie(request):
    return add_content(request, 'movie', success_message='Novo filme adicionado com sucesso!')

@staff_member_required
def addSerie(request):
    return add_content(request, 'serie', success_message='Nova série adicionada com sucesso!', redirect_url='add-episode')

@staff_member_required
def addEpisode(request):
    return add_content(request, 'episode', success_message='Episódio adicionado com sucesso!', allow_add_another=True)

@staff_member_required
def addGenre(request):
    return add_content(request, 'genre', success_message='Novo gênero adicionado com sucesso!')

def add_content(request, content_type, success_message, redirect_url=None, allow_add_another=False):
    form = ContentFactory.create_content(content_type, request.POST if request.method == 'POST' else None, request.FILES if request.method == 'POST' else None)
    
    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                form.save()
            if allow_add_another and 'add_another' in request.POST:
                form = ContentFactory.create_content(content_type)  # Reset form for new entry
            else:
                return redirect(redirect_url) if redirect_url else HttpResponse(success_message)
        except IntegrityError:
            return HttpResponse('Erro ao salvar o conteúdo! Verifique as referências.')
    
    return render(request, f"add_{content_type}.html", {'form': form})

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

