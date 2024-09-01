from django.db import models
import uuid
class BaseModel(models.Model):
    uid=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at=models.DateField(auto_now=True)
    updated_at=models.DateField(auto_now_add=True)
    class Meta:
        abstract=True
