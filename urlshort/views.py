from django.db import reset_queries
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import ShortURL
from .forms import CreateNewShortURL, CustomUserCreationForm
from datetime import date, datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import random, string
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    return render(request, "home.html")


@login_required
def deleteURL(request):
    ShortURL.objects.filter(short_url=request.POST["shortlink"]).delete()
    messages.info(request, "Your link has been deleted successfully!")
    return redirect("dashboard")


@login_required
def dashboard(request):
    if request.method == "POST":
        ShortURL.objects.filter(short_url=request.POST["shortlink"]).update(
            original_url=request.POST["link"]
        )
        messages.info(request, "Your link has been edited successfully!")

    links_list = ShortURL.objects.filter(user=request.user)

    return render(request, "dashboard.html", {"links_list": links_list})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        else:
            username = request.POST["username"]
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists !")
                return redirect("register")
            messages.info(request, "Weak Password !")
            return redirect("register")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


def signin(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.info(request, "INVALID DETAILS !")
        return redirect("signin")

    else:
        form = AuthenticationForm()
    return render(request, "signin.html", {"form": form})


def signout(request):
    logout(request)
    return redirect("home")


def createShortURL(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = CreateNewShortURL(request.POST)
            if form.is_valid():
                original_website = form.cleaned_data["original_url"]
                random_chars_list = list(string.ascii_letters)
                random_chars = ""
                for i in range(6):
                    random_chars += random.choice(random_chars_list)
                while len(ShortURL.objects.filter(short_url=random_chars)) != 0:
                    for i in range(6):
                        random_chars += random.choice(random_chars_list)
                d = datetime.now()
                s = ShortURL(
                    original_url=original_website,
                    short_url=random_chars,
                    time_date_created=d,
                    user=request.user,
                )
                s.save()
                return render(request, "urlcreated.html", {"chars": random_chars})
            else:
                messages.info(request, "INVALID URL!")
                return redirect("create")
        else:
            form = CreateNewShortURL()
            context = {"form": form}
            return render(request, "create.html", context)

    return redirect("signin")


def redirectURL(request, url):
    current_obj = ShortURL.objects.filter(short_url=url)
    print(request)
    if len(current_obj) == 0:
        return render(request, "pagenotfound.html")

    context = {"obj": current_obj[0]}
    return render(request, "redirect.html", context)
