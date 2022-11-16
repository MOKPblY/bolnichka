from datetime import date

from celery.schedules import crontab
from cnis.celery import app
from .models import Patient

@app.task
def freeze_patients():
    queryset = Patient.objects.filter(oper_date__isnull = False,
                           status = Patient.Status.PASSED_COM,
                           oper_date__lt = date.today())
    names = list(queryset.values_list('fio', flat=True))
    queryset.update(status = Patient.Status.HEAL_FREEZE) #потестить скорость, возможно, обнулить даты???
    if not names:
        return "Ни один пациент с лечения не снят"
    elif len(names) == 1:
        return f"Пациент {str(names[0])} был снят с лечения"
    else:
        strnames = ', '.join(names)
        return f"Пациенты {strnames} были сняты с лечения"



app.conf.beat_schedule = {
    'add_review': {
        'task': 'mainapp.tasks.freeze_patients',
        'schedule': crontab()
    },
}