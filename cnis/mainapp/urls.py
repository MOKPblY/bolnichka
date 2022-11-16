from django.urls import path, re_path
from django.views.static import serve

from .views import *

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('waitlist/addpatient/', AddPatient.as_view(), name='addpat'),
    path('', WaitlistView.as_view(), name='wlist'),
    path('waitlist/', WaitlistView.as_view(), name='wlist'),
    path('comission/', ComissionView.as_view(), name='com'),
    path('lk/<int:doc_id>', DocUpdateView.as_view(), name='lk'),
    path('mypatslist/', MyPats.as_view(), name='mypats'),
    path('mypatslist/pathistory/<int:pat_id>', UpdatePatient.as_view(), name='history'),
    path('calendar/', CalendarView.as_view(), name='cal'),
    path('calendar/ajax_details/<int:pat_id>', ajaxDetails, name='ajax_details'),
    #path('calendar/ajax_get_pats/', ajaxGetPats, name = 'ajax_get_pats'),
    path('login/', LoginUser.as_view() , name='login'),#login_view
    path('logout/', logout_user, name='logout'),
    path('waitlist/get/<int:pat_id>', to_waitlist, name='towlist'),
    path('mypatslist/deny/<int:pat_id>', deny_a_patient, name='deny'),
]

