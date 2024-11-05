from .strategies import MovieStrategy, SerieStrategy, EpisodeStrategy

def get_strategy(content_type):
    if content_type == 'movie':
        return MovieStrategy()
    elif content_type == 'serie':
        return SerieStrategy()
    elif content_type == 'episode':
        return EpisodeStrategy()
    else:
        raise ValueError("Tipo de conteúdo inválido.")