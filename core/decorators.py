"""
Custom decorators and mixins for ReefGuard application.

Provides role-based access control for views and functions.
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Decorator to restrict access to specific user roles.

    Usage:
        @role_required('admin', 'researcher')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(
                    request,
                    f'Access denied. This feature requires {" or ".join(roles)} role.'
                )
                raise PermissionDenied
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorator to restrict access to admin users only.

    Usage:
        @admin_required
        def admin_only_view(request):
            ...
    """
    return role_required('admin')(view_func)


def researcher_or_admin_required(view_func):
    """
    Decorator to restrict access to researchers and admins.

    Usage:
        @researcher_or_admin_required
        def research_view(request):
            ...
    """
    return role_required('admin', 'researcher')(view_func)


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin for class-based views to restrict access by role.

    Usage:
        class MyView(RoleRequiredMixin, ListView):
            allowed_roles = ['admin', 'researcher']
            ...
    """
    allowed_roles = []

    def test_func(self):
        """Check if user has required role."""
        if not self.allowed_roles:
            return True
        return self.request.user.role in self.allowed_roles

    def handle_no_permission(self):
        """Handle users without required permissions."""
        if self.request.user.is_authenticated:
            messages.error(
                self.request,
                f'Access denied. This feature requires '
                f'{" or ".join(self.allowed_roles)} role.'
            )
            raise PermissionDenied
        return super().handle_no_permission()


class AdminRequiredMixin(RoleRequiredMixin):
    """
    Mixin for class-based views restricted to admins only.

    Usage:
        class AdminOnlyView(AdminRequiredMixin, ListView):
            ...
    """
    allowed_roles = ['admin']


class ResearcherOrAdminMixin(RoleRequiredMixin):
    """
    Mixin for class-based views accessible to researchers and admins.

    Usage:
        class ResearchView(ResearcherOrAdminMixin, CreateView):
            ...
    """
    allowed_roles = ['admin', 'researcher']


class StaffOrOwnerMixin(LoginRequiredMixin):
    """
    Mixin to allow access to staff users or the object owner.

    Usage:
        class EditEventView(StaffOrOwnerMixin, UpdateView):
            owner_field = 'reported_by'  # Field name that contains the owner
            ...
    """
    owner_field = 'user'  # Default field name

    def dispatch(self, request, *args, **kwargs):
        """Check if user is staff or owner before dispatching."""
        obj = self.get_object()
        owner = getattr(obj, self.owner_field, None)

        # Allow if user is admin/researcher or is the owner
        if request.user.role in ['admin', 'researcher'] or owner == request.user:
            return super().dispatch(request, *args, **kwargs)

        messages.error(
            request,
            'You do not have permission to access this resource.'
        )
        raise PermissionDenied
