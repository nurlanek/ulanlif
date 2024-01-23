from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from .models import Kroy, Kroy_detail #Uchastok
from .forms import KroyForm, KroyDetailForm, Masterdata, MasterdataSearchForm, MasterdataForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse_lazy

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

        try:
            edinitsa = int(edinitsa)
        except ValueError:
            edinitsa = 0  # Default value if parsing fails

        # Create a new Masterdata object and save it to the database
        #uchastok = get_object_or_404(Uchastok, pk=uchastok)

        # Get the User instance based on the username
        user = get_object_or_404(User, username=username)

        masterdata = Masterdata(
            kroy_no=kroy_no,
            #uchastok=uchastok,
            edinitsa=edinitsa,
            user=user,  # Assign the User instance
            # Add other fields here as needed
        )
        masterdata.save()

        kroy_record = get_object_or_404(Kroy, kroy_no=kroy_no)
        kroy_record.edinitsa = int(kroy_record.edinitsa or 0) - edinitsa
        kroy_record.save()

        return redirect('masterdata_list')

    return render(request, 'main/kroy/kroy_masterdata.html')

class MasterdataListView(ListView):
    model = Masterdata
    template_name = 'main/mdata/masterdata_list.html'
    context_object_name = 'masterdata_list'

    def get_queryset(self):
        form = MasterdataSearchForm(self.request.GET)
        queryset = Masterdata.objects.filter(is_active=True)

        if form.is_valid():
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            #uchastok_search = form.cleaned_data.get('uchastok_search')
            kroy_no_search = form.cleaned_data.get('kroy_no_search')

            filter_conditions = Q()

            if start_date:
                filter_conditions &= Q(created__gte=start_date)
            if end_date:
                filter_conditions &= Q(created__lte=end_date)
            #if uchastok_search:
                #queryset = queryset.filter(Q(uchastok__name__icontains=uchastok_search))
            if kroy_no_search:
                filter_conditions &= Q(kroy_no__icontains=kroy_no_search)

                # Apply the combined filters
            queryset = queryset.filter(filter_conditions)

        queryset = queryset.order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = MasterdataSearchForm(self.request.GET)
        context['additional_variable'] = 'Some additional value'

        return context

def MdataKroyDetailView(request, kroy_id):
        kroy_instance = get_object_or_404(Masterdata, pk=kroy_id)
        kroy_details = Kroy_detail.objects.filter(kroy=kroy_instance)  # Retrieve related Kroy_detail records

        context = {
            'kroy_instance': kroy_instance,
            'kroy_details': kroy_details,  # Pass the related records to the template
        }
        return render(request, 'main/dmata/dmata_kroy_detail_view.html', context)

class KroyListView(ListView):
    model = Kroy
    template_name = 'main/kroy/kroy_list.html'

    def get_queryset(self):
        # Filter the Kroy objects where is_active is True
        return Kroy.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['uchastok'] = Uchastok.objects.all()
        context['user'] = User.objects.all()

        return context

class KroyCreateView(CreateView):
    model = Kroy
    form_class = KroyForm
    template_name = 'main/kroy/kroy_form.html'
    success_url = reverse_lazy ('kroy-create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kroy_list'] = Kroy.objects.all().order_by('-created')[
                                      :10]  # Add this line to pass the data to the template
        return context
def KroyDetailView(request, kroy_id):
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

class KroyUpdateView(UpdateView):
    model = Kroy
    form_class = KroyForm
    template_name = 'main/kroy/kroy_form.html'
    success_url = '/kroy/'

class KroyDetailListView(ListView):
    model = Kroy_detail
    template_name = 'main/kroy/kroy_detail_list.html'

class KroyDetailCreateView(CreateView):
    model = Kroy_detail
    form_class = KroyDetailForm
    template_name = 'main/kroy/kroy_detail_form.html'
    success_url = reverse_lazy('kroy-detail-create')

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
        edinitsa = request.POST.get('edinitsa')

        # No need to get the username separately; use request.user directly
        user = request.user

        masterdata = Masterdata(
            kroy_no=kroy_no,
            edinitsa=edinitsa,
            user=user,
        )
        masterdata.save()

    context = {
        'masterdata_list': Masterdata.objects.filter(user=request.user),
        'kroy_detail_list': Kroy_detail.objects.filter(user=request.user),
        'user': request.user,
        'kroy_list': Kroy.objects.all(),
    }

    return render(request, 'main/masterdatauser_list.html', context)

