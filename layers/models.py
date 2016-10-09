from django.contrib.gis.db.models import MultiPolygonField
from django.db import models


class FKBLayer(models.Model):
    objtype = models.CharField(max_length=32)
    geom = MultiPolygonField(srid=32632)

# Auto-generated `LayerMapping` dictionary for ByggFlate model
fkblayer_mapping = {
    'objtype' : 'OBJTYPE',
    'geom' : 'MULTIPOLYGON25D',
}
