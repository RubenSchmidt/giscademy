import json

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from courses.models import Exercise
from gisoperations.services import operations
from gisoperations.services.operations import OperationsMixin
from layers.models import Layer


class GISOperationSerializer(serializers.Serializer, OperationsMixin):
    operation = serializers.CharField(max_length=255, required=True)
    geojson = serializers.JSONField()
    extra_args = serializers.JSONField()

    operation_function = None
    extra_args_list = ['layer_name']

    def validate(self, attrs):
        extra_args = attrs['extra_args']
        for arg in self.extra_args_list:
            if arg not in extra_args:
                raise serializers.ValidationError('{} is required in extra args'.format(arg))
        return attrs

    def create(self, validated_data):
        exercise = self._get_exercise(validated_data)
        extra_args = validated_data['extra_args']
        layer_name = extra_args.get('layer_name')
        layer = Layer.objects.create(name=layer_name, exercise=exercise, user=self.context['request'].user)
        operation_function = self._get_operation_function(validated_data)
        operation_function(json=json.dumps(validated_data['geojson']), layer=layer, **extra_args)
        return layer

    def _get_operation_function(self, validated_data):
        operation = validated_data['operation']
        if operation == 'buffer':
            return self.create_buffer_layer
        elif operation == 'intersect':
            return self.create_intersection_layer
        elif operation == 'merge':
            return self.create_merge_layer
        elif operation == 'union':
            return self.create_union_layer
        elif operation == 'difference':
            return self.create_difference_layer
        else:
            raise NotImplementedError

    @staticmethod
    def _get_exercise(validated_data):
        extra_args = validated_data['extra_args']
        exercise_slug = extra_args.get('exercise_slug')
        if exercise_slug:
            exercise = get_object_or_404(Exercise, slug=exercise_slug)
        else:
            exercise = None
        return exercise
