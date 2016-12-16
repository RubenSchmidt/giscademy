from courses.models import UserLesson


def get_user_progress_percent(user, lesson):
    user_lesson, created = UserLesson.objects.get_or_create(lesson=lesson, user=user)
    total_exercises = lesson.exercise_set.count()
    user_exercises = user_lesson.exercises_completed.count()
    return int((user_exercises / total_exercises) * 100)
