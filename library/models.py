from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    # latitude = models.FloatField()
    # longitude = models.FloatField()

    def __str__(self):
        return self.name    