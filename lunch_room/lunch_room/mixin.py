from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse

from .permissions import Permissions


class PageTitleMixin:
    """
    Adds class variable "page_title" which will be added to context and then set as page title in base.html.
    """
    page_title = None

    def get_page_title(self, *args, **kwargs) -> str:
        return self.page_title if isinstance(self.page_title, str) else ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        return context


class PermissionMixin(LoginRequiredMixin):

    def get_view_permission_context(self, request, *args, **kwargs):
        """
        This method should be overwritten in View's as necessary
        """
        return {}

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            next_url = request.path
            return redirect(f'{reverse("login")}?next={next_url}')

        permissions = Permissions(request.user)
        permission_context = self.get_view_permission_context(request, *args, **kwargs)

        if not permissions.check_view_permissions(self.__class__.__name__, permission_context):
            raise PermissionDenied("You don't have permission to access this page")

        self.permissions = permissions.base_permissions()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permissions'] = self.permissions
        return context


class BaseMixin(PermissionMixin, PageTitleMixin, LoginRequiredMixin):
    """
    Containing base Mixins for Views
    """
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)