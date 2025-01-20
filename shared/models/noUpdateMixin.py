from django.core.exceptions import ValidationError
from django.db import models


class NoUpdateModel(models.Model):
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("Updates are not allowed for this model.")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
