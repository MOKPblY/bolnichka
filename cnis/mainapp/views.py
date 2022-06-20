from calendar import monthrange
from datetime import date, timedelta, datetime
from os.path import abspath

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth import models
from django.contrib.auth.models import Group


from .models import *
from .forms import *
# Create your views here.

@login_required(login_url='login')
def waitlist(request):
    patients = Patient.objects.filter(doc=None)
    context = {
        'pats' : patients,
        'user_is_doctor' : request.user.groups.filter(name='Врачи').exists(),
        'user_is_reg' : request.user.groups.filter(name='Регистраторы').exists(),
    }
    return render(request, 'mainapp/index.html', context)


@login_required(login_url='login')
def get_a_patient(request, pat_id):
    Patient.objects.filter(id=pat_id).update(doc=request.user)
    return redirect('wlist')

@login_required(login_url='login')
def deny_a_patient(request, pat_id):
    Patient.objects.filter(id=pat_id).update(doc=None)
    return redirect('mypats')




class AddPatient(CreateView):
    template_name = 'mainapp/addform.html'
    model = Patient
    context_object_name = 'pats'
    form_class = AddPatient

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Patient.objects.filter(doc_id=self.request.user.id)


# @login_required(login_url='login')
# def addpatient(request):
#     if request.method == 'POST':
#         form = AddPatient(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             Patient.objects.create(**form.cleaned_data) #распаковка аргументов
#             return redirect('wlist')
#         else:
#             form.add_error(None, 'Ошибка добавления пациента')
#     else:
#         form = AddPatient()
#
#     return render(request, 'mainapp/addform.html', {'form': form})

class UpdatePatient(UpdateView):
    template_name = 'mainapp/history.html'
    model = Patient
    form_class = DocEditPat
    pk_url_kwarg = 'pat_id'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MyPats(ListView):
    template_name = 'mainapp/mypats.html'
    model = Patient
    context_object_name = 'pats'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_doctor'] = self.request.user.groups.filter(name='Врачи').exists(),
        context['user_is_reg'] = self.request.user.groups.filter(name='Регистраторы').exists(),
        return context

    def get_queryset(self):
        return Patient.objects.filter(doc_id=self.request.user.id)


#
# @login_required(login_url='login')
# def history(request,pat_id):
#     patient = Patient.objects.get(id = pat_id)
#     return render(request, 'mainapp/history.html', {'p': patient})

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'mainapp/login.html'

    def get_context_data(self, *, object_list = None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('wlist')

def logout_user(request):
    logout(request)
    return redirect('login')

class CalendarView(ListView):
    model = Patient
    days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'] #?????
    today = date.today()

    mdays = monthrange(today.year, today.month)[1]

    template_name = 'mainapp/calendar.html'

    def get_context_data(self, *, object_list = None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['days'] = self.days #?????

        oneday = timedelta(days=1)
        today = self.today

        # day = 1
        # weeks = []
        # print(weeks)
        # for i in range(5):
        #     weeks.append([])
        #     for j in range(7):
        #         weeks[i].append([])
        #         day+=1
        #         if day>30:
        #             break
        #     if day>30:
        #         break

        monthdays = [today+i*oneday for i in range(30)] # today.day, today.day + 30
        print(monthdays)
        print(date.today().weekday())
        mypats = Patient.objects.filter(doc_id=self.request.user.id,hosp_date__range=[today, today + 30*oneday])
        weeks = []

        for i in range(5):
            weeks.append(dict({}))

        for i in range(len(monthdays)):
            weeks[i//7].update({monthdays[i]:list([])})

        print(weeks, monthdays)

        #
        # for week in weeks:
        #     for weekday in range(7):
        #         week[weekday] = monthdays[i]

        for pat in mypats:
            if pat.hosp_date:
                days = (pat.hosp_date-today).days
                print(days//7, days%7)
                weeks[days//7][pat.hosp_date].append(pat)
                #weeks[(pat.hosp_date-today).days//7][(pat.hosp_date-today).days%7]

        #context['parent_list']= [{'A': 'val1', 'B': 'val2'}, {'C': 'val3', 'D': 'val4'}]
        context['weeks']=weeks
        print(weeks)
        return context

    