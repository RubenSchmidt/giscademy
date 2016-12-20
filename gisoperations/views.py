from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from gisoperations.serializers import BufferSerializer, IntersectSerializer, MergeSerializer, UnionSerializer, \
    DifferenceSerializer
from layers.serializers import LayerSerializer


class OperationView(APIView):
    def post(self, request):
        """
        Do GIS operations on geojson features
        """

        operation = request.data.get('operation')
        if not operation:
            return Response('operation is required', status=status.HTTP_400_BAD_REQUEST)

        serializer_class = self.get_serializer_class(operation)
        serializer = serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        layer = serializer.save()
        data = LayerSerializer(layer).data
        return Response(data)

    @staticmethod
    def get_serializer_class(operation):
        """
        Get the correct serializer for the given operation.
        """
        if operation == 'buffer':
            return BufferSerializer
        elif operation == 'intersect':
            return IntersectSerializer
        elif operation == 'merge':
            return MergeSerializer
        elif operation == 'union':
            return UnionSerializer
        elif operation == 'difference':
            return DifferenceSerializer
        else:
            raise NotImplementedError
