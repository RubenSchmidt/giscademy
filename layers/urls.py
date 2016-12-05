from django.conf.urls import url

from .import views

urlpatterns = [
    url(r'^import-geojson/$', views.ImportGeoJsonView.as_view(), name='import-geojson'),
    url(r'^$', views.LayerListView.as_view(), name='layer-list'),
    url(r'^(?P<exercise_slug>[-\w]+)/$', views.ExerciseLayersListView.as_view(), name='exercise-layer-list'),
]
