from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers

from layers.models import Point, LineString, Polygon, Layer


class BaseGeofeatureSerializer(gis_serializers.GeoFeatureModelSerializer):
    def get_properties(self, instance, fields):
        # TODO show properties JSON field.
        return instance.properties


class PointSerializer(BaseGeofeatureSerializer):
    class Meta:
        model = Point
        geo_field = 'geom'
        fields = ['geom', 'id']


class LineStringSerializer(BaseGeofeatureSerializer):
    class Meta:
        model = LineString
        geo_field = 'geom'
        fields = ['geom']


class PolygonSerializer(BaseGeofeatureSerializer):
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
        fields = ['id', 'name', 'user', 'exercise', 'points', 'linestrings', 'polygons']
