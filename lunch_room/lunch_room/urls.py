from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from lunch_room.utils import activate_account
from lunch_room.views import LunchSessionListView, SignUpView, UserProfileView, RestaurantListView, RestaurantEditView, \
    RestaurantDeleteView, RestaurantCreateView, MealCreateView, MealEditView, MealDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', LunchSessionListView.as_view(), name='lunch-session-list'),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('account-activation-sent/', TemplateView.as_view(template_name='registration/account_activation_sent.html'),
         name='account_activation_sent'),
    path('account-activation-complete/', TemplateView.as_view(template_name='registration/activation_complete.html'),
         name='activation_complete'),
    path('account-activation-invalid/', TemplateView.as_view(template_name='registration/activation_invalid.html'),
         name='activation_invalid'),
    path('restaurants/', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurant/<int:restaurant_id>', RestaurantEditView.as_view(), name='restaurant-edit'),
    path('restaurant-delete/', RestaurantDeleteView.as_view(), name='restaurant-delete'),
    path('restaurant-create/', RestaurantCreateView.as_view(), name='restaurant-create'),
    path('meal-create/', MealCreateView.as_view(), name='meal-create'),
    path('meal-edit/', MealEditView.as_view(), name='meal-edit'),
    path('meal-delete/', MealDeleteView.as_view(), name='meal-delete'),
]