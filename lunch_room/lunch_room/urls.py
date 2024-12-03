from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from lunch_room.utils import activate_account
from lunch_room.views import LunchSessionListView, SignUpView, UserProfileView, RestaurantListView, RestaurantEditView, \
    RestaurantDeleteView, RestaurantCreateView, MealCreateView, MealEditView, MealDeleteView, LunchSessionCreateView, \
    LunchSessionView, LunchSessionEditView, LunchSessionOrderView, LunchSessionSummaryView

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
    path('lunch_session_create', LunchSessionCreateView.as_view(), name='lunch-session-create'),
    path('lunch_session/<int:lunch_session_id>', LunchSessionView.as_view(), name='lunch-session'),
    path('lunch_session_edit/', LunchSessionEditView.as_view(), name='lunch-session-edit'),
    path('lunch_session_order/<int:lunch_session_id>/<int:user_id>/', LunchSessionOrderView.as_view(), name='lunch-session-order'),
    path('lunch_session_summary/<int:lunch_session_id>', LunchSessionSummaryView.as_view(), name='lunch-session-summary')
]