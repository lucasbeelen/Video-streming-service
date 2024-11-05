from .strategies import MovieStrategy, SerieStrategy

def get_strategy(content_type):
    if content_type == 'movie':
        return MovieStrategy()
    elif content_type == 'serie':
        return SerieStrategy()
    else:
        raise ValueError("Tipo de conteúdo inválido.")