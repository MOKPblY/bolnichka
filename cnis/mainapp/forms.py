from django import forms
from django.contrib.admin import widgets
from django.forms import ModelChoiceField

from .models import *


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['fio', 'birth_date', 'adress', 'parent_phone', 'parent_name', 'hosp_date', 'diag_desc', 'diag_code', 'oper_name', 'oper_date', 'comment', 'doc']
        widgets = {
            'birth_date' : forms.DateInput(format = ('%Y-%m-%d'), attrs={'type':'date'}),
            'oper_date' : forms.DateInput(format = ('%Y-%m-%d'), attrs={'type':'date'}),
            'hosp_date' : forms.DateInput(format = ('%Y-%m-%d'), attrs={'type':'date'}),
            'diag_desc' : forms.Textarea(attrs={'contenteditable': 'true', 'cols': 1, 'rows': 4, 'maxlength': 1000}),
            'comment' : forms.Textarea(attrs={'contenteditable': 'true', 'cols': 1, 'rows': 4, 'maxlength': 1000})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = 'Не заполнено'
            field.label_suffix = ''

    # doc = ModelChoiceField(label='Врач', queryset=MyUser.objects.all(), required=True)


class DocUpdateForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None
            field.widget.attrs['placeholder'] = 'Не заполнено'
            field.label_suffix = ''

    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'email', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }