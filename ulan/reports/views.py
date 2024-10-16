from django.shortcuts import render, redirect
from django.shortcuts import render
from django.db.models import Sum
from main.models import Masterdata
from .forms import ReportForm, Report_allForm, AlluserReportForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    return render(request, "reports/index.html")


def weekly_report(request):
    form = ReportForm()
    report_data = None
    user = None  # Kullanıcıyı burada başlatıyoruz
    status = None
    total_units = 0

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

            # Подсчет общей суммы единиц
            total_units = report_data.aggregate(total=Sum('edinitsa'))['total'] or 0

    return render(request, 'reports/weekly_report.html', {
        'form': form,
        'report_data': report_data,
        'user': user,  # Kullanıcıyı template'e gönderiyoruz
        'status': status,
        'total_units': total_units  # Добавляем общую сумму в контекст
    })

def weekly_report_all(request):
    form = Report_allForm()
    report_data = None
    user = None

    if request.method == "POST":
        form = Report_allForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            # Filtreleme
            if user:
                report_data = Masterdata.objects.filter(
                    created__range=(start_date, end_date),
                    user=user
                )
            else:
                report_data = Masterdata.objects.filter(
                    created__range=(start_date, end_date)
                )

    return render(request, 'reports/weekly_report_all.html', {
        'form': form,
        'report_data': report_data,
        'user': user,
    })

def alluser_report(request):
    form = AlluserReportForm(request.GET or None)
    report_data = []
    status = None
    kroy_no = None
    start_date = None
    end_date = None

    if request.method == 'GET' and form.is_valid():
        status = form.cleaned_data.get('status')
        kroy_no = form.cleaned_data.get('kroy_no')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        filters = {}
        if status:
            filters['status'] = status
        if status:
            filters['kroy_no'] = kroy_no
        if start_date:
            filters['created__gte'] = start_date
        if end_date:
            filters['created__lte'] = end_date

        report_data = (
            Masterdata.objects
            .filter(**filters)
            .values('user__username', 'created', 'user__first_name', 'user__last_name')
            .annotate(total_edinitsa=Sum('edinitsa'), total_price=Sum('price'))
        )


    context = {
        'form': form,
        'report_data': report_data,
        'status': status,
        'kroy_no': kroy_no,
        'start_date': start_date,
        'end_date': end_date,
        #'created': created,
    }
    return render(request, 'reports/alluser_report.html', context)