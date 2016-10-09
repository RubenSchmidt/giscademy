from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from gis.models import ByggFlate

admin.site.register(ByggFlate, OSMGeoAdmin)
