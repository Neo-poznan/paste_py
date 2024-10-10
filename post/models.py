from django.db import models
from django.utils import timezone
from .validators import post_date_validator


class Posts(models.Model):
    '''Таблица для хранения информации о постах'''
    key = models.CharField(max_length=14, primary_key=True, verbose_name='название файла в хранилище S3')
    views_count = models.IntegerField(default=0, verbose_name='счетчик просмотров')
    delete_date = models.DateField(validators=[post_date_validator], verbose_name='дата удаления поста')
    last_query = models.DateTimeField(auto_now=True, verbose_name='время последнего запроса')
    
    