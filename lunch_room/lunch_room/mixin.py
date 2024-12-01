from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
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

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        permissions = Permissions(request.user)

        if not permissions.check_view_permissions(self.__class__.__name__):
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