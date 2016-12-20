from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from layers.models import Layer, Point, Polygon, LineString
from layers.serializers import LayerSerializer


class LayerListView(APIView):
    def get(self, request):
        layers = Layer.objects.all()
        data = LayerSerializer(layers, many=True).data
        return Response(data=data)


class LayerDetailView(APIView):

    def delete(self, request, pk):
        layer = get_object_or_404(Layer, pk=pk)
        layer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExerciseLayersListView(APIView):
    def get(self, request, exercise_slug):
        """
        Return the layers defined internally.
        """
        layers = Layer.objects.filter(exercise__slug=exercise_slug, user__isnull=True)
        user_layers = Layer.objects.filter(exercise__slug=exercise_slug, user=request.user)
        data = {
            'layers': LayerSerializer(layers, many=True).data,
            'user_layers': LayerSerializer(user_layers, many=True).data
        }
        return Response(data=data)


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
