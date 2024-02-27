from django import forms
from .models import Kroy, Kroy_detail, Masterdata
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class KroyForm(forms.ModelForm):
    class Meta:
        model = Kroy
        fields = ['kroy_no', 'name', 'ras_tkani', 'ras_dublerin', 'edinitsa', 'description']

    def clean_kroy_no(self):
        kroy_no = self.cleaned_data.get('kroy_no')
        if self.instance and self.instance.pk is not None:
            return kroy_no
        if Kroy.objects.filter(kroy_no=kroy_no).exists():
            raise ValidationError("Этот номер Кроя уже существует. Пожалуйста, введите другой номер.")
        return kroy_no


class KroyDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(KroyDetailForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = get_user_model().objects.all()

    class Meta:
        model = Kroy_detail
        fields = ['kroy', 'pachka', 'razmer', 'rost', 'stuk', 'user', 'city', 'color']  # You can specify specific fields if needed


class MasterdataSearchForm(forms.Form):
    start_date = forms.DateField(label='Дата начала', required=False)
    end_date = forms.DateField(label='Дата окончания', required=False)
    uchastok_search = forms.CharField(label='Искать по участке', required=False)
    kroy_no_search = forms.CharField(label='Искать по крой но:', required=False)
    user = forms.CharField(label='Искать по крой но:', required=False)

class MasterdataForm(forms.ModelForm):
    class Meta:
        model = Masterdata
        fields = ['user']  # Add other fields as needed
