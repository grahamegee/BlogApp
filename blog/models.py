from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Entry(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    # only updates created date on add (not edit)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_date']
    
    def __unicode__(self):
        return self.title
        
