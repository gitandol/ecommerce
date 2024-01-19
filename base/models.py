from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        qs = super(BaseManager, self).get_queryset()
        return qs


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()
