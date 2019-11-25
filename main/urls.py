from django.conf.urls import url
from .views import review, doctors_list, add_review


urlpatterns = [
    url(r'^review/$', review, name='review'),
    url(r'^doctors_list/$', doctors_list, name='doctors_list'),
    url(r'^add_review/(?P<doctor_id>[0-9]+)/$', add_review, name='add_review')
]
