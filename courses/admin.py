from django.contrib import admin

# Register your models here.
from courses.models import Course, Lesson, Exercise, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    pass


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass
