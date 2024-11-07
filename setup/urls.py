
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from content.views import homeVideos

urlpatterns = [
    path("", homeVideos, name="home-videos"),
    path('admin/', admin.site.urls),
    path('usuario/',include("usuarios.urls")),
    path("content/", include("content.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
