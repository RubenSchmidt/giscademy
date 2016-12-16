from courses.models import Enrollment


def get_user_progress_percent(user, course):
    enrollment, created = Enrollment.objects.get_or_create(course=course, user=user)
    total_exercises = course.lessons.count()
    user_exercises = enrollment.lessons_completed.count()
    return int((user_exercises / total_exercises) * 100) if total_exercises != 0 else 0
