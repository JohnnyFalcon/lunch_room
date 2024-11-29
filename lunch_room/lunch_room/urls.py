from django.contrib import admin
from django.urls import path, include

from .views import LunchSessionListView, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', LunchSessionListView.as_view(), name='lunch-session-list'),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),

]