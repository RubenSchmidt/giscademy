import json

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from courses.models import Exercise
from gisoperations.services import operations


class GISOperationSerializer(serializers.Serializer):
    geojson = serializers.JSONField()
    extra_args = serializers.JSONField()

    extra_args_list = []

    def validate(self, attrs):
        extra_args = attrs['extra_args']
        for arg in self.extra_args_list:
            if arg not in extra_args:
                raise serializers.ValidationError('{} is required in extra args'.format(arg))
        return attrs

    def create(self, validated_data):
        raise NotImplementedError


class IntersectSerializer(GISOperationSerializer):
    extra_args_list = ['layer_name']

    def create(self, validated_data):
        extra_args = validated_data['extra_args']
        exercise_slug = extra_args.get('exercise_slug')
        if exercise_slug:
            exercise = get_object_or_404(Exercise, slug=exercise_slug)
        else:
            exercise = None
        layer_name = extra_args.get('layer_name')

        layer = operations.create_intersection_layer(
            json=json.dumps(validated_data['geojson']),
            layer_name=layer_name,
            user=self.context['request'].user,
            exercise=exercise
        )

        if not layer:
            raise serializers.ValidationError('Not valid geometry')
        return layer


class BufferSerializer(GISOperationSerializer):
    extra_args_list = ['layer_name', 'size']

    def create(self, validated_data):
        extra_args = validated_data['extra_args']
        exercise_slug = extra_args.get('exercise_slug')
        if exercise_slug:
            exercise = get_object_or_404(Exercise, slug=exercise_slug)
        else:
            exercise = None

        layer_name = extra_args.get('layer_name')
        buffer_meters = extra_args.get('size')

        layer = operations.create_buffer_layer(
            json.dumps(validated_data['geojson']),
            buffer_meters,
            layer_name,
            self.context['request'].user,
            exercise)
        return layer


