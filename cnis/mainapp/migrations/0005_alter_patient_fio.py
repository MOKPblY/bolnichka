# Generated by Django 4.1 on 2022-08-11 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_patient_fio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='fio',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ФИО'),
        ),
    ]
