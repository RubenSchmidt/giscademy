import serpy
import json
from django.core.serializers import serialize
from rest_framework_gis import serializers

from layers.models import Feature, Point, LineString, Polygon, Layer


class PointSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Point
        geo_field = 'geom'
        fields = ['geom']


class LineStringSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = LineString
        geo_field = 'geom'
        fields = ['geom']


class PolygonSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Polygon
        geo_field = 'geom'
        fields = ['geom']


class LayerSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)
    linestrings = LineStringSerializer(many=True)
    polygons = PolygonSerializer(many=True)

    class Meta:
        model = Layer
        fields = ['name', 'exercise', 'points', 'linestrings', 'polygons']

