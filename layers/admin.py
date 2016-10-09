from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Layer


@admin.register(Layer)
class LayerAdmin(OSMGeoAdmin):
    list_display = ['objtype']
    list_filter = ['objtype']
