from django import forms
from .models import Kroy, Kroy_detail, Masterdata, Operation_code, Operation_list, Kroy_operation_code  #, Code_operation, Kroy_operations
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError



class KroyForm(forms.ModelForm):
    class Meta:
        model = Kroy
        fields = ['kroy_no', 'name', 'ras_tkani', 'ras_dublerin', 'edinitsa', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 23}),
        }

    def clean_kroy_no(self):
        kroy_no = self.cleaned_data.get('kroy_no')
        if self.instance and self.instance.pk is not None:
            return kroy_no
        if Kroy.objects.filter(kroy_no=kroy_no).exists():
            raise ValidationError("Этот номер Кроя уже существует. Пожалуйста, введите другой номер.")
        return kroy_no


class KroyDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.kroy_instance = kwargs.pop('kroy_instance', None)
        super(KroyDetailForm, self).__init__(*args, **kwargs)
        if self.kroy_instance:
            self.fields['kroy'].widget.attrs['readonly'] = True
            self.initial['kroy'] = self.kroy_instance.pk


    class Meta:
        model = Kroy_detail
        fields = ['kroy', 'pachka', 'razmer', 'rost', 'stuk', 'city', 'color']

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

class OperationCodeForm(forms.ModelForm):
    class Meta:
        model = Operation_code
        fields = ['title', 'description', 'product_type', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 23}),
        }


class OperationListForm(forms.ModelForm):
    class Meta:
        model = Operation_list
        fields = ['title', 'price']

class KroyOperationCodeForm(forms.ModelForm):
    class Meta:
        model = Kroy_operation_code
        fields = ['kroy', 'operation_code', 'is_active']
        widgets = {
            'kroy': forms.Select(attrs={'class': 'form-control'}),
            'operation_code': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }