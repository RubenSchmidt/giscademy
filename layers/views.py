import json

from django.contrib.gis import geos
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, GeometryCollection
from django.shortcuts import render

# Create your views here.
from django.views import View

from layers.models import Layer, Point, Polygon


class SandboxView(View):
    template_name = 'sandbox.html'

    def get(self, request):
        return render(request, self.template_name)


class ImportGeoJsonView(View):
    """
    Add geojson layers.
    """
    template_name = 'import_geojson.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        geojson = request.POST.get('geojson')
        layer_name = request.POST.get('name')
        ds = DataSource(geojson)
        if len(ds) == 1:
            layer = Layer.objects.create(name=layer_name, json=geojson)
            geoms = ds[0].get_geoms(geos=True)
            for geom in geoms:
                geom_type = geom.geom_type
                if geom_type == 'Point':
                    Point.objects.create(geom=geom, layer=layer)

                if geom_type == 'Polygon':
                    Polygon.objects.create(geom=MultiPolygon(geom), layer=layer)

                if geom_type == 'MultiPolygon':
                    Polygon.objects.create(geom=geom, layer=layer)

        return render(request, self.template_name)
