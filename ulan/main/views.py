from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import (Kroy, Kroy_detail, Operation_code, Operation_list, Kroy_operation_code)
from .forms import (KroyForm, KroyDetailForm, Masterdata, MasterdataSearchForm,
                    OperationCodeForm, OperationListForm, KroyOperationCodeForm,)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.http import Http404




#@permission_required('main.add_operationcode', raise_exception=True)
def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "main/index.html")

def index1(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "main/index1.html")
# --- Master data alani basi ---
class MasterdataListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):

    model = Masterdata
    template_name = 'main/mdata/masterdata_list.html'
    context_object_name = 'masterdata_list'
    login_url = '/login/'
    permission_required = 'main.view_masterdata'

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
# --- Masterdata alani sonu ---

# --- Kroy basi ---
class KroyListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Kroy
    template_name = 'main/kroy/kroy_list.html'
    login_url = '/login/'
    permission_required = 'main.view_kroy'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

    def get_queryset(self):
        # Filter the Kroy objects where is_active is True
        return Kroy.objects.filter(is_active=True).order_by('-id')[:100]

class KroyCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Kroy
    form_class = KroyForm
    template_name = 'main/kroy/kroy_form.html'
    success_url = reverse_lazy ('kroy-create')
    login_url = '/login/'
    permission_required = 'app_name.view_kroy'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kroy_list'] = Kroy.objects.all().order_by('-created')[:10]  # Add this line to pass the data to the template
        return context


class KroyUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Kroy
    form_class = KroyForm
    template_name = 'main/kroy/kroy_form.html'
    success_url = '/kroy/'
    login_url = '/login/'
    permission_required = 'app_name.view_kroy'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')
# --- Kroy sonu ---
# ---Kroy detail basi ---
@login_required
@permission_required('main.add_view', raise_exception=True)
def KroyDetailView(request, kroy_id):
    if not request.user.is_authenticated:
        return redirect("login")

    kroy_instance = get_object_or_404(Kroy, pk=kroy_id)
    kroy_details = Kroy_detail.objects.filter(kroy=kroy_instance)
    kroy_list = Kroy.objects.all()
    kroy_operation_codes = Kroy_operation_code.objects.filter(kroy=kroy_instance).order_by('operation_code')
    # Stuk sütununun toplamını hesapla
    stuk_total = kroy_details.aggregate(stuk_sum=Sum('stuk'))['stuk_sum'] or 0
    context = {
        'objects':kroy_list,
        'kroy_instance': kroy_instance,
        'kroy_details': kroy_details,
        'kroy_operation_codes': kroy_operation_codes,  # Yeni eklenen liste
        'stuk_total': stuk_total,  # Toplamı context'e ekle
    }
    return render(request, 'main/kroy/kroy_detail_view.html', context)

class KroyDetailListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Kroy_detail
    template_name = 'main/kroy/kroy_detail_list.html'
    login_url = '/login/'
    permission_required = 'app_name.view_KroyDetail'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_kroys = Kroy_detail.objects.order_by('-created')[:30]  # Son 10 kaydı al
        print(latest_kroys)
        context['latest_kroys'] = latest_kroys  # Son 10 kaydı context'e ekle
        return context


class KroyDetailCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = Kroy_detail
    form_class = KroyDetailForm
    template_name = 'main/kroy/kroy_detail_form.html'
    success_url = reverse_lazy('kroy-detail-create')
    login_url = '/login/'
    permission_required = 'app_name.view_KroyDetail'

    def handle_no_permission(self):
        # Kullanıcı oturum açmamışsa, giriş yapma sayfasına yönlendir
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kroy_detail_list'] = Kroy_detail.objects.all().order_by('-created')[:10]  # Add this line to pass the data to the template
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kroy_instance_id = self.kwargs.get('kroy_id')
        try:
            kroy_instance = Kroy.objects.get(pk=kroy_instance_id)
            kwargs['kroy_instance'] = kroy_instance
        except Kroy.DoesNotExist:
            raise Http404("Kroy matching query does not exist.")
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        #burada geldigim kroy-detail-view daki secilmis kroya gitmesi lazim
        return reverse_lazy('kroy-detail-view', kwargs={'kroy_id': self.object.kroy.pk})

class KroyDetailUpdateView(UpdateView, PermissionRequiredMixin):
    model = Kroy_detail
    form_class = KroyDetailForm
    template_name = 'main/kroy/kroy_detail_form.html'
    success_url = '/kroy-detail/'
    permission_required = 'app_name.view_KroyDetail'

    def get_success_url(self):
        #burada geldigim kroy-detail-view daki secilmis kroya gitmesi lazim
        return reverse_lazy('kroy-detail-view', kwargs={'kroy_id': self.object.kroy.pk})


class KroyDetailDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Kroy_detail
    template_name = 'main/kroy/kroy_detail_confirm_delete.html'
    permission_required = 'app_name.view_KroyDetail'
    #success_url = reverse_lazy('kroy-detail-view')  # Silme işleminden sonra yönlendirilecek URL

    def handle_no_permission(self):
        return redirect('login')

    def get_success_url(self):
        #burada geldigim kroy-detail-view daki secilmis kroya gitmesi lazim
        return reverse_lazy('kroy-detail-view', kwargs={'kroy_id': self.object.kroy.pk})


# ---Kroy detail sonu ---
# --- Operasynu kodu olusturma alani basi---
@login_required
@permission_required('main.add_view', raise_exception=True)
def operation_code_create(request):
    if request.method == 'POST':
        form = OperationCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('operation_code_list')  # operation_code_list view'ine yönlendir
    else:
        form = OperationCodeForm()
    return render(request, 'main/operation/operation_code_create.html', {'form': form})

@login_required
@permission_required('main.add_view', raise_exception=True)
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

@login_required
@permission_required('main.add_view', raise_exception=True)
def operation_code_delete(request, pk):
    operation_code = get_object_or_404(Operation_code, pk=pk)
    if request.method == 'POST':
        operation_code.delete()
        return redirect('operation_code_list')  # Silme işlemi gerçekleştiğinde listeleme sayfasına yönlendir
    return render(request, 'main/operation/operation_code_delete.html', {'object': operation_code})

@login_required
@permission_required('main.add_view', raise_exception=True)
def operation_code_list(request):
    operation_codes = Operation_code.objects.filter(is_active=True)
    return render(request, 'main/operation/operation_code_list.html', {'operation_codes': operation_codes})

# --- operasyon kodu olusturma alani sonu ---

# --- operasyon listesi olusturma alani basi ---
@login_required
@permission_required('main.add_view', raise_exception=True)
def operation_list_detail(request, operation_code_id):
    operation_code = get_object_or_404(Operation_code, id=operation_code_id)
    operation_lists = Operation_list.objects.filter(operation_code=operation_code)
    total_price = sum(operation.price for operation in operation_lists)
    return render(request, 'main/operation/operation_list_detail.html', {
        'operation_code': operation_code,
        'operation_lists': operation_lists,
        'total_price': total_price,
    })

@login_required
@permission_required('main.add_view', raise_exception=True)
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

@login_required
@permission_required('main.add_view', raise_exception=True)
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

@login_required
@permission_required('main.add_view', raise_exception=True)
def operation_list_delete(request, pk):
    operation_list = get_object_or_404(Operation_list, pk=pk)
    operation_code_id = operation_list.operation_code.id
    operation_list.delete()
    return redirect('operation_list_detail', operation_code_id=operation_code_id)

@login_required
@permission_required('main.add_view', raise_exception=True)
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

# --- operasyon listesi olusturma alani sonu ---

# --- Operasyonu Kroy icin atama alani basi ---
@login_required
@permission_required('main.add_view', raise_exception=True)
def kroy_operation_code_list(request):
    codes = Kroy_operation_code.objects.filter(is_active=True)

    return render(request, 'main/opercode/kroy_operation_code_list.html', {'codes': codes})

@login_required
@permission_required('main.add_view', raise_exception=True)
def kroy_operation_code_create(request):
    if request.method == 'POST':
        form = KroyOperationCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kroy_operation_code_list')
    else:
        form = KroyOperationCodeForm()
    return render(request, 'main/opercode/kroy_operation_code_form.html', {'form': form})

@login_required
@permission_required('main.add_view', raise_exception=True)
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

@login_required
@permission_required('main.add_view', raise_exception=True)
def kroy_operation_code_delete(request, pk):
    code = get_object_or_404(Kroy_operation_code, pk=pk)
    if request.method == 'POST':
        code.delete()
        return redirect('kroy_operation_code_list')
    return render(request, 'main/opercode/kroy_operation_code_confirm_delete.html', {'code': code})
# --- Operasyonu Kroy icin atama alani sonu ---

# --- Kullanicilar safasi basi ---
@login_required
@permission_required('main.add_view', raise_exception=True)
def get_operation_codes(request):
    kroy_no = request.GET.get('kroy_no')
    if kroy_no:
        operations = Kroy_operation_code.objects.filter(kroy__kroy_no=kroy_no).values('operation_code', 'operation_code__title')
        data = [{'code': op['operation_code'], 'title': op['operation_code__title']} for op in operations]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@login_required
@permission_required('main.add_view', raise_exception=True)
def get_operation_list(request):
    operation_code = request.GET.get('operation_code')
    if operation_code:
        operations = Operation_list.objects.filter(operation_code=operation_code).values('id', 'title')
        data = [{'id': op['id'], 'title': op['title']} for op in operations]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@login_required
@permission_required('main.add_view', raise_exception=True)
def get_operation_price(request):
    operation_id = request.GET.get('operation_id')
    if operation_id:
        try:
            operation = Operation_list.objects.get(id=operation_id)
            return JsonResponse({'price': operation.price})
        except Operation_list.DoesNotExist:
            return JsonResponse({'price': 0})
    return JsonResponse({'price': 0})

@login_required
#@permission_required('main.add_view', raise_exception=True)
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
# --- Kullanicilar sayfasi sonu--