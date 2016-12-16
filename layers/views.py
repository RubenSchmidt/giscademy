from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from layers.models import Layer, Point, Polygon, LineString
from layers.serializers import LayerSerializer


class LayerListView(View):
    def get(self, request):
        layers = Layer.objects.all()
        data = LayerSerializer(layers, many=True).data
        return JsonResponse(data=data, safe=False)


class ExerciseLayersListView(View):
    def get(self, request, exercise_slug):
        layers = Layer.objects.filter(exercise__slug=exercise_slug)
        data = LayerSerializer(layers, many=True).data
        return JsonResponse(data=data, safe=False)


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
            layer = Layer.objects.create(name=layer_name)
            geoms = ds[0].get_geoms(geos=True)
            for geom in geoms:
                geom_type = geom.geom_type
                if geom_type == 'Point':
                    Point.objects.create(geom=geom, layer=layer)

                if geom_type == 'LineString':
                    LineString.objects.create(geom=geom, layer=layer)

                if geom_type == 'Polygon':
                    Polygon.objects.create(geom=MultiPolygon(geom), layer=layer)

                if geom_type == 'MultiPolygon':
                    Polygon.objects.create(geom=geom, layer=layer)

        return render(request, self.template_name)
