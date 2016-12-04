from django.db import models

# Create your models here.
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


class Lesson(SlugTitleable):
    course = models.ForeignKey('courses.Course', related_name='lessons')
    overview = models.TextField()


class Exercise(SlugTitleable):
    lesson = models.ForeignKey('courses.Lesson')
