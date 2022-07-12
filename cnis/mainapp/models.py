from django.conf import settings
from django.db import models
# Create your models here.
from django.urls import reverse


class Patient(models.Model):
    class Meta:
        ordering = ['-id', ]

    fio = models.CharField(max_length=255, verbose_name='ФИО')
    city = models.CharField(max_length=255, verbose_name='Город')
    parent_phone = models.CharField(max_length=10, null=True, verbose_name='Телефон родителей')
    birth_date = models.DateField(null=True, verbose_name='Дата рождения')

    reg_date = models.DateField(auto_now_add=True)
    hosp_date = models.DateField(null=True)
    oper_date = models.DateField(null=True)
    diag_code = models.CharField(max_length=10, null=True)
    diag_desc = models.TextField(null=True)
    doc = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse('wlist')


class PatientNote(models.Model):
    patient = models.ForeignKey('Patient', null=True, on_delete=models.CASCADE)
    note_date = models.DateField(null=True)
    diag_code = models.CharField(max_length=10, null=True)
    comment = models.TextField(null=True)
    doc = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
