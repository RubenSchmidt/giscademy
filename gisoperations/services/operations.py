from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPolygon

from gisoperations.services.buffers import with_metric_buffer
from layers.models import Layer, Polygon


def create_buffer_layer(json, buffer_meters, layer_name, user, exercise=None):
    """
    Buffer any geos geometry.
    :param exercise:
    :param layer_name:
    :param user:
    :param json: Input json
    :param buffer_meters: Buffer size in meters
    :return: Layer model
    """
    ds = DataSource(json)
    layer = Layer.objects.create(name=layer_name, exercise=exercise, user=user)
    geoms = ds[0].get_geoms(geos=True)
    for geom in geoms:
        buffered = with_metric_buffer(geom, buffer_meters)
        Polygon.objects.create(geom=MultiPolygon(buffered), layer=layer)

    return layer


def create_intersection_layer(json, layer_name, user, exercise=None):
    ds = DataSource(json)
    layer = Layer.objects.create(name=layer_name, exercise=exercise, user=user)
    geoms = ds[0].get_geoms(geos=True)
    if len(geoms) != 2:
        return None

    intersection_geos = geoms[0].intersection(geoms[1])

    try:
        geom = MultiPolygon(intersection_geos)
    except:
        return None
    Polygon.objects.create(geom=geom, layer=layer)
    return layer
