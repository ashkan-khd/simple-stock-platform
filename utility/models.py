from django.db import models


class CreateHistoryModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateHistoryModel(models.Model):
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseHistoryModel(CreateHistoryModel, UpdateHistoryModel):
    class Meta:
        abstract = True


def null_blank(value=True):
    return {
        'null': value,
        'blank': value
    }