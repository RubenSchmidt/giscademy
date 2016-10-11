from django.conf.urls import url

from .views import ImportGeoJsonView

urlpatterns = [
    url(r'^import-geojson/$', ImportGeoJsonView.as_view(), name='import-geojson'),
]