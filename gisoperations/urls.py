from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^operation/$', views.OperationView.as_view(),),

]