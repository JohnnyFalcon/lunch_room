from django.contrib.auth.mixins import LoginRequiredMixin


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


class BaseMixin(PageTitleMixin, LoginRequiredMixin):
    """
    Containing base Mixins for Views
    """
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)