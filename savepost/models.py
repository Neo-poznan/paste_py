from django.db import models
from .validators import date_validator


class PostUrls(models.Model):
    key = models.CharField(max_length=14, primary_key=True)
    file_url = models.URLField()
    views = models.IntegerField(default=0)
    del_date = models.DateField(validators=[date_validator])
    
    