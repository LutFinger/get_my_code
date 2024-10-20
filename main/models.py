from django.db import models

class DateTimeStampedModel(models.Model):
    date_time_created = models.DateTimeField(auto_now_add=True, null=True)
    date_time_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
