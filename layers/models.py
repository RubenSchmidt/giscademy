from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.contrib.postgres.fields import JSONField
from django.db import models

from giscademy.utils.model_utils import Timestampable


class Layer(Timestampable):
    objtype = models.CharField(max_length=32)
    geom = MultiPolygonField()
    json = JSONField(blank=True)
