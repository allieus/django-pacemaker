from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^migrate/$', views.migrate, name='migrate'),
    url(r'^createsuperuser/$', views.createsuperuser, name='createsuperuser'),
]

