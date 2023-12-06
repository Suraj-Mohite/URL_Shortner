from django.db import models
from Base.models import BaseModel
from django.contrib.auth.models import User

# Create your models here.

class URL(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_url = models.URLField()
    alias = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['-created_at']