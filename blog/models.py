from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Entry(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())

    def __unicode__(self):
        return self.title
        
