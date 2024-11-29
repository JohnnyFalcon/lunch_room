from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


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



class CustomLoginRequiredMixin(LoginRequiredMixin):
   login_url = reverse_lazy('login')
   redirect_field_name = 'next'


class BaseMixin(PageTitleMixin, CustomLoginRequiredMixin):
    """
    Containing base Mixins for Views
    """
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)