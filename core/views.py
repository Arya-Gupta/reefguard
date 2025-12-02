"""
Views for ReefGuard application.

Implements class-based views for:
- Home page
- Reef list and detail
- Event list and detail
- Article list and detail
- Forms (pollution report, coral sighting, contact)
- User authentication
- Image gallery
- User profile and dashboard
- Data export
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView, DetailView, CreateView, FormView, TemplateView, UpdateView
)
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import csv
from datetime import datetime
from .models import Reef, Event, Article, ImageGallery, CustomUser, ReefBookmark
from .forms import (
    UserRegistrationForm, PollutionReportForm, CoralSightingForm,
    ContactForm, ImageUploadForm
)
from .decorators import (
    RoleRequiredMixin, AdminRequiredMixin, ResearcherOrAdminMixin
)
class PollutionReportCreateView(LoginRequiredMixin, CreateView):
    """
    Form view for submitting pollution reports.
    """
    model = Event
    form_class = PollutionReportForm
    template_name = 'core/pollution_report_form.html'
    success_url = reverse_lazy('event_list')
 
    def form_valid(self, form):
        form.instance.reported_by = self.request.user
        form.instance.event_type = 'pollution'
        messages.success(
            self.request,
            'Pollution report submitted successfully. Thank you!'
        )
        return super().form_valid(form)
class EventDetailView(DetailView):
    """
    Detail view for individual event.
    """
    model = Event
    template_name = 'core/event_detail.html'
    context_object_name = 'event'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['gallery_items'] = event.gallery_items.all()
        return context
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

class ReefListView(ListView):
    """
    List view for all reefs with search, filtering, and sorting.
    Supports filtering by region and health status.s
    """
    model = Reef
    template_name = 'core/reef_list.html'
    context_object_name = 'reefs'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()

        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(country__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Filter by region
        region = self.request.GET.get('region', '')
        if region:
            queryset = queryset.filter(region=region)

        # Filter by health status
        health = self.request.GET.get('health', '')
        if health:
            queryset = queryset.filter(health_status=health)

        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort in ['name', '-name', 'area_km2', '-area_km2', 'health_status', '-health_status', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)

        # Store filters in session
        self.request.session['last_reef_filters'] = {
            'search': search_query,
            'region': region,
            'health': health,
        }

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Reef.REGION_CHOICES
        context['health_statuses'] = [
            ('excellent', 'Excellent'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('poor', 'Poor'),
            ('critical', 'Critical'),
        ]
        context['current_filters'] = self.request.GET
        context['current_sort'] = self.request.GET.get('sort', '-created_at')

        # Recently viewed reefs
        viewed_reef_ids = self.request.session.get('viewed_reefs', [])
        if viewed_reef_ids:
            context['recently_viewed'] = Reef.objects.filter(id__in=viewed_reef_ids)[:5]

        return context

class ReefDetailView(DetailView):
    """
    Detail view for individual reef.
    Shows reef info, related events, and gallery.
    """
    model = Reef
    template_name = 'core/reef_detail.html'
    context_object_name = 'reef'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reef = self.get_object()
        context['events'] = reef.events.all()[:10]
        context['gallery_items'] = reef.gallery_items.all()[:8]

        # Track last viewed reef in session
        if 'viewed_reefs' not in self.request.session:
            self.request.session['viewed_reefs'] = []

        viewed_reefs = self.request.session['viewed_reefs']
        reef_id = reef.id
        if reef_id in viewed_reefs:
            viewed_reefs.remove(reef_id)
        viewed_reefs.insert(0, reef_id)
        self.request.session['viewed_reefs'] = viewed_reefs[:10]  # Keep last 10
        self.request.session.modified = True

        return context

class ArticleListView(ListView):
    """
    List view for published articles with search and filtering.
    """
    model = Article
    template_name = 'core/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.filter(published=True)

        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )

        # Filter by category
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category=category)

        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort in ['title', '-title', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Article.CATEGORY_CHOICES
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        return context


class ArticleDetailView(DetailView):
    """
    Detail view for individual article.
    """
    model = Article
    template_name = 'core/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        return Article.objects.filter(published=True)

class EventListView(ListView):
    """
    List view for all events with filtering and sorting.
    """
    model = Event
    template_name = 'core/event_list.html'
    context_object_name = 'events'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().select_related('reef', 'reported_by')

        # Filter by event type
        event_type = self.request.GET.get('event_type', '')
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        # Filter by severity
        severity = self.request.GET.get('severity', '')
        if severity:
            queryset = queryset.filter(severity=severity)

        # Filter by year
        year = self.request.GET.get('year', '')
        if year:
            queryset = queryset.filter(event_date__year=year)

        # Filter by resolved status
        resolved = self.request.GET.get('resolved', '')
        if resolved in ['true', 'false']:
            queryset = queryset.filter(resolved=(resolved == 'true'))

        # Sorting
        sort = self.request.GET.get('sort', '-event_date')
        if sort in ['event_date', '-event_date', 'severity', '-severity', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_types'] = Event.EVENT_TYPE_CHOICES
        context['severities'] = Event.SEVERITY_CHOICES

        # Get dynamic list of years from events
        years = Event.objects.dates('event_date', 'year', order='DESC')
        context['years'] = [date.year for date in years]

        context['current_filters'] = self.request.GET
        context['current_sort'] = self.request.GET.get('sort', '-event_date')
        return context

class CustomPasswordResetView(PasswordResetView):
    """
    Password reset request view.
    """
    template_name = 'core/password_reset.html'
    email_template_name = 'core/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
 
    def form_valid(self, form):
        messages.info(
            self.request,
            'Password reset email has been sent if the email exists in our system.'
        )
        return super().form_valid(form)

class BookmarkListView(LoginRequiredMixin, ListView):
    """
    View to display user's bookmarked reefs.
    """
    model = ReefBookmark
    template_name = 'core/bookmarks.html'
    context_object_name = 'bookmarks'
    paginate_by = 12
 
    def get_queryset(self):
        """Get bookmarks for current user."""
        return ReefBookmark.objects.filter(
            user=self.request.user
        ).select_related('reef')
 
 
def bookmark_toggle(request, reef_id):
    """
    Toggle bookmark status for a reef (AJAX endpoint).
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
 
    reef = get_object_or_404(Reef, pk=reef_id)
 
    bookmark, created = ReefBookmark.objects.get_or_create(
        user=request.user,
        reef=reef
    )
 
    if not created:
        # Bookmark exists, so remove it
        bookmark.delete()
        bookmarked = False
        message = f'Removed {reef.name} from bookmarks'
    else:
        bookmarked = True
        message = f'Added {reef.name} to bookmarks'
 
    messages.success(request, message)
 
    return JsonResponse({
        'bookmarked': bookmarked,
        'message': message
    })
