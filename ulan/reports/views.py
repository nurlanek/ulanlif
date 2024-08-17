from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    return render(request, "reports/index.html")