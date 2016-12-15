from django.contrib import admin

# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin

from courses.models import Course, Lesson, Exercise, Enrollment, Instruction, UserExercise


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Exercise)
class ExerciseAdmin(OSMGeoAdmin):
    pass


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Instruction)
class InstructionAdmin(admin.ModelAdmin):
    pass


@admin.register(UserExercise)
class UserExerciseAdmin(admin.ModelAdmin):
    pass
