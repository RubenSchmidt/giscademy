from django.contrib.gis.db.models import MultiPolygonField
from django.db import models


# Create your models here.
class ByggFlate(models.Model):
    poly_field = models.FloatField()
    poly_id = models.FloatField()
    koordh = models.FloatField()
    objtype = models.CharField(max_length=32)
    byggtyp_nb = models.IntegerField()
    byggstat = models.CharField(max_length=2)
    byggnr = models.IntegerField()
    sefrakkomm = models.IntegerField()
    registreri = models.IntegerField()
    husloepenr = models.IntegerField()
    komm = models.CharField(max_length=4)
    produkt = models.CharField(max_length=15)
    versjon = models.CharField(max_length=50)
    omradeid = models.CharField(max_length=4)
    orgdatvert = models.CharField(max_length=50)
    kopidato = models.CharField(max_length=20)
    geom = MultiPolygonField(srid=4326)

# Auto-generated `LayerMapping` dictionary for ByggFlate model
byggflate_mapping = {
    'poly_field' : 'POLY_',
    'poly_id' : 'POLY_ID',
    'koordh' : 'KOORDH',
    'objtype' : 'OBJTYPE',
    'byggtyp_nb' : 'BYGGTYP_NB',
    'byggstat' : 'BYGGSTAT',
    'byggnr' : 'BYGGNR',
    'sefrakkomm' : 'SEFRAKKOMM',
    'registreri' : 'REGISTRERI',
    'husloepenr' : 'HUSLOEPENR',
    'komm' : 'KOMM',
    'produkt' : 'PRODUKT',
    'versjon' : 'VERSJON',
    'omradeid' : 'OMRADEID',
    'orgdatvert' : 'ORGDATVERT',
    'kopidato' : 'KOPIDATO',
    'geom' : 'MULTIPOLYGON25D',
}
