from django.db import models
from django.utils import timezone
from .validators import date_validator


class PostUrls(models.Model):
    key = models.CharField(max_length=14, primary_key=True)
    file_url = models.URLField()
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    del_date = models.DateField(validators=[date_validator])
    last_query = models.DateTimeField(auto_now=True)
    
    