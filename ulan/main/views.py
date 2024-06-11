from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from .models import (Kroy, Kroy_detail, Operations, Product_type,
                     Operation_code, Operation_list, Kroy_operation_code)
from .forms import (KroyForm, KroyDetailForm, Masterdata, MasterdataSearchForm,
                    OperationCodeForm, OperationListForm, KroyOperationCodeForm,
                    MasterdataForm)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse





def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "main/index.html")

"""def create_masterdata(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, 'main/kroy/kroy_masterdata.html')
"""
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

"""@login_required
def MdataKroyDetailView(request, kroy_id):
    if not request.user.is_authenticated:
        return redirect("login")
        
        return render(request, 'main/dmata/dmata_kroy_detail_view.html', context)
"""
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


class KroyUpdateView(LoginRequiredMixin, UpdateView):
    model = Kroy
    form_class = KroyForm
    template_name = 'main/kroy/kroy_form.html'
    success_url = '/kroy/'
    login_url = '/login/'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

@login_required
def KroyDetailView(request, kroy_id):
    if not request.user.is_authenticated:
        return redirect("login")

    kroy_instance = get_object_or_404(Kroy, pk=kroy_id)
    kroy_details = Kroy_detail.objects.filter(kroy=kroy_instance)
    kroy_list = Kroy.objects.all()
    kroy_operation_codes = Kroy_operation_code.objects.filter(kroy=kroy_instance).order_by('operation_code')

    context = {
        'objects':kroy_list,
        'kroy_instance': kroy_instance,
        'kroy_details': kroy_details,
        'kroy_operation_codes': kroy_operation_codes,  # Yeni eklenen liste
    }
    return render(request, 'main/kroy/kroy_detail_view.html', context)

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




def operation_code_create(request):
    if request.method == 'POST':
        form = OperationCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('operation_code_list')  # operation_code_list view'ine yönlendir
    else:
        form = OperationCodeForm()
    return render(request, 'main/operation/operation_code_create.html', {'form': form})

def operation_code_update(request, pk):
    operation_code = get_object_or_404(Operation_code, pk=pk)
    if request.method == 'POST':
        form = OperationCodeForm(request.POST, instance=operation_code)
        if form.is_valid():
            form.save()
            return redirect('operation_code_list')  # operation_code_list view'ine yönlendir
    else:
        form = OperationCodeForm(instance=operation_code)
    return render(request, 'main/operation/operation_code_update.html', {'form': form})

def operation_code_delete(request, pk):
    operation_code = get_object_or_404(Operation_code, pk=pk)
    if request.method == 'POST':
        operation_code.delete()
        return redirect('operation_code_list')  # Silme işlemi gerçekleştiğinde listeleme sayfasına yönlendir
    return render(request, 'main/operation/operation_code_delete.html', {'object': operation_code})
def operation_code_list(request):
    operation_codes = Operation_code.objects.all()
    return render(request, 'main/operation/operation_code_list.html', {'operation_codes': operation_codes})


# Existing Operation_code views...

def operation_list_detail(request, operation_code_id):
    operation_code = get_object_or_404(Operation_code, id=operation_code_id)
    operation_lists = Operation_list.objects.filter(operation_code=operation_code)
    total_price = sum(operation.price for operation in operation_lists)
    return render(request, 'main/operation/operation_list_detail.html', {
        'operation_code': operation_code,
        'operation_lists': operation_lists,
        'total_price': total_price,
    })

def operation_list_create(request, operation_code_id):
    operation_code = get_object_or_404(Operation_code, id=operation_code_id)
    if request.method == "POST":
        form = OperationListForm(request.POST)
        if form.is_valid():
            operation_list = form.save(commit=False)
            operation_list.operation_code = operation_code
            operation_list.save()
            return redirect('operation_list_detail', operation_code_id=operation_code.id)
    else:
        form = OperationListForm()
    return render(request, 'main/operation/operation_list_form.html', {'form': form, 'operation_code': operation_code})

def operation_list_update(request, pk):
    operation_list = get_object_or_404(Operation_list, pk=pk)
    if request.method == "POST":
        form = OperationListForm(request.POST, instance=operation_list)
        if form.is_valid():
            form.save()
            return redirect('operation_list_detail', operation_code_id=operation_list.operation_code.id)
    else:
        form = OperationListForm(instance=operation_list)
    return render(request, 'main/operation/operation_list_form.html', {'form': form})

def operation_list_delete(request, pk):
    operation_list = get_object_or_404(Operation_list, pk=pk)
    operation_code_id = operation_list.operation_code.id
    operation_list.delete()
    return redirect('operation_list_detail', operation_code_id=operation_code_id)


def OperationListView(request, operation_code_id):
    operation_code_instance = get_object_or_404(Operation_code, pk=operation_code_id)
    operation_lists = Operation_list.objects.filter(operation_code=operation_code_instance)
    total_price = sum(operation.price for operation in operation_lists if operation.price)

    context = {
        'operation_code': operation_code_instance,
        'operation_lists': operation_lists,
        'total_price': total_price,
    }
    return render(request, 'main/operation/operation_list_view.html', context)

def example_view(request):
    kroys = Kroy.objects.all()
    status_list = [option[0] for option in Masterdata.OPTION_CHOICES]
    return render(request, 'main/mdata/example.html', {'kroys': kroys, 'status_list': status_list})



def kroy_operation_code_list(request):
    codes = Kroy_operation_code.objects.all()
    return render(request, 'main/opercode/kroy_operation_code_list.html', {'codes': codes})

def kroy_operation_code_create(request):
    if request.method == 'POST':
        form = KroyOperationCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kroy_operation_code_list')
    else:
        form = KroyOperationCodeForm()
    return render(request, 'main/opercode/kroy_operation_code_form.html', {'form': form})

def kroy_operation_code_edit(request, pk):
    code = get_object_or_404(Kroy_operation_code, pk=pk)
    if request.method == 'POST':
        form = KroyOperationCodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            return redirect('kroy_operation_code_list')
    else:
        form = KroyOperationCodeForm(instance=code)
    return render(request, 'main/opercode/kroy_operation_code_form.html', {'form': form})

def kroy_operation_code_delete(request, pk):
    code = get_object_or_404(Kroy_operation_code, pk=pk)
    if request.method == 'POST':
        code.delete()
        return redirect('kroy_operation_code_list')
    return render(request, 'main/opercode/kroy_operation_code_confirm_delete.html', {'code': code})


def get_operation_codes(request):
    kroy_no = request.GET.get('kroy_no')
    if kroy_no:
        operations = Kroy_operation_code.objects.filter(kroy__kroy_no=kroy_no).values('operation_code', 'operation_code__title')
        data = [{'code': op['operation_code'], 'title': op['operation_code__title']} for op in operations]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def get_operation_list(request):
    operation_code = request.GET.get('operation_code')
    if operation_code:
        operations = Operation_list.objects.filter(operation_code=operation_code).values('id', 'title')
        data = [{'id': op['id'], 'title': op['title']} for op in operations]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def get_operation_price(request):
    operation_id = request.GET.get('operation_id')
    if operation_id:
        try:
            operation = Operation_list.objects.get(id=operation_id)
            return JsonResponse({'price': operation.price})
        except Operation_list.DoesNotExist:
            return JsonResponse({'price': 0})
    return JsonResponse({'price': 0})

def MasterdatauserListView(request):
    if not request.user.is_authenticated:
        return redirect('masterdata_login')

    if request.method == 'POST':
        kroy_no = request.POST.get('kroy_no')
        operation_code = request.POST.get('type_product')
        operations = request.POST.get('operations')
        price = request.POST.get('price', '0')
        edinitsa = request.POST.get('edinitsa')
        status = request.POST.get('status')
        user = request.user

        operation_code_instance = Operation_code.objects.get(id=operation_code)
        masterdata = Masterdata(
            kroy_no=kroy_no,
            operation_code=operation_code_instance,
            operations=operations,
            price=price,
            edinitsa=edinitsa,
            status=status,
            user=user
        )
        masterdata.save()
        return HttpResponseRedirect('/masterdatauser/')

    else:
        context = {
            'masterdata_list': Masterdata.objects.filter(user=request.user),
            'kroy_detail_list': Kroy_detail.objects.filter(user=request.user),
            'user': request.user,
            'kroy_list': Kroy.objects.all(),
            'status_list': [option[0] for option in Masterdata.OPTION_CHOICES],
        }
        return render(request, 'main/mdata/masterdatauser.html', context)
