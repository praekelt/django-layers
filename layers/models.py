from django.db import models

from layers import monkey


class Layer(models.Model):
    """A model to represent a layer. This exists purely to facilitate filtering
    at database level."""
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name
