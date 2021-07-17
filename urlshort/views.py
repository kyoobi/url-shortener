from django.db import reset_queries
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import date, datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import random, string

# Create your views here.


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
    else:
        form = UserCreationForm()
    
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

        return HttpResponse(status=403)

    else:
        form = AuthenticationForm()
    return render(request, "signin.html", {"form": form})



def signout(request):
    logout(request)
    return redirect("home")


@login_required
def createShortURL(request):
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
            )
            s.save()
            return render(request, "urlcreated.html", {"chars": random_chars})
        else:
            return render(request, "home.html")
    else:
        form = CreateNewShortURL()
        context = {"form": form}
        return render(request, "create.html", context)


def redirectURL(request, url):
    current_obj = ShortURL.objects.filter(short_url=url)
    print(request)
    if len(current_obj) == 0:
        return render(request, "pagenotfound.html")
    context = {"obj": current_obj[0]}
    return render(request, "redirect.html", context)
