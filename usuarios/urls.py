from django.urls import path
from django.contrib.auth import login
from django.contrib.auth import views as authviews 
from . import views

urlpatterns = [
    path("login/", authviews.LoginView.as_view(template_name='login.html'), name='login'),
    path("home/", views.home, name="home-view"),
    path("cadastro/", views.cadastro_usuario, name="cadastro-usuario"),
    path("logout", views.logout_view, name="logout"),
    path("<int:pk>/<str:type>/add_bookmark", views.add_bookmark, name="add-bookmark"),
    path("<int:pk>/<str:type>/remove_bookmark", views.remove_bookmark, name="remove-bookmark"),
    path("<int:pk>/<str:type>/add_to_watchHistory", views.add_watch_to_history, name="add-to-watchHistory"),
    path("parental_control/", views.parental_control, name="parental-control"),
]
