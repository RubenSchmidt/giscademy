from courses.models import UserLesson, Enrollment


def get_user_progress_percent(user, lesson):
    user_lesson, created = UserLesson.objects.get_or_create(lesson=lesson, user=user)
    total_exercises = lesson.exercise_set.count()
    user_exercises = user_lesson.exercises_completed.count()
    return int((user_exercises / total_exercises) * 100) if total_exercises != 0 else 0


def check_completion(user_lesson, lesson):
    exercise_count = lesson.exercise_set.count()
    if user_lesson.exercises_completed.count() != exercise_count:
        return False

    # The user has completed all the exercises
    enrollment, created = Enrollment.objects.get_or_create(user=user_lesson.user, course=lesson.course)
    enrollment.lessons_completed.add(lesson)
    return True
