from django.contrib.auth.models import User
from django.db import models

from commodityAccounting.middleware import get_current_user


class UserTrackingMixin(models.Model):
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="Изменено пользователем")

    def save(self, *args, **kwargs):
        self.modified_by = get_current_user()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
