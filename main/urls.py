from django.conf.urls import url
from .views import review, doctors_list, add_review, user_register, LoginController, LogoutController, success_review


urlpatterns = [
    url(r'^review/$', review, name='review'),
    url(r'^doctors_list/$', doctors_list, name='doctors_list'),
    url(r'^add_review/(?P<doctor_id>[0-9]+)/$', add_review, name='add_review'),
    url(r'user_register/', user_register, name='user_register'),
    url(r'login/', LoginController.as_view(), name='login'),
    url(r'logout/', LogoutController.as_view(), name='logout'),
    url(r'success_review_msg/', success_review, name='success_review')
]
