from courses.models import UserLesson


def check_completion(user_exercise, exercise):
    # check if the user completed the exercise
    instructions_count = exercise.instructions.count()
    if user_exercise.instructions_completed.count() != instructions_count:
        return False

    # The user has completed all the instructions
    user_lesson, created = UserLesson.objects.get_or_create(user=user_exercise.user, lesson=exercise.lesson)
    user_lesson.exercises_completed.add(exercise)
    return True

