from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse


# Create your views here.
def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login (request, user)
            return redirect("home")
        else:
            return render(request, "account/login.html", {
                "error": "имя или пароль неправильно"
            })

    return render(request, "account/login.html")

def register_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, 'account/register.html', {"error": "такой пользователь уже существует"})
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, 'account/register.html', {"error": "такой эл.почта уже существует"})
                else:
                    user = User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname, password=password)
                    user.save()
                    return redirect("login")

        else:
            return render(request, 'account/register.html', {"error":"Пароль не совпадает"})


    return render(request, "account/register.html")

def logout_request(request):
    logout(request)
    return redirect("home")

def user_logout_request(request):
    logout(request)
    return redirect(reverse("main:masterdatauser"))

def masterdata_login(request):
    if request.user.is_authenticated:
        return redirect(reverse("main:masterdatauser"))  # Kullanıcı zaten giriş yapmışsa, home sayfasına yönlendir

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Kullanıcı kimlik doğrulaması
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Başarılı kimlik doğrulaması durumunda giriş yap
            login(request, user)
            return redirect(reverse("main:masterdatauser"))  # masterdatauser sayfasına yönlendir
        else:
            return render(request, "account/masterdata_login.html", {
                "error": "Kullanıcı adı veya şifre yanlış"
            })

    return render(request, "account/masterdata_login.html")