from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


class SlugTitleable(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(SlugTitleable, self).save(*args, **kwargs)


class Course(SlugTitleable):
    overview = models.TextField()
    difficulty = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    def is_enrolled(self, user: User):
        return Enrollment.objects.filter(course=self, user=user).exists()

    def enroll(self, user: User):
        """
        Enroll the user to the course if he is not already enrolled
        :param user:
        :return: Enrollment object
        """
        return Enrollment.objects.get_or_create(course=self, user=user)


class Enrollment(models.Model):
    user = models.ForeignKey('auth.User')
    course = models.ForeignKey('courses.Course')
    lessons_completed = models.ManyToManyField(
        'courses.Lesson'
    )


class Lesson(SlugTitleable):
    course = models.ForeignKey('courses.Course', related_name='lessons')
    overview = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    next_lesson = models.ForeignKey('self', related_name='next', blank=True, null=True)
    prev_lesson = models.ForeignKey('self', related_name='prev', null=True, blank=True)

    def __str__(self):
        return '{} | {}'.format(self.course, self.title)


class UserLesson(models.Model):
    user = models.ForeignKey('auth.User')
    lesson = models.ForeignKey('courses.Lesson', related_name='lessons')
    exercises_completed = models.ManyToManyField(
        'courses.Exercise'
    )


class Exercise(SlugTitleable):
    lesson = models.ForeignKey('courses.Lesson')
    order = models.PositiveSmallIntegerField(default=0)
    description = RichTextField()
    map_center = PointField(blank=True, null=True)

    next_exercise = models.ForeignKey('self', related_name='next', blank=True, null=True)
    prev_exercise = models.ForeignKey('self', related_name='prev', null=True, blank=True)

    def __str__(self):
        return '{} | {}'.format(self.lesson, self.title)


class UserExercise(models.Model):
    """
    Save the exercise status for a user.
    """

    exercise = models.ForeignKey('courses.Exercise')
    user = models.ForeignKey('auth.User')
    instructions_completed = models.ManyToManyField(
        'courses.Instruction'
    )


class Instruction(models.Model):
    exercise = models.ForeignKey('courses.Exercise', related_name='instructions')
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    completionOperation = models.CharField(max_length=255)
    completionArgs = JSONField(null=True, blank=True)

    def __str__(self):
        return self.description
