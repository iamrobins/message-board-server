import uuid
from django.db import models

# Create your models here.
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    source = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content