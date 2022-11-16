from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.urls import reverse
# Create your models here.

class MyUser(AbstractUser):
    color = models.CharField("Мой цвет", max_length = 7, default= '#808080')
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def get_absolute_url(self):
        return reverse('mypats')

class Patient(models.Model):
    class Meta:
        ordering = ['-id', ]
        verbose_name = "пациент"
        verbose_name_plural = "пациенты"

    class Status(models.TextChoices):
        ON_COM = 'OC', _('На комиссии')
        PASSED_COM = 'PC', _('Прошел комиссию')
        HEAL_FREEZE = 'HF', _('Лечение приостановлено')


    fio = models.CharField("ФИО", max_length=35, null=True, blank = True)
    adress = models.CharField("Адрес", max_length=255, blank = True)
    parent_phone = models.CharField("Телефон родителя", max_length=10, null=True, blank = True)
    parent_name = models.CharField("Имя родителя", max_length=20, null=True, blank = True)
    birth_date = models.DateField("Дата рождения", null=True, blank = True)

    reg_date = models.DateField("Дата регистрации", auto_now_add=True, blank = True)
    hosp_date = models.DateField("Дата госпитализации", null=True, blank = True)
    oper_name = models.CharField("Операция", max_length=100, null = True, blank = True)
    oper_date = models.DateField("Дата операции", null=True, blank = True)
    diag_code = models.CharField("Код диагноза", max_length=10, null=True, blank = True)
    diag_desc = models.TextField("Описание диагноза", max_length=10, null=True, blank = True)
    comment = models.TextField("Комментарий", null=True, blank = True)
    status = models.CharField("Прошел комиссию", max_length=2, choices=Status.choices, default = Status.ON_COM, null=False)
    doc = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT, verbose_name="Врач")  # добавить null = False

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('mypats')


class PatientNote(models.Model):
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    note_date = models.DateField(null=True)
    diag_code = models.CharField(max_length=10, null=True)
    comment = models.TextField(null=True)
    doc = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
