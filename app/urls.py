from django.conf.urls import url
from app import views
urlpatterns = [
url(r'^$', views.index, name='index'),
url(r'^admin/login/$', views.admin_login, name ="admin_login"),
url(r'^operator/login/$', views.operator_login, name ="operator_login"),
url(r'^logout/$', views.logout, name ="logout"),
url(r'^patient/(?P<patient_id>\w+)/$',views.patient,name="patient view"),
url(r'^patient/(?P<patient_id>\w+)/(?P<status>\w+)/mark/$',views.patient_mark_attendance,name="patient mark attendance"),
url(r'^patient/(?P<patient_id>\w+)/delete/$',views.patient_delete,name="patient delete"),
url(r'^admin/add_clinic/$', views.admin_add_clinic, name ="admin add clinic"),
url(r'^report/$', views.report_generator, name ="report generator"),
url(r'^operator/patient_reg/$', views.op_patient_register, name ="patient register"),
url(r'^search/$', views.autocompleteModel , name = 'search'), #clinic
url(r'^search2/$', views.autocompleteModel2 , name = 'search2'), #p name
url(r'^search3/$', views.autocompleteModel3 , name = 'search3'), #p mob
url(r'^search4/$', views.autocompleteModel4 , name = 'search4'), #p key
url(r'^sendmsg/$', views.sendmsg, name ="send msg"),
]
