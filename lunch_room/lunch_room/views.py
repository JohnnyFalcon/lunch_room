from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from mixin import BaseMixin, PageTitleMixin


class SignUpView(PageTitleMixin, TemplateView):
    template_name = "registration/signup.html"
    page_title = 'Sign Up'
    success_url = reverse_lazy("login")

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.form_data = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'form_data'):
            context['form_data'] = self.form_data
        return context

    def post(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        errors = {}

        self.form_data = {
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'email': request.POST.get('email', ''),
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=self.form_data['email']).exists():
            errors['email'] = "Ten email jest już zarejestrowany."

        if password != password2:
            errors['password2'] = "Hasła nie są takie same."

        try:
            validate_password(password)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            context['errors'] = errors
            return self.render_to_response(context)

        try:
            _ = User.objects.create_user(
                username=self.form_data['email'],
                email=self.form_data['email'],
                password=password,
                first_name=self.form_data['first_name'],
                last_name=self.form_data['last_name']
            )
            return redirect(self.success_url)
        except Exception as ex:
            context['error'] = "Wystąpił błąd podczas rejestracji. Spróbuj ponownie."
            return self.render_to_response(context)


class IndexView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/index.html'
    page_title = 'Strona Główna'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class LunchSessionListView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/lunch_session_list.html'
    page_title = 'Lista sesji'

    def get_context_data(self, **kwargs):
        context = super(LunchSessionListView, self).get_context_data(**kwargs)
        return context
