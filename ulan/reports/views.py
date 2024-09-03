from django.shortcuts import render, redirect
from django.shortcuts import render
from django.db.models import Sum
from main.models import Masterdata
from .forms import ReportForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    return render(request, "reports/index.html")


def weekly_report(request):
    form = ReportForm()
    report_data = None

    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            status = form.cleaned_data['status']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Filtreleme
            report_data = Masterdata.objects.filter(
                created__range=(start_date, end_date),
                user=user if user else None,
                status=status if status else None
            )

    return render(request, 'reports/weekly_report.html', {'form': form, 'report_data': report_data})