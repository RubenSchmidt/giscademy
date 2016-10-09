from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import FKBLayer


@admin.register(FKBLayer)
class FKBLayerAdmin(OSMGeoAdmin):
    list_display = ['objtype']
    list_filter = ['objtype']
