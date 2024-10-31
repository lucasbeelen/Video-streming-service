from .models import Movie, Serie, Episode

class ContentFactory:
    @staticmethod
    def create_movie(form):
        if form.is_valid():
            return form.save()  # Salva o objeto diretamente usando form.save()
        return None
    
    @staticmethod
    def create_serie(form):
        if form.is_valid():
            return form.save()  # Salva o objeto diretamente usando form.save()
        return None
    
    @staticmethod
    def create_episode(form):
        if form.is_valid():
            return form.save()  # Salva o objeto diretamente usando form.save()
        return None