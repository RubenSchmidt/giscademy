from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon

from gisoperations.services.buffers import with_metric_buffer
from layers.models import Polygon, Point, LineString


class OperationsMixin(object):
    @staticmethod
    def difference_features(json, layer, **kwargs):
        ds = DataSource(json)
        geoms = ds[0].get_geoms(geos=True)
        base_geom = geoms[0]
        for geom in geoms[1:]:
            base_geom = base_geom.difference(geom)
        Polygon.objects.create(geom=MultiPolygon(base_geom), layer=layer)
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
        ds = DataSource(json)
        lyr = ds[0]
        for feature in lyr:
            print(feature)

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
        return layer

    @staticmethod
    def buffer_features(json, layer, **kwargs):
        ds = DataSource(json)
        geoms = ds[0].get_geoms(geos=True)
        for geom in geoms:
            buffered = with_metric_buffer(geom, kwargs['size'])
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
