from django.conf.urls import url
from .views import review


urlpatterns = [
    url('review/', review)
]
