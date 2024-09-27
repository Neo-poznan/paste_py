from django.db import models
from django.utils import timezone
from .validators import date_validator


class Posts(models.Model):
    key = models.CharField(max_length=14, primary_key=True)
    views = models.IntegerField(default=0)
    del_date = models.DateField(validators=[date_validator])
    last_query = models.DateTimeField(auto_now=True)
    
    