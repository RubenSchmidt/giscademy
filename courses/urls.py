from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<course_slug>[-\w]+)/lessons/(?P<lesson_slug>[-\w]+)/$',
        views.LessonDetailView.as_view(), name='lesson-detail'),

    url(r'^(?P<course_slug>[-\w]+)/lessons/(?P<lesson_slug>[-\w]+)/exercises/(?P<exercise_slug>[-\w]+)/$',
        views.ExerciseDetailView.as_view(), name='exercise-detail'),
]
