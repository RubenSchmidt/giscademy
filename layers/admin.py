from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Layer, Polygon, Point, LineString


@admin.register(Layer)
class LayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Polygon)
class PolygonAdmin(admin.ModelAdmin):
    pass


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass


@admin.register(LineString)
class LineStringAdmin(admin.ModelAdmin):
    pass
