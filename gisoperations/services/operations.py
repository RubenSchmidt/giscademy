from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon

from gisoperations.services.buffers import with_metric_buffer
from layers.models import Polygon, Point, LineString


class OperationsMixin(object):

    @staticmethod
    def get_layer(json):
        ds = DataSource(json)
        return ds[0]

    @staticmethod
    def extract_properties(feature):
        fields = feature.fields
        properties = {}
        for field in fields:
            name = field.decode('UTF-8')
            properties[name] = feature.get(name)
        return properties

    @staticmethod
    def difference_features(json, layer, **kwargs):
        ds = DataSource(json)
        geoms = ds[0].get_geoms(geos=True)
        base_geom = geoms[0]
        for geom in geoms[1:]:
            base_geom = base_geom.difference(geom)
        if base_geom.geom_type == 'MultiPolygon':
            geom = base_geom
        else:
            geom = MultiPolygon(base_geom)
        Polygon.objects.create(geom=geom, layer=layer)
        return layer

    @staticmethod
    def unite_features(json, layer, **kwargs):
        ds = DataSource(json)
        geoms = ds[0].get_geoms(geos=True)
        base_geom = geoms[0]
        for geom in geoms[1:]:
            base_geom = base_geom.union(geom)
        Polygon.objects.create(geom=MultiPolygon(base_geom), layer=layer)
        return layer

    @staticmethod
    def add_all_features_to_layer(json, layer, **kwargs):
        """
        Add all the features in the json to a single layer.
        """
        lyr = OperationsMixin.get_layer(json)
        for feature in lyr:
            geom = feature.geom.clone()
            geom.coord_dim = 2
            geos = geom.geos
            geom_type = geos.geom_type
            properties = OperationsMixin.extract_properties(feature)
            if geom_type == 'Point':
                Point.objects.create(geom=geos, layer=layer, properties=properties)
            elif geom_type == 'LineString':
                LineString.objects.create(geom=geos, layer=layer, properties=properties)
            elif geom_type == 'Polygon':
                Polygon.objects.create(geom=MultiPolygon(geos), layer=layer, properties=properties)
            elif geom_type == 'MultiPolygon':
                Polygon.objects.create(geom=geos, layer=layer, properties=properties)
        return layer

    @staticmethod
    def buffer_features(json, layer, **kwargs):
        ds = DataSource(json)
        geoms = ds[0].get_geoms(geos=True)
        # Merge all the layers first
        base_geom = geoms[0]
        for geom in geoms[1:]:
            base_geom = base_geom.union(geom)
        buffered = with_metric_buffer(base_geom, float(kwargs['size']))
        if buffered.geom_type == 'MultiPolygon':
            Polygon.objects.create(geom=buffered, layer=layer)
        else:
            Polygon.objects.create(geom=MultiPolygon(buffered), layer=layer)
        return layer

    @staticmethod
    def intersect_features(json, layer, **kwargs):
        ds = DataSource(json)
        geoms = ds[0].get_geoms(geos=True)
        base_geom = geoms[0]

        for geom in geoms[1:]:
            base_geom = base_geom.intersection(geom)
        try:
            geom = MultiPolygon(base_geom)
        except:
            return None
        Polygon.objects.create(geom=geom, layer=layer)
        return layer
