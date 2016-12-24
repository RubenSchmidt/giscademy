from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gisoperations.serializers import GISOperationSerializer
from layers.serializers import LayerSerializer


class OperationView(APIView):
    def post(self, request):
        """
        Do GIS operations on geojson features
        """
        serializer = GISOperationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        layer = serializer.save()
        data = LayerSerializer(layer).data
        return Response(data)

