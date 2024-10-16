# forms.py
from django import forms
from django.contrib.auth.models import User
from main.models import Status, Kroy

class ReportForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Пользователь",
        required=False
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Состояние работ",
        required=False
    )
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата начала')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата окончания')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-sm'})


class Report_allForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Пользователь')
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата начала')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата окончания')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-sm'})

class AlluserReportForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    kroy_no = forms.ModelChoiceField(
        queryset=Kroy.objects.all(),
        required=False,
        label='Крой номер',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата начала')
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Дата окончания')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-sm'})