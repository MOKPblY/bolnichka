from django.urls import path

from .views import *

urlpatterns = [
    path('waitlist/addpatient/', AddPatient.as_view(), name = 'addpat'),
    path('', waitlist, name = 'wlist'),
    path('waitlist/', waitlist, name = 'wlist'),
    path('mypatslist/', MyPats.as_view(), name = 'mypats'),
    path('mypatslist/pathistory/<int:pat_id>', UpdatePatient.as_view(), name = 'history'),
    path('calendar/', CalendarView.as_view(), name = 'cal'),
    path('login/', LoginUser.as_view(), name = 'login'),
    path('logout/', logout_user, name = 'logout'),
    path('waitlist/get/<int:pat_id>', get_a_patient, name = 'take'),
    path('mypatslist/deny/<int:pat_id>', deny_a_patient, name = 'deny'),

]