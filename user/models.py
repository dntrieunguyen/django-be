import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar_url = models.ImageField(upload_to="static/avatars", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted= models.BooleanField(default=False)
    deleted_at = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self)-> str:
        return str(self.id)
