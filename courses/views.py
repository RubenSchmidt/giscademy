import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Exercise, Lesson, Course, UserExercise, Instruction, UserLesson
from courses.serializers import InstructionSerializer
from courses.services import exercises
from giscademy.utils.view_utils import ProtectedView


class LessonDetailView(ProtectedView):
    def get(self, request, course_slug, lesson_slug):
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        exercises = lesson.exercise_set.all().order_by('order')
        exercise = exercises.first()
        return HttpResponseRedirect(reverse('exercise-detail', args=[lesson.course.slug, lesson.slug, exercise.slug]))


class ExerciseDetailView(ProtectedView):
    template_name = 'exercise_detail.html'

    def get(self, request, course_slug, lesson_slug, exercise_slug):
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        exercise = get_object_or_404(Exercise, slug=exercise_slug, lesson=lesson)
        exercise_count = lesson.exercise_set.all().order_by('order').count()
        instructions = exercise.instructions.all()

        context = {
            'next_lesson': lesson.next_lesson,
            'exercise': exercise,
            'next_exercise': exercise.next_exercise,
            'prev_exercise': exercise.prev_exercise,
            'map_center_lat': json.dumps(exercise.map_center.y),
            'map_center_lng': json.dumps(exercise.map_center.x),
            'instructions': instructions,
            'exercise_count': exercise_count}
        return render(request, self.template_name, context)


class ExerciseInstructionList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, exercise_slug):
        exercise = get_object_or_404(Exercise, slug=exercise_slug)
        user_exercise, created = UserExercise.objects.get_or_create(exercise=exercise, user=request.user)
        instructions = exercise.instructions.all().order_by('order')
        data = InstructionSerializer(instructions, many=True, user_exercise=user_exercise).data
        return Response(data)


class CompleteInstructionView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, exercise_slug):
        exercise = get_object_or_404(Exercise, slug=exercise_slug)
        user_exercise, created = UserExercise.objects.get_or_create(exercise=exercise, user=request.user)

        instruction = get_object_or_404(Instruction, id=request.data.get('instruction_id'))
        user_exercise.instructions_completed.add(instruction)

        completed = exercises.check_completion(user_exercise, exercise)
        data = {
            'completed_exercise': completed
        }
        return Response(data, status=status.HTTP_201_CREATED)
