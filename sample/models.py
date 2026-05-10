from django.db import models
from core.models import CoreModel

class Item(CoreModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
