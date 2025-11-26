from django.views.generic import TemplateView
from .models import Reef, Event, Article

class HomeView(TemplateView):
    """Home page view with featured content and recent activity."""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_articles'] = Article.objects.filter(
            published=True, featured=True
        )[:3]
        context['recent_events'] = Event.objects.select_related('reef')[:5]
        context['reef_count'] = Reef.objects.count()
        context['event_count'] = Event.objects.count()
        return context
