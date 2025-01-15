from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True

    def __str__(self):
        return f"Создано: {self.created_at}, обновлено: {self.updated_at}"
