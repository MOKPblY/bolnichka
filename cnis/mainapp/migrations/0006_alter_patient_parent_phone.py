# Generated by Django 4.1 on 2022-08-11 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_patient_fio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='parent_phone',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
