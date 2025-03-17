from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

# from django.contrib.auth.views import LoginView
urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
