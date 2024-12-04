import datetime
import json

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import TemplateView

from django.conf import settings
from lunch_room.mixin import BaseMixin, PageTitleMixin
from lunch_room.models import Restaurant, Meal, LunchSession, OrderGroup, LunchSessionOrderItem


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

            is_active = True if settings.DEBUG else False

            user = User.objects.create_user(
                username=self.form_data['email'],
                email=self.form_data['email'],
                password=password,
                first_name=self.form_data['first_name'],
                last_name=self.form_data['last_name'],
                is_active=is_active
            )

            if not settings.DEBUG:

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
            else:
                return redirect(self.success_url)

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
        context['lunch_sessions'] = LunchSession.objects.filter(participants=self.request.user.id).order_by('-session_end_time')
        return context


class LunchSessionCreateView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/lunch_session_create.html'
    page_title = 'Utwórz sesje'

    def get_context_data(self, **kwargs):
        context = super(LunchSessionCreateView, self).get_context_data(**kwargs)

        context['available_users'] = User.objects.exclude(id=self.request.user.id)
        context['order_groups'] = OrderGroup.objects.all()
        context['restaurants'] = Restaurant.objects.all().values('id', 'name')

        return context

    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        restaurant_id = request.POST.get('restaurant')
        delivery_time = timezone.datetime.strptime(request.POST.get('delivery_time'), '%Y-%m-%dT%H:%M')
        session_end_time = timezone.datetime.strptime(request.POST.get('session_end_time'), '%Y-%m-%dT%H:%M')

        try:

            lunch_session = LunchSession.objects.create(
                name=name,
                restaurant_id=restaurant_id,
                delivery_time=delivery_time,
                session_end_time=session_end_time,
                status=LunchSession.ACTIVE,
                creator=request.user
            )

            lunch_session.add_manager(request.user)

            for user_id in request.POST.getlist('participants[]'):
                try:
                    user = User.objects.get(id=user_id)
                    lunch_session.add_member(user)

                    current_site = get_current_site(request)

                    lunch_session_url = f'http://{current_site.domain}{reverse("lunch-session", kwargs={"lunch_session_id": lunch_session.id})}'

                    if not settings.DEBUG:
                        message = render_to_string('lunch_room/email_templates/session_invitation.html', {
                            'user': user,
                            'lunch_session': lunch_session,
                            'creator': request.user,
                            'lunch_session_url': lunch_session_url
                        })
                        email = EmailMessage(
                            'Zaproszenie do sesji zamawiania',
                            message,
                            to=[user.email]
                        )
                        email.send()
                except User.DoesNotExist:
                    continue

            group_ids = request.POST.getlist('order_groups[]')
            for group_id in group_ids:
                try:
                    group = OrderGroup.objects.get(id=group_id)
                    for user in group.users.all():
                        if user != request.user:
                            lunch_session.add_member(user)
                except OrderGroup.DoesNotExist:
                    continue

            return redirect('lunch-session', lunch_session_id=lunch_session.id)

        except Exception as e:
            context = self.get_context_data()
            context['error'] = str(e)
            return self.render_to_response(context)


class LunchSessionView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/lunch_session_details.html'
    page_title = 'Lunch Session Details'

    def get_view_permission_context(self, request, *args, **kwargs):
        return {
            'lunch_session_id': self.kwargs['lunch_session_id']
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lunch_session = get_object_or_404(LunchSession, pk=self.kwargs['lunch_session_id'])
        current_user = self.request.user
        is_manager = lunch_session.get_managers().filter(id=current_user.id).exists()
        is_session_active = lunch_session.is_active()
        user_order = {
            'orders': lunch_session.session_orders.filter(user=current_user),
            'total': lunch_session.get_user_order_total(current_user)
        }
        has_order = user_order['orders'].exists()

        users_orders = None
        if is_manager:
            users_orders = []
            for order in lunch_session.session_orders.exclude(user=current_user):
                if not any(d['user'] == order.user for d in users_orders):
                    users_orders.append({
                        'user': order.user,
                        'orders': lunch_session.session_orders.filter(user=order.user),
                        'total': lunch_session.get_user_order_total(order.user)
                    })

        context.update({
            'page_title': lunch_session.name or 'Sesja',
            'lunch_session': lunch_session,
            'has_order': has_order,
            'user_order': user_order,
            'users_orders': users_orders,
            'is_manager': is_manager,
            'meals': lunch_session.restaurant.meals.all(),
            'available_users': User.objects.exclude(id=lunch_session.creator.id),
            'order_groups': OrderGroup.objects.all(),
            'restaurants': Restaurant.objects.all(),
            'is_session_active': is_session_active
        })

        return context


class LunchSessionEditView(BaseMixin, View):

    def get_view_permission_context(self, request, *args, **kwargs):
        return {
            'lunch_session_id': self.request.POST.get('lunch_session_id')
        }

    def post(self, request, *args, **kwargs):
        lunch_session = get_object_or_404(LunchSession, pk=request.POST.get('lunch_session_id'))
        try:
            delivery_time = datetime.datetime.strptime(request.POST.get('delivery_time'), '%Y-%m-%dT%H:%M')
            session_end_time = datetime.datetime.strptime(request.POST.get('session_end_time'), '%Y-%m-%dT%H:%M')
            time_now = datetime.datetime.now()
            if lunch_session.status == LunchSession.CLOSED and session_end_time > time_now:
                lunch_session.status = LunchSession.ACTIVE
            lunch_session.name = request.POST.get('name')
            lunch_session.restaurant_id = request.POST.get('restaurant')
            lunch_session.delivery_time = delivery_time
            lunch_session.session_end_time = session_end_time
            lunch_session.save()

            current_participants = set(lunch_session.participants.exclude(id=request.user.id).values_list('id', flat=True))
            new_participants = set(map(int, request.POST.getlist('participants[]')))

            for user_id in current_participants - new_participants:
                if user_id != request.user.id:
                    lunch_session.participants.remove(User.objects.get(id=user_id))

            for user_id in new_participants - current_participants:
                if user_id != request.user.id:
                    lunch_session.add_member(User.objects.get(id=user_id))

            for group_id in request.POST.getlist('order_groups[]'):
                group = OrderGroup.objects.get(id=group_id)
                for user in group.users.all():
                    if user.id != request.user.id:
                        lunch_session.add_member(user)

            return JsonResponse({'status': 'success', 'message': 'Sesja zaktualizowana'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class LunchSessionOrderView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/lunch_session_order.html'
    page_title = 'Edycja zamówienia'


    def get_view_permission_context(self, request, *args, **kwargs):
        return {
            'lunch_session_id': self.kwargs['lunch_session_id'],
            'user_id': self.kwargs['user_id']
        }


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lunch_session = get_object_or_404(LunchSession, pk=self.kwargs['lunch_session_id'])
        user = get_object_or_404(User, pk=self.kwargs['user_id'])

        user_orders = lunch_session.session_orders.filter(user=user)
        existing_quantities = {
            order.meal.id: order.quantity
            for order in user_orders
        }

        context.update({
            'lunch_session': lunch_session,
            'user': user,
            'meals': lunch_session.restaurant.meals.all(),
            'existing_quantities': existing_quantities,
            'user_orders': user_orders,
            'order_total': lunch_session.get_user_order_total(user),
        })
        return context

    def post(self, request, *args, **kwargs):
        lunch_session = get_object_or_404(LunchSession, pk=self.kwargs['lunch_session_id'])
        user = get_object_or_404(User, pk=self.kwargs['user_id'])

        lunch_session.session_orders.filter(user=user).delete()

        new_orders = []
        for key, value in request.POST.items():
            if key.startswith('meal_') and value and int(value) > 0:
                meal_id = int(key.split('_')[1])
                quantity = int(value)
                meal = get_object_or_404(Meal, id=meal_id, restaurant=lunch_session.restaurant)

                order = LunchSessionOrderItem(
                    lunch_session=lunch_session,
                    user=user,
                    meal=meal,
                    quantity=quantity,
                    total_price=meal.price * quantity
                )
                new_orders.append(order)

        if new_orders:
            LunchSessionOrderItem.objects.bulk_create(new_orders)

        messages.success(request, 'Zamówienie zostało zaktualizowane.')
        return redirect('lunch-session', lunch_session_id=lunch_session.id)


class LunchSessionSummaryView(BaseMixin, TemplateView):
    template_name = 'lunch_room/pages/lunch_session_summary.html'
    page_title = 'Podsumowanie sesji'

    def get_view_permission_context(self, request, *args, **kwargs):
        return {
            'lunch_session_id': self.kwargs['lunch_session_id']
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lunch_session = get_object_or_404(LunchSession, pk=self.kwargs['lunch_session_id'])

        users_orders = []
        for user in lunch_session.participants.all():
            orders = lunch_session.session_orders.filter(user=user)
            if orders.exists():
                users_orders.append({
                    'user': user,
                    'orders': orders,
                    'total': sum(order.total_price for order in orders)
                })

        all_meals_summary = {}
        total_session_price = 0

        for order in lunch_session.session_orders.all():
            meal_key = order.meal.id
            if meal_key not in all_meals_summary:
                all_meals_summary[meal_key] = {
                    'meal': order.meal,
                    'total_quantity': 0,
                    'total_price': 0
                }
            all_meals_summary[meal_key]['total_quantity'] += order.quantity
            all_meals_summary[meal_key]['total_price'] += order.total_price
            total_session_price += order.total_price

        context.update({
            'lunch_session': lunch_session,
            'users_orders': users_orders,
            'all_meals_summary': all_meals_summary.values(),
            'total_session_price': total_session_price,
        })
        return context