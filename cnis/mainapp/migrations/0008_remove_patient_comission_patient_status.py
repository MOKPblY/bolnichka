# Generated by Django 4.1 on 2022-11-07 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_alter_patient_options_alter_myuser_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='comission',
        ),
        migrations.AddField(
            model_name='patient',
            name='status',
            field=models.CharField(choices=[('OC', 'На комиссии'), ('PC', 'Прошел комиссию'), ('HF', 'Лечение приостановлено')], default='HF', max_length=2, verbose_name='Прошел комиссию'),
        ),
    ]
