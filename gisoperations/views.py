from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gisoperations.serializers import BufferSerializer, IntersectSerializer
from layers.serializers import LayerSerializer


class OperationView(APIView):
    def post(self, request):
        """
        Do GIS operations on geojson features
        """

        operation = request.data.get('operation')
        if not operation:
            return Response('operation is required', status=status.HTTP_400_BAD_REQUEST)

        if operation == 'buffer':
            serializer = BufferSerializer(data=request.data, context={'request': request})
        elif operation == 'intersect':
            serializer = IntersectSerializer(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        layer = serializer.save()
        data = LayerSerializer(layer).data
        return Response(data)
