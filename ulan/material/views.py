from django.shortcuts import render, redirect, get_object_or_404
from .models import GirisHareketi, CikisHareketi, TransferHareketi, Malzeme
from .forms import GirisHareketiForm, CikisHareketiForm, MalzemeForm
from django.contrib import messages

def malzeme_listesi(request):
    malzemeler = Malzeme.objects.all()
    return render(request, 'material/malzeme_listesi.html', {'malzemeler': malzemeler})

def malzeme_edit(request, pk):
    malzeme = get_object_or_404(Malzeme, pk=pk)
    if request.method == "POST":
        form = MalzemeForm(request.POST, instance=malzeme)
        if form.is_valid():
            form.save()
            return redirect('material:malzeme_listesi')
    else:
        form = MalzemeForm(instance=malzeme)
    return render(request, 'material/malzeme_edit.html', {'form': form})

def malzeme_delete(request, pk):
    malzeme = get_object_or_404(Malzeme, pk=pk)
    if request.method == "POST":
        malzeme.delete()
        return redirect('material:malzeme_listesi')
    return render(request, 'material/malzeme_delete.html', {'malzeme': malzeme})

def malzeme_detayi(request, pk):
    malzeme = get_object_or_404(Malzeme, pk=pk)
    giris_hareketleri = GirisHareketi.objects.filter(malzeme=malzeme)
    cikis_hareketleri = CikisHareketi.objects.filter(malzeme=malzeme)
    transfer_hareketleri = TransferHareketi.objects.filter(malzeme=malzeme)  # Transfer hareketlerini ekleyin

    context = {
        'malzeme': malzeme,
        'giris_hareketleri': giris_hareketleri,
        'cikis_hareketleri': cikis_hareketleri,
        'transfer_hareketleri': transfer_hareketleri,  # Context'e ekleyin
    }
    return render(request, 'material/malzeme_detayi.html', context)


def giris_hareketleri(request):
    hareketler = GirisHareketi.objects.all()
    return render(request, 'material/giris_hareketleri.html', {'hareketler': hareketler})

def cikis_hareketleri(request):
    hareketler = CikisHareketi.objects.all()
    return render(request, 'material/cikis_hareketleri.html', {'hareketler': hareketler})

def malzeme_giris(request):
    if request.method == 'POST':
        form = GirisHareketiForm(request.POST)
        if form.is_valid():
            giris_hareketi = form.save()
            giris_hareketi.malzeme.miktar += giris_hareketi.miktar
            giris_hareketi.malzeme.save()
            messages.success(request, 'Поступление материала успешно зарегистрировано.')
            return redirect('material:malzeme_listesi')
    else:
        form = GirisHareketiForm()
    return render(request, 'material/malzeme_giris.html', {'form': form})

def malzeme_cikis(request):
    if request.method == 'POST':
        form = CikisHareketiForm(request.POST)
        if form.is_valid():
            cikis_hareketi = form.save()
            cikis_hareketi.malzeme.miktar -= cikis_hareketi.miktar
            cikis_hareketi.malzeme.save()
            messages.success(request, 'Выпуск материала успешно зафиксирован')
            return redirect('material:malzeme_listesi')
    else:
        form = CikisHareketiForm()
    return render(request, 'material/malzeme_cikis.html', {'form': form})


def malzeme_kaydet(request):
    if request.method == 'POST':
        form = MalzemeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('material:malzeme_listesi')  # Kayıttan sonra malzeme listesi sayfasına yönlendirme
    else:
        form = MalzemeForm()
    return render(request, 'material/malzeme_kaydet.html', {'form': form})