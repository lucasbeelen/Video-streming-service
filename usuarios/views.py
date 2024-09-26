from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from content.models import Movie, Serie
from .models import Bookmark, WatchHistory,CustomUser
from django.contrib import messages

# Create your views here.



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home-view'))

def cadastro_usuario(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, "cadastro.html", {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(form.cleaned_data['password'])  
            user.save()
            return HttpResponseRedirect(reverse('login'))
    
    return render(request, "cadastro.html", {'form': form})

def home(request):
    return render(request, "home.html")

@login_required
def add_bookmark(request, pk, type):
    
    if type == 'movie':
        model = Movie
    elif type == 'serie':
        model = Serie
    else:
        messages.error(request, "Tipo de conteúdo inválido.")
        return redirect('home-videos')
    
    content_object = get_object_or_404(model, pk=pk)
    
    content_type = ContentType.objects.get_for_model(content_object)
    
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=content_object.id,
    )   
    return redirect('get-content', pk=pk, type=type)

@login_required
def remove_bookmark(request, pk, type):
    user = request.user
    
    if type == 'movie':
        model = Movie
    elif type == 'serie':
        model = Serie
    else:
        messages.error(request, "Tipo de conteúdo inválido.")
        return redirect('home-videos')
    
    
    content_object = get_object_or_404(model, pk=pk)
    content_type = ContentType.objects.get_for_model(content_object)
    
    bookmark = Bookmark.objects.filter(user=user, content_type=content_type, object_id=content_object.pk)
    
    if bookmark.exists():
        bookmark.delete()
        
    return redirect('get-content', pk=pk, type=type)

def add_watch_to_history(request, pk , type):
    user = request.user
    
    if type == 'movie':
        model = Movie
    elif type == 'episode':
        model = Serie
    else:
        messages.error(request, "Tipo de conteúdo inválido.")
        return redirect('home-videos')
    
    content_object = get_object_or_404(model, pk=pk)
    content_type = ContentType.objects.get_for_model(content_object)
    
    watchHistory, created = WatchHistory.objects.get_or_create(
        user=request.user,
        content_type=content_type,
        object_id=content_object.id,
    )   
    if type == 'movie':
        return redirect('play-movie', pk=pk, type=type)
    elif type == 'serie':
        model = Serie 
    return redirect('play-movie', pk=pk, type=type)

@login_required
def parental_control(request):
    user = request.user
    
    user.parental_control_enabled = not user.parental_control_enabled
    user.save()
    
    return redirect('home-videos')
