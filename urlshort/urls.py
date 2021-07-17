from django.urls import path
from .views import dashboard, home, createShortURL, redirectURL, register, signin, signout

urlpatterns = [
    path("", home, name="home"),
    path("create/", createShortURL, name="create"),
    path("register/", register, name="register"),
    path("signin/", signin, name="signin"),
    path("signout/", signout, name="signout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("<str:url>", redirectURL, name="redirectURL"),
]
