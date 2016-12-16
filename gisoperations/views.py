import json

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Exercise
from gisoperations.services import buffers
from layers.serializers import LayerSerializer


class BufferView(APIView):
    def post(self, request):
        """
        Buffer geojson features
        """
        exercise_slug = request.data.get('exercise_slug')
        if exercise_slug:
            exercise = get_object_or_404(Exercise, slug=exercise_slug)
        else:
            exercise = None

        layer_name = request.data.get('layer_name')
        source = request.data.get('geojson')
        buffer_meters = request.data.get('meters')

        layer = buffers.buffer_geojson(json.dumps(source), buffer_meters, layer_name, request.user, exercise)

        data = LayerSerializer(layer).data
        return Response(data)
