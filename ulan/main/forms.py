from django import forms
from .models import Kroy, Kroy_detail, Masterdata
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class KroyForm(forms.ModelForm):
    class Meta:
        model = Kroy
        fields = ['kroy_no', 'name', 'ras_tkani', 'ras_dublerin', 'edinitsa', 'description']

class KroyDetailForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(KroyDetailForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = get_user_model().objects.all()

    class Meta:
        model = Kroy_detail
        fields = ['kroy', 'pachka', 'razmer', 'rost', 'stuk', 'user']  # You can specify specific fields if needed

    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.HiddenInput(),
        initial=get_user_model().objects.get(username='admin')
    )

class MasterdataSearchForm(forms.Form):
    start_date = forms.DateField(label='Дата начала', required=False)
    end_date = forms.DateField(label='Дата окончания', required=False)
    uchastok_search = forms.CharField(label='Искать по участке', required=False)
    kroy_no_search = forms.CharField(label='Искать по крой но:', required=False)

class MasterdataForm(forms.ModelForm):
    class Meta:
        model = Masterdata
        fields = ['user']  # Add other fields as needed
