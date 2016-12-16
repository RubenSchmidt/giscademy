from django.contrib.gis.db.models import MultiPolygonField, PointField, LineStringField
from django.contrib.postgres.fields import JSONField
from django.db import models

from giscademy.utils.model_utils import Timestampable


class Layer(Timestampable):
    name = models.CharField(max_length=255)
    exercise = models.ForeignKey('courses.Exercise', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def points(self):
        return self.point_set.all()

    @property
    def linestrings(self):
        return self.linestring_set.all()

    @property
    def polygons(self):
        return self.polygon_set.all()


class Feature(Timestampable):
    layer = models.ForeignKey(
        'layers.Layer'
    )

    class Meta:
        abstract = True


class Point(Feature):
    geom = PointField()


class LineString(Feature):
    geom = LineStringField()


class Polygon(Feature):
    geom = MultiPolygonField()
