from django.db import models
from django.utils import timezone


class Timestampable(models.Model):
    """
    Adds implementation of the created_at and updated_at datetimes. Uses the timezone specified in the settings.
    Save method is overridden to make sure the updated_at also is in the correct timezone.
    """
    created_at = models.DateTimeField(
        default=timezone.now
    )

    updated_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super(Timestampable, self).save(*args, **kwargs)
