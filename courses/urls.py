from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<course_slug>[-\w]+)/lessons/(?P<lesson_slug>[-\w]+)/$',
        views.LessonDetailView.as_view(), name='lesson-detail'),

    url(r'^(?P<course_slug>[-\w]+)/lessons/(?P<lesson_slug>[-\w]+)/exercises/(?P<exercise_slug>[-\w]+)/$',
        views.ExerciseDetailView.as_view(), name='exercise-detail'),

    url(r'^(?P<exercise_slug>[-\w]+)/instructions/$', views.ExerciseInstructionList.as_view(), name='exercise-instruction-list'),

    url(r'^(?P<exercise_slug>[-\w]+)/instructions/complete-instruction/$', views.CompleteInstructionView.as_view(), name='complete-instruction'),
]
