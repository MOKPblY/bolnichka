from django import forms
from .models import *

class AddPatient(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['fio', 'city', 'parent_phone', 'birth_date']
        widgets = {
            'fio' : forms.TextInput(attrs={'maxlength':50, 'placeholder':'Петров Петр Петрович'}),
            'city' : forms.TextInput(attrs={'maxlength':50, 'placeholder':'Москва'}),
            'parent_phone' : forms.TextInput(attrs={'maxlength':50}),
            'birth_date' : forms.SelectDateWidget(),
        }

class DocEditPat(forms.ModelForm):

    fio = forms.CharField(label = 'ФИО', disabled=True,required=False,widget=forms.TextInput(attrs={'maxlength':50, 'placeholder':'K01'}))
    city = forms.CharField(disabled=True,required=False,widget=forms.TextInput(attrs={'maxlength':50, 'placeholder':'K01'}))
    parent_phone = forms.CharField(disabled=True,required=False,widget=forms.TextInput(attrs={'maxlength':50, 'placeholder':'K01'}))
    birth_date = forms.DateField(disabled=True,required=False,widget=forms.TextInput(attrs={'maxlength':50, 'placeholder':'K01'}))
    hosp_date = forms.DateField(required=False,widget=forms.SelectDateWidget(attrs={'maxlength':50, 'placeholder':'K01'}))
    oper_date = forms.DateField(required=False,widget=forms.SelectDateWidget(attrs={'maxlength':50, 'placeholder':'K01'}))
    diag_code = forms.CharField(required=False,widget=forms.TextInput(attrs={'maxlength':50, 'placeholder':'K01'}))
    diag_desc = forms.CharField(required=False,widget=forms.Textarea(attrs={'maxlength':50, 'placeholder':'K01'}))
    class Meta:
        model = Patient
        fields = ['fio','city','parent_phone','birth_date','hosp_date','oper_date','diag_code','diag_desc']
        widgets = {
            'fio' : forms.TextInput(attrs={'disabled': True,'maxlength':50, 'placeholder':'Петров Петр Петрович'}),
            'city' : forms.TextInput(attrs={'required':'False','disabled': True,'maxlength':50, 'placeholder':'Москва'}),
            'parent_phone' : forms.TextInput(attrs={'required':'False','disabled' : True,'maxlength':50}),
            'birth_date' : forms.DateInput(attrs = {'required': 'False','disabled' : True}),
            #'reg_date' : forms.DateInput(attrs = {'required': 'false','disabled':True}),
            'hosp_date' : forms.SelectDateWidget(attrs = {}),
            'oper_date' : forms.SelectDateWidget(attrs = {}),
            'diag_code' : forms.TextInput(attrs = {'required': False,}),
            'diag_desc' : forms.Textarea(attrs = {}),
        }
