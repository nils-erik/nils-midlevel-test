from django.db import models

# models which would theoretically be used to populate our database
# with inspection and inspector data.  Includes company field to filter
# based on company name.
class inspection_model(models.Model):
    createdAt = models.TextField(max_length=120)
    city = models.TextField(max_length=120)
    scheduledDate = models.TextField(max_length=120)
    inspectorId = models.IntegerField()
    items = models.JSONField()
    company = models.CharField(max_length=120, default='')


class inspector_model(models.Model):
    createdAt = models.TextField(max_length=120)
    name = models.TextField(max_length=120)
    availableIntegrations = models.JSONField()
    inspectorId = models.IntegerField()
    company = models.CharField(max_length=120, default='')
