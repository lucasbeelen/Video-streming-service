from .models import Serie,Movie
from usuarios.forms import ReviewForm
from django.contrib.contenttypes.models import ContentType
from usuarios.models import CustomUser,Bookmark, WatchHistory, Review
from django.shortcuts import get_object_or_404


class ContentDetailFacade:
    def __init__(self, user, content_type, pk):
        self.user = user
        self.pk = pk
        self.content_type = content_type

    def get_content_object(self):
        if self.content_type == 'movie':
            return get_object_or_404(Movie, pk=self.pk)
        elif self.content_type == 'serie':
            return get_object_or_404(Serie, pk=self.pk)
        else:
            raise ValueError("Tipo de conteúdo inválido")

    def get_is_bookmarked(self, content):
        content_type = ContentType.objects.get_for_model(content)
        return Bookmark.objects.filter(user=self.user, content_type=content_type, object_id=content.pk).exists()

    def get_reviews(self, content):
        content_type = ContentType.objects.get_for_model(content)
        return Review.objects.filter(content_type=content_type, object_id=content.pk)

    def handle_review_submission(self, request, content):
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = self.user
                review.content_type = ContentType.objects.get_for_model(content)
                review.object_id = content.pk
                review.save()
                return review_form
        return ReviewForm()

    def get_context(self, request):
        content = self.get_content_object()
        is_bookmarked = self.get_is_bookmarked(content)
        reviews = self.get_reviews(content)
        review_form = self.handle_review_submission(request, content)

        context = {
            'content': content,
            'is_bookmarked': is_bookmarked,
            'review_form': review_form,
            'reviews': reviews,
        }

        if isinstance(content, Serie):
            context['episodes'] = content.episodes.all()

        return context
