# Generated by Django 4.1 on 2022-08-11 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_myuser_managers_alter_patient_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='doc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]