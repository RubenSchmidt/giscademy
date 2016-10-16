from django.conf.urls import url

from .views import ImportGeoJsonView, SandboxView

urlpatterns = [
    url(r'^import-geojson/$', ImportGeoJsonView.as_view(), name='import-geojson'),
    url(r'^sandbox/$', SandboxView.as_view(), name='sandbox'),
]
