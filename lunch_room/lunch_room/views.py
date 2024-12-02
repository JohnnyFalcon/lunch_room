import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView
from lunch_room.mixin import BaseMixin, PageTitleMixin
from lunch_room.models import Restaurant, Meal


class SignUpView(PageTitleMixin, TemplateView):
    template_name = "registration/signup.html"
    page_title = 'Sign Up'
    success_url = reverse_lazy("login")

    def __init__(self, *args, **kwargs):
        self.form_data = {}
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'form_data'):
            context['form_data'] = self.form_data
        return context

    def post(self, request, *args, **kwargs):

        self.form_data = {
            'first_name': request.POST.get('first_name', ''),
            'last_name': request.POST.get('last_name', ''),
            'email': request.POST.get('email', ''),
        }

        context = self.get_context_data(**kwargs)
        errors = {}

        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(email=self.form_data['email']).exists():
            errors['email'] = ["Ten email jest już zarejestrowany."]

        if password != password2:
            errors['password2'] = ["Hasła nie są takie same."]

        try:
            validate_password(password)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            context['errors'] = errors
            return self.render_to_response(context)

        try:
            user = User.objects.create_user(
                username=self.form_data['email'],
                email=self.form_data['email'],
                password=password,
                first_name=self.form_data['first_name'],
                last_name=self.form_data['last_name'],
                is_active=False
            )

            # Generate confirmation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)

            # Create confirmation link
            confirm_link = reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
            activation_url = f'http://{current_site.domain}{confirm_link}'

            mail_subject = 'Activate your account'
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'activation_url': activation_url,
            })

            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            return redirect('account_activation_sent')

        except Exception as ex:
            context['error'] = "An error occurred during registration."
            return self.render_to_response(context)


class UserProfileView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/user_profile.html'
    page_title = 'Profil użytkownika'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = user.username = request.POST.get('email')

        try:
            user.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, 'Error updating profile.')

        return redirect('profile')


class IndexView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/index.html'
    page_title = 'Strona Główna'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context


class RestaurantListView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/restaurants_list.html'
    page_title = 'Jadłodajnie'

    def get_context_data(self, **kwargs):
        context = super(RestaurantListView, self).get_context_data(**kwargs)
        context['restaurants'] = Restaurant.objects.all()
        return context


class RestaurantEditView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/restaurant_edit.html'


    def get_context_data(self, **kwargs):
        context = super(RestaurantEditView, self).get_context_data(**kwargs)
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        context['page_title'] = restaurant.name if restaurant.name else 'Jadłodajnia'
        context['restaurant'] = restaurant
        return context

    def post(self, request, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, pk=self.kwargs['restaurant_id'])
        restaurant.name = request.POST.get('name')
        restaurant.address = request.POST.get('address')
        restaurant.phone = request.POST.get('phone')
        restaurant.save()
        messages.success(request, 'Jadłodajnia została zaktualizowana.')
        return redirect('restaurant-list')


class RestaurantDeleteView(BaseMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            restaurant_id = request.POST.get('restaurant_id')
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            restaurant.delete()
            messages.success(request, f'Jadłodajnia "{restaurant.name}" została usunięta.')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error'}, status=400)


class RestaurantCreateView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/restaurant_create.html'
    page_title = 'Utwórz jadłodajnie'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            with transaction.atomic():

                restaurant = Restaurant.objects.create(
                    name=data['name'],
                    address=data['address'],
                    phone=data['phone']
                )

                for meal_data in data['meals']:
                    Meal.objects.create(
                        restaurant=restaurant,
                        name=meal_data['name'],
                        price=meal_data['price']
                    )

            messages.success(request, f'Jadłodajnia "{restaurant.name}" została utworzona.')
            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)


class MealCreateView(BaseMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            restaurant = get_object_or_404(Restaurant, pk=data['restaurant_id'])

            Meal.objects.create(
                restaurant=restaurant,
                name=data['name'],
                price=data['price']
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class MealEditView(BaseMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            meal = get_object_or_404(Meal, pk=data['id'])

            meal.name = data['name']
            meal.price = data['price']
            meal.save()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class MealDeleteView(BaseMixin, View):

    def post(self, request, *args, **kwargs):

        try:
            data = json.loads(request.body)
            meal = get_object_or_404(Meal, pk=data['meal_id'])
            meal.delete()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class LunchSessionListView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/lunch_session_list.html'
    page_title = 'Lista sesji'

    def get_context_data(self, **kwargs):
        context = super(LunchSessionListView, self).get_context_data(**kwargs)
        return context
