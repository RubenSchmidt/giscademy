from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^buffer/$', views.BufferView.as_view(),),

]