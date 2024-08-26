from django import forms
from .models import GirisHareketi, CikisHareketi, Malzeme

class GirisHareketiForm(forms.ModelForm):
    class Meta:
        model = GirisHareketi
        fields = ['malzeme', 'miktar', 'tedarikci']
        widgets = {
            'malzeme': forms.Select(attrs={'class': 'form-control'}),
            'miktar': forms.NumberInput(attrs={'class': 'form-control'}),
            'tedarikci': forms.TextInput(attrs={'class': 'form-control'}),

        }

class CikisHareketiForm(forms.ModelForm):
    class Meta:
        model = CikisHareketi
        fields = ['malzeme', 'miktar', 'uretim_siparisi']

class MalzemeForm(forms.ModelForm):
    class Meta:
        model = Malzeme
        fields = ['isim', 'miktar', 'malzeme_category', 'malzeme_birim', 'aciklama', ]
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'form-control'}),
            'miktar': forms.NumberInput(attrs={'class': 'form-control'}),
            'malzeme_category': forms.Select(attrs={'class': 'form-control'}),
            'malzeme_birim': forms.Select(attrs={'class': 'form-control'}),
            'aciklama': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 23}),
        }
