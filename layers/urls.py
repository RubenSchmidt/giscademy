from django.conf.urls import url

from .views import ImportGeoJsonView, LayerListView

urlpatterns = [
    url(r'^import-geojson/$', ImportGeoJsonView.as_view(), name='import-geojson'),
    url(r'^$', LayerListView.as_view(), name='layer-list'),
]
