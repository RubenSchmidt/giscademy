from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


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


class Lesson(SlugTitleable):
    course = models.ForeignKey('courses.Course', related_name='lessons')
    overview = models.TextField()

    def __str__(self):
        return self.title


class Exercise(SlugTitleable):
    lesson = models.ForeignKey('courses.Lesson')

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey('auth.User')
    course = models.ForeignKey('courses.Course')
