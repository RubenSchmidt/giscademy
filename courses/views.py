from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse

from courses.models import Exercise, Lesson
from giscademy.utils.view_utils import ProtectedView


class LessonDetailView(ProtectedView):
    def get(self, request, course_slug, lesson_slug):
        lesson = get_object_or_404(Lesson, slug=lesson_slug)

        # Check the users status
        exercises = lesson.exercise_set.all().order_by('order')
        exercise = exercises[0]
        return HttpResponseRedirect(reverse('exercise-detail', args=[lesson.course.slug, lesson.slug, exercise.slug]))


class ExerciseDetailView(ProtectedView):
    template_name = 'exercise_detail.html'

    def get(self, request, course_slug, lesson_slug, exercise_slug):
        exercise = get_object_or_404(Exercise, slug=exercise_slug)
        return render(request, self.template_name, {'exercise': exercise})
