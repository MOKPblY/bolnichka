from calendar import monthrange
from datetime import date, timedelta
from time import strftime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import PermissionsMixin, Group, User
from django.http import HttpResponse, JsonResponse
from django.template.context_processors import request
from django.template.defaultfilters import date as _date

from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from .forms import *


# Create your views here.


class WaitlistView(ListView, LoginRequiredMixin):
    template_name = 'mainapp/waitlist.html'
    model = Patient
    context_object_name = 'pats'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_doctor'] = self.request.user.groups.filter(name='Врачи').exists()
        context['user_is_reg'] = self.request.user.groups.filter(name='Регистраторы').exists()
        return context

    def get_queryset(self, status = Patient.Status.PASSED_COM):
        return Patient.objects.filter(status = status) ##list??


class ComissionView(ListView, LoginRequiredMixin):
    template_name = 'mainapp/comission.html'
    model = Patient
    context_object_name = 'pats'
    success_url = reverse_lazy('com')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_doctor'] = self.request.user.groups.filter(name='Врачи').exists()
        context['user_is_reg'] = self.request.user.groups.filter(name='Регистраторы').exists()
        return context

    def get_queryset(self, status = Patient.Status.ON_COM):
        return Patient.objects.filter(status = status) ##list??



@login_required(login_url='login')
def to_waitlist(request, pat_id):
    Patient.objects.filter(id=pat_id).update(status=Patient.Status.PASSED_COM)
    return redirect('com')


@login_required(login_url='login')
def deny_a_patient(request, pat_id):
    Patient.objects.filter(id=pat_id).update(doc=None)
    return redirect('mypats')


class AddPatient(CreateView, LoginRequiredMixin):
    template_name = 'mainapp/addform.html'
    model = Patient
    context_object_name = 'pats'
    form_class = PatientForm
    success_url = reverse_lazy('com')
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context
    #
    # def get_queryset(self):
    #     return Patient.objects.get(doc_id=self.request.user.id)


class UpdatePatient(UpdateView, LoginRequiredMixin):
    template_name = 'mainapp/history.html'
    model = Patient
    form_class = PatientForm
    pk_url_kwarg = 'pat_id'
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context


class MyPats(ListView, LoginRequiredMixin):
    template_name = 'mainapp/mypats.html'
    model = Patient
    context_object_name = 'pats'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_doctor'] = self.request.user.groups.filter(name='Врачи').exists()
        context['user_is_reg'] = self.request.user.groups.filter(name='Регистраторы').exists()
        return context

    def get_queryset(self):
        return Patient.objects.filter(doc_id=self.request.user.id, status = Patient.Status.PASSED_COM) ##list??



# def login_view(request):
#     # future -> ?next=/articles/create/
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('/')
#     else:
#         form = AuthenticationForm(request)
#     context = {
#         "form": form
#     }
#     return render(request, "mainapp/login.html", context)

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'mainapp/login.html'

    def get_success_url(self):
        return reverse_lazy('wlist')


def logout_user(request):
    logout(request)
    return redirect('login')


class CalendarView(ListView, LoginRequiredMixin):
    model = MyUser
    template_name = 'mainapp/calendar.html'
    context_object_name = 'docs'

    def get_queryset(self):
        return MyUser.objects.filter(groups__name = 'Врачи')



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_doctor'] = self.request.user.groups.filter(name='Врачи').exists()
        context['user_is_reg'] = self.request.user.groups.filter(name='Регистраторы').exists()

        context['days'] = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт']  # ?????


        oneday = timedelta(days=1)
        today = date.today()

        context['cur_month'] = _date(today, "F Y (D)")  #today.strftime('%B %Y') #для шапки

        start_day = today-(today.weekday())*oneday
        monthdays = [start_day + i * oneday for i in range(35) if i%7<5] #список ключей

        mypats = Patient.objects.filter(hosp_date__range=[start_day, start_day + 35 * oneday]).select_related("doc") #выходные вычернкуть? doc_id=self.request.user.id,
        weeks = [] # список недель

        for i in range(5):
            weeks.append(dict({})) #заполняем словарями-неделями

        for i in range(len(monthdays)):
            weeks[i // 5].update({monthdays[i]: list([])}) #добавляем пары (дата: пустой список) в соответствующие словари недель

        for pat in mypats: #раскидываем пациентов по дням
            if pat.hosp_date and pat.hosp_date.weekday() not in [5,6]: # Временно! Исключает пациентов, записанных на выходные
                days = (pat.hosp_date - start_day).days
                days -= 2*(days//7) #убрать, когда поправлю фильтр пациентов по дате

                weeks[days // 5][pat.hosp_date].append(pat)

        context['weeks'] = weeks
        return context

# def waitlist(request):
#     patients = Patient.objects.filter(doc=None)
#     context = {
#         'pats': patients,
#         'user_is_doctor': request.user.groups.filter(name='Врачи').exists(),
#         'user_is_reg': request.user.groups.filter(name='Регистраторы').exists(),
#     }
#     return render(request, 'mainapp/waitlist.html', context)
#
# def ajaxGetPats(request):
#
#     oneday = timedelta(days=1)
#     today = date.today()
#
#     start_day = today - (today.weekday()) * oneday
#     monthdays = [start_day + i * oneday for i in range(35) if i % 7 < 5]  # список ключей
#     pats = Patient.objects.filter(doc_id=request.user.id,
#                                     hosp_date__range=[start_day, start_day + 35 * oneday])  # выходные вычернкуть?
#     weeks = []  # список недель
#
#     for i in range(5):
#         weeks.append(dict({}))  # заполняем словарями-неделями
#
#     for i in range(len(monthdays)):
#         weeks[i // 5].update(
#             {monthdays[i]: list([])})  # добавляем пары (дата: пустой список) в соответствующие словари недель
#
#     for pat in pats:  # раскидываем пациентов по дням
#         # print("Пациент", pat)
#         if pat.hosp_date and pat.hosp_date.weekday() not in [5,
#                                                              6]:  # Временно! Исключает пациентов, записанных на выходные
#             days = (pat.hosp_date - start_day).days
#             days -= 2 * (days // 7)  # убрать, когда поправлю фильтр пациентов по дате
#             print(days // 5, days % 5)
#             print(pat.hosp_date)
#             print(days)
#             weeks[days // 5][pat.hosp_date].append(pat)
#
#
#     context['weeks'] = weeks
#     # print(weeks)
#     return context

def ajaxDetails(request, pat_id):
    pat = Patient.objects.get(id=pat_id)
    pat_json = dict.fromkeys(['fio', 'diag', 'oper', 'op_date'], None)
    pat_json['fio'] = pat.fio
    pat_json['diag'] = pat.diag_desc
    pat_json['oper'] = pat.oper_name
    pat_json['op_date'] = pat.oper_date
    for k, v in pat_json.items():
        if not v:
            pat_json[k] = 'Не заполнено'
    return(JsonResponse(pat_json))


class DocUpdateView(UpdateView, LoginRequiredMixin):

    template_name = 'mainapp/mycab.html'
    model = MyUser
    form_class = DocUpdateForm
    pk_url_kwarg = 'doc_id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_doctor'] = self.request.user.groups.filter(name='Врачи').exists()
        context['user_is_reg'] = self.request.user.groups.filter(name='Регистраторы').exists()
        return context
