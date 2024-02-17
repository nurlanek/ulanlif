from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from .models import Kroy, Kroy_detail, Operations
from .forms import KroyForm, KroyDetailForm, Masterdata, MasterdataSearchForm, MasterdataForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from django.contrib import messages


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "main/index.html")

def create_masterdata(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        kroy_no = request.POST.get('kroy_no')
        edinitsa = request.POST.get('edinitsa')
        username = request.POST.get('user')  # Get the username

        # Get the User instance based on the username
        user = get_user_model().objects.get(username=username)  # Kullanıcı nesnesini almak için değişiklik yaptım

        masterdata = Masterdata(
            kroy_no=kroy_no,
            edinitsa=edinitsa,
            user=user,
        )
        masterdata.save()

        kroy_record = get_object_or_404(Kroy, kroy_no=kroy_no)
        kroy_record.save()

        return redirect('masterdata_list')

    return render(request, 'main/kroy/kroy_masterdata.html')

class MasterdataListView(LoginRequiredMixin, ListView):

    model = Masterdata
    template_name = 'main/mdata/masterdata_list.html'
    context_object_name = 'masterdata_list'
    login_url = '/login/'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

    def get_queryset(self):
        form = MasterdataSearchForm(self.request.GET)
        queryset = Masterdata.objects.filter(is_active=True)

        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            #uchastok_search = form.cleaned_data.get('uchastok_search')
            kroy_no_search = form.cleaned_data.get('kroy_no_search')
            user = form.cleaned_data.get('user')

            filter_conditions = Q()

            if start_date:
                filter_conditions &= Q(created__gte=start_date)
            if end_date:
                filter_conditions &= Q(created__lte=end_date)
            #if uchastok_search:
                #queryset = queryset.filter(Q(uchastok__name__icontains=uchastok_search))
            if kroy_no_search:
                filter_conditions &= Q(kroy_no__icontains=kroy_no_search)
            if user:
                filter_conditions &= Q(user__username__icontains=user)

                # Apply the combined filters
            queryset = queryset.filter(filter_conditions)

        queryset = queryset.order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MasterdataSearchForm(self.request.GET)
        context['additional_variable'] = 'Some additional value'

        return context

@login_required
def MdataKroyDetailView(request, kroy_id):
    if not request.user.is_authenticated:
        return redirect("login")
        kroy_instance = get_object_or_404(Masterdata, pk=kroy_id)
        kroy_details = Kroy_detail.objects.filter(kroy=kroy_instance)  # Retrieve related Kroy_detail records

        context = {
            'kroy_instance': kroy_instance,
            'kroy_details': kroy_details,  # Pass the related records to the template
        }
        return render(request, 'main/dmata/dmata_kroy_detail_view.html', context)

class KroyListView(LoginRequiredMixin, ListView):
    model = Kroy
    template_name = 'main/kroy/kroy_list.html'
    login_url = '/login/'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

    def get_queryset(self):
        # Filter the Kroy objects where is_active is True
        return Kroy.objects.filter(is_active=True).order_by('-id')[:100]



class KroyCreateView(LoginRequiredMixin, CreateView):
    model = Kroy
    form_class = KroyForm
    template_name = 'main/kroy/kroy_form.html'
    success_url = reverse_lazy ('kroy-create')
    login_url = '/login/'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kroy_list'] = Kroy.objects.all().order_by('-created')[:10]  # Add this line to pass the data to the template
        return context

@login_required
def KroyDetailView(request, kroy_id):
    if not request.user.is_authenticated:
        return redirect("login")

    kroydetil_instance = Kroy_detail.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = KroyDetailForm(request.POST, instance=kroydetil_instance)
        if form.is_valid():
            form.save()
    else:
        form = KroyDetailForm(instance=kroydetil_instance)

    kroy_instance = get_object_or_404(Kroy, pk=kroy_id)
    kroy_details = Kroy_detail.objects.filter(kroy=kroy_instance)

    context = {
        'form': form,
        'kroy_instance': kroy_instance,
        'kroy_details': kroy_details,
    }
    return render(request, 'main/kroy/kroy_detail_view.html', context)

class KroyUpdateView(LoginRequiredMixin, UpdateView):
    model = Kroy
    form_class = KroyForm
    template_name = 'main/kroy/kroy_form.html'
    success_url = '/kroy/'
    login_url = '/login/'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

class KroyDetailListView(LoginRequiredMixin, ListView):
    model = Kroy_detail
    template_name = 'main/kroy/kroy_detail_list.html'
    login_url = '/login/'
    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_kroys = Kroy_detail.objects.order_by('-created')[:30]  # Son 10 kaydı al
        print(latest_kroys)
        context['latest_kroys'] = latest_kroys  # Son 10 kaydı context'e ekle
        return context

class KroyDetailCreateView(LoginRequiredMixin, CreateView):
    model = Kroy_detail
    form_class = KroyDetailForm
    template_name = 'main/kroy/kroy_detail_form.html'
    success_url = reverse_lazy('kroy-detail-create')
    login_url = '/login/'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kroy_detail_list'] = Kroy_detail.objects.all().order_by('-created')[:10]  # Add this line to pass the data to the template
        return context

class KroyDetailUpdateView(UpdateView):
    model = Kroy_detail
    form_class = KroyDetailForm
    template_name = 'main/kroy/kroy_detail_form.html'
    success_url = '/kroy-detail/'


@login_required
def MasterdatauserListView(request):

    if request.method == 'POST':
        kroy_no = request.POST.get('kroy_no')
        status = request.POST.get('status', 'звершень')
        edinitsa = request.POST.get('edinitsa')
        operations = request.POST.get('operations')

        # No need to get the username separately; use request.user directly
        user = request.user

        masterdata = Masterdata(
            operations=operations,
            status=status,
            kroy_no=kroy_no,
            edinitsa=edinitsa,
            user=user,
        )
        masterdata.save()

        # Get the related Kroy record
        related_kroy = Kroy.objects.get(kroy_no=kroy_no)
        # Now you can use 'related_kroy' to access the details of the related Kroy record

    context = {
        'masterdata_list': Masterdata.objects.filter(user=request.user),
        'kroy_detail_list': Kroy_detail.objects.filter(user=request.user),
        'user': request.user,
        'kroy_list': Kroy.objects.all(),
        'status_list': [option[0] for option in Masterdata.OPTION_CHOICES],
    }

    return render(request, 'main/masterdatauser_list.html', context)

def get_operations(request):
    kroy_no = request.GET.get('kroy_no')
    operations = Operations.objects.filter(kroy__kroy_no=kroy_no).values('id', 'name')
    return JsonResponse(list(operations), safe=False)


@login_required
def KroyOperationsView(request, kroy_id):
    if not request.user.is_authenticated:
        return redirect("login")


    kroy_instance = get_object_or_404(Kroy, pk=kroy_id)
    kroy_operations = Operations.objects.filter(kroy=kroy_instance)

    context = {
        'kroy_instance': kroy_instance,
        'kroy_operations': kroy_operations,
    }
    return render(request, 'main/kroy/kroy_operations_list.html', context)
