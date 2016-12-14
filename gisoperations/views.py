import json

from django.contrib.gis.gdal import DataSource
from rest_framework.response import Response
from rest_framework.views import APIView

from gisoperations.services import geojson, buffers


class BufferView(APIView):

    def post(self, request):
        """
        Buffer geojson features
        """
        source = request.data.get('geojson')
        buffer_meters = request.data.get('meters')
        data = buffers.buffer_geojson(json.dumps(source), buffer_meters)
        return Response(data)
