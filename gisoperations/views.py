import json

from rest_framework.response import Response
from rest_framework.views import APIView

from gisoperations.services import buffers


class BufferView(APIView):

    def post(self, request):
        """
        Buffer geojson features
        """
        source = request.data.get('geojson')
        buffer_meters = request.data.get('meters')
        feature_collection = buffers.buffer_geojson(json.dumps(source), buffer_meters)
        # Return a fake layer
        data = {
            'name':  request.data.get('name'),
            'polygons': feature_collection
        }
        return Response(data)
