from django.contrib.gis.db.models import MultiPolygonField
from django.db import models

from giscademy.utils.model_utils import Timestampable


class Layer(Timestampable):
    objtype = models.CharField(max_length=32)
    geom = MultiPolygonField(srid=32632)

