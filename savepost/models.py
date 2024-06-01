from django.db import models

class PostUrls(models.Model):
    key = models.CharField(max_length=13, primary_key=True)
    file_url = models.URLField()
    views = models.IntegerField(default=0)
    del_date = models.DateField()
    